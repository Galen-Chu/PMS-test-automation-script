import argparse
import configparser
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import requests

BASE_URL = "https://api.qase.io/v1"
DEFAULT_PROJECT = "PMS"

PRIORITY_MAP = {0: "not set", 1: "high", 2: "medium", 3: "low"}
SEVERITY_MAP = {
    0: "not set",
    1: "blocker",
    2: "critical",
    3: "major",
    4: "normal",
    5: "minor",
    6: "trivial",
}
AUTOMATION_MAP = {0: "not-automated", 1: "to-be-automated", 2: "automated"}
STATUS_MAP = {0: "actual", 1: "draft", 2: "deprecated"}
RUN_STATUS_MAP = {0: "in_progress", 1: "passed", 2: "failed", 3: "interrupted"}


def _read_pytest_ini(key):
    ini_path = Path(__file__).resolve().parent.parent / "pytest.ini"
    if not ini_path.exists():
        return None
    with open(ini_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith(f"{key}") and "=" in line:
                value = line.split("=", 1)[1].strip()
                if value:
                    return value
    return None


def _get_token():
    token = os.environ.get("QASE_API_TOKEN") or _read_pytest_ini("QASE_API_TOKEN")
    if not token:
        print("ERROR: QASE_API_TOKEN not found in env or pytest.ini", file=sys.stderr)
        sys.exit(1)
    return token


def _api_get(endpoint, params=None):
    headers = {"Token": _get_token(), "Content-Type": "application/json"}
    url = f"{BASE_URL}/{endpoint}"
    resp = requests.get(url, headers=headers, params=params, timeout=30)
    if resp.status_code != 200:
        print(f"ERROR: API returned {resp.status_code}", file=sys.stderr)
        try:
            detail = resp.json()
            print(f"  {detail}", file=sys.stderr)
        except Exception:
            print(f"  {resp.text[:200]}", file=sys.stderr)
        sys.exit(1)
    data = resp.json()
    if not data.get("status"):
        print(f"ERROR: API response status=false", file=sys.stderr)
        print(f"  {data}", file=sys.stderr)
        sys.exit(1)
    return data["result"]


AUTOMATION_REVERSE = {v: k for k, v in AUTOMATION_MAP.items()}


def _api_patch(endpoint, payload):
    headers = {"Token": _get_token(), "Content-Type": "application/json"}
    url = f"{BASE_URL}/{endpoint}"
    resp = requests.patch(url, headers=headers, json=payload, timeout=30)
    if resp.status_code != 200:
        print(f"ERROR: API returned {resp.status_code}", file=sys.stderr)
        try:
            detail = resp.json()
            print(f"  {detail}", file=sys.stderr)
        except Exception:
            print(f"  {resp.text[:200]}", file=sys.stderr)
        sys.exit(1)
    data = resp.json()
    if not data.get("status"):
        print(f"ERROR: API response status=false", file=sys.stderr)
        print(f"  {data}", file=sys.stderr)
        sys.exit(1)
    return data["result"]


def _format_case(case):
    lines = []
    lines.append(f"Case #{case['id']}: {case['title']}")
    lines.append(f"Suite: #{case.get('suite_id', 'N/A')}")

    status = STATUS_MAP.get(case.get("status"), str(case.get("status", "N/A")))
    priority = PRIORITY_MAP.get(case.get("priority"), str(case.get("priority", "N/A")))
    automation = AUTOMATION_MAP.get(case.get("automation"), str(case.get("automation", "N/A")))
    lines.append(f"Status: {status} | Priority: {priority} | Automation: {automation}")

    preconditions = (case.get("preconditions") or "").strip()
    if preconditions:
        lines.append("")
        lines.append("Preconditions:")
        for line in preconditions.split("\n"):
            lines.append(f"  {line}")

    postconditions = (case.get("postconditions") or "").strip()
    if postconditions:
        lines.append("")
        lines.append("Postconditions:")
        for line in postconditions.split("\n"):
            lines.append(f"  {line}")

    steps_type = case.get("steps_type", "classic")
    steps = case.get("steps", [])
    if steps:
        lines.append("")
        if steps_type == "gherkin":
            lines.append("Steps (Gherkin):")
            for step in steps:
                action = (step.get("action") or "").strip()
                for gherkin_line in action.split("\n"):
                    lines.append(f"  {gherkin_line}")
        else:
            lines.append("Steps:")
            for step in sorted(steps, key=lambda s: s.get("position", 0)):
                pos = step.get("position", "?")
                action = (step.get("action") or "").strip()
                expected = (step.get("expected_result") or "").strip()
                data = (step.get("data") or "").strip()
                lines.append(f"  {pos}. [Action] {action}")
                if expected:
                    lines.append(f"     [Expected] {expected}")
                if data:
                    lines.append(f"     [Data] {data}")

    return "\n".join(lines)


def _format_cases_list(entities, suite_id):
    lines = []
    lines.append(f"Suite #{suite_id} ({len(entities)} cases)")
    lines.append("")
    for case in entities:
        cid = f"#{case['id']}"
        title = case.get("title", "")
        automation = AUTOMATION_MAP.get(case.get("automation"), str(case.get("automation", "")))
        params = case.get("params", [])
        params_tag = f" params:{len(params)}" if params else ""
        lines.append(f"  {cid:<6} {title:<40} [{automation}]{params_tag}")
    return "\n".join(lines)


def _format_suites_list(entities, project):
    lines = []
    lines.append(f"Project: {project} ({len(entities)} suites)")
    lines.append("")
    for suite in entities:
        sid = f"#{suite['id']}"
        title = suite.get("title", "")
        count = suite.get("cases_count", 0)
        parent = suite.get("parent_id")
        prefix = f"  (parent: #{parent})" if parent else ""
        lines.append(f"  {sid:<6} {title:<40} ({count} cases){prefix}")
    return "\n".join(lines)


def cmd_get_case(args):
    result = _api_get(f"case/{args.project}/{args.case_id}")
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(_format_case(result))


def cmd_list_cases(args):
    params = {"suite_id": args.suite_id, "limit": 100, "offset": 0}
    result = _api_get(f"case/{args.project}", params=params)
    entities = result.get("entities", [])
    if args.json:
        print(json.dumps(entities, ensure_ascii=False, indent=2))
    else:
        print(_format_cases_list(entities, args.suite_id))


def cmd_update_case(args):
    payload = {}

    if args.automation:
        auto_val = AUTOMATION_REVERSE.get(args.automation)
        if auto_val is None:
            print(
                f"ERROR: invalid automation value '{args.automation}', must be one of: {list(AUTOMATION_REVERSE.keys())}",
                file=sys.stderr,
            )
            sys.exit(1)
        payload["automation"] = auto_val

    if args.fields:
        for f in args.fields:
            if "=" not in f:
                print(f"ERROR: --field format is key=value, got '{f}'", file=sys.stderr)
                sys.exit(1)
            key, val = f.split("=", 1)
            try:
                payload[key] = int(val)
            except ValueError:
                payload[key] = val

    if args.params:
        parsed = json.loads(args.params)
        payload["params"] = [
            {"title": title, "values": values if isinstance(values, list) else [values]}
            for title, values in parsed.items()
        ]

    if args.steps_file:
        with open(args.steps_file, encoding="utf-8") as f:
            gherkin_text = f.read().strip()
        payload["steps_type"] = "gherkin"
        payload["steps"] = [{"action": gherkin_text, "expected_result": ""}]
    elif args.steps:
        payload["steps_type"] = "gherkin"
        payload["steps"] = [{"action": args.steps.strip(), "expected_result": ""}]

    if not payload:
        print(
            "ERROR: nothing to update (use --automation, --field, --params, or --steps/--steps-file)",
            file=sys.stderr,
        )
        sys.exit(1)

    if not args.yes:
        current = _api_get(f"case/{args.project}/{args.case_id}")
        print(f"Case #{args.case_id}: {current['title']}")
        print(f"  Current automation: {AUTOMATION_MAP.get(current.get('automation'), '?')}")
        print(f"  Updates: {json.dumps(payload, ensure_ascii=False)}")
        confirm = input("  Proceed? [y/N] ").strip().lower()
        if confirm != "y":
            print("Cancelled.")
            return

    result = _api_patch(f"case/{args.project}/{args.case_id}", payload)
    print(f"Updated case #{args.case_id} (id={result.get('id', args.case_id)})")

    if args.automation:
        print(f"  automation → {args.automation}")
    if args.steps or args.steps_file:
        print(f"  steps → updated (gherkin)")


def cmd_list_suites(args):
    params = {"limit": 100, "offset": 0}
    result = _api_get(f"suite/{args.project}", params=params)
    entities = result.get("entities", [])
    if args.json:
        print(json.dumps(entities, ensure_ascii=False, indent=2))
    else:
        print(_format_suites_list(entities, args.project))


def _format_plans_list(entities, project):
    lines = []
    lines.append(f"Project: {project} ({len(entities)} plans)")
    lines.append("")
    for plan in entities:
        pid = f"#{plan['id']}"
        title = plan.get("title", "")
        count = plan.get("cases_count", 0)
        updated = plan.get("updated", "")[:10]
        lines.append(f"  {pid:<6} {title:<40} ({count} cases) | {updated}")
    return "\n".join(lines)


def cmd_list_plans(args):
    params = {"limit": 100, "offset": 0}
    result = _api_get(f"plan/{args.project}", params=params)
    entities = result.get("entities", [])
    if args.json:
        print(json.dumps(entities, ensure_ascii=False, indent=2))
    else:
        print(_format_plans_list(entities, args.project))


def _format_plan_detail(plan):
    lines = []
    lines.append(f"Plan #{plan['id']}: {plan['title']}")
    if plan.get("description"):
        lines.append(f"Description: {plan['description']}")
    cases = plan.get("cases", [])
    lines.append(f"Cases: {len(cases)}")
    lines.append(f"Created: {plan.get('created', 'N/A')}")
    lines.append(f"Updated: {plan.get('updated', 'N/A')}")
    if cases:
        lines.append("")
        lines.append("Case IDs: " + ", ".join(str(c["case_id"]) for c in cases))
    return "\n".join(lines)


def cmd_get_plan(args):
    result = _api_get(f"plan/{args.project}/{args.plan_id}")
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(_format_plan_detail(result))


def _format_runs_list(entities, project):
    lines = []
    lines.append(f"Project: {project} ({len(entities)} runs)")
    lines.append("")
    for run in entities:
        rid = f"#{run['id']}"
        title = run.get("title", "")
        status = RUN_STATUS_MAP.get(run.get("status"), str(run.get("status", "")))
        stats = run.get("stats", {})
        total = stats.get("total", 0)
        passed = stats.get("passed", 0)
        failed = stats.get("failed", 0)
        untested = stats.get("untested", 0)
        start = run.get("start_time", "")[:10] if run.get("start_time") else "N/A"
        lines.append(
            f"  {rid:<6} {title:<40} [{status}] "
            f"T:{total} P:{passed} F:{failed} U:{untested} | {start}"
        )
    return "\n".join(lines)


def cmd_list_runs(args):
    params = {"limit": args.limit or 25, "offset": 0}
    result = _api_get(f"run/{args.project}", params=params)
    entities = result.get("entities", [])
    if args.json:
        print(json.dumps(entities, ensure_ascii=False, indent=2))
    else:
        print(_format_runs_list(entities, args.project))


def _format_run_detail(run):
    lines = []
    lines.append(f"Run #{run['id']}: {run['title']}")
    status = RUN_STATUS_MAP.get(run.get("status"), str(run.get("status", "")))
    lines.append(f"Status: {status}")
    stats = run.get("stats", {})
    lines.append(
        f"Total: {stats.get('total', 0)} | Passed: {stats.get('passed', 0)} | "
        f"Failed: {stats.get('failed', 0)} | Untested: {stats.get('untested', 0)} | "
        f"Blocked: {stats.get('blocked', 0)} | Skipped: {stats.get('skipped', 0)}"
    )
    lines.append(f"Start: {run.get('start_time') or 'N/A'}")
    lines.append(f"End: {run.get('end_time') or 'N/A'}")
    env = run.get("environment")
    if env:
        lines.append(f"Environment: {env.get('title', 'N/A')}")
    milestone = run.get("milestone")
    if milestone:
        lines.append(f"Milestone: {milestone.get('title', 'N/A')}")
    plan_id = run.get("plan_id")
    if plan_id:
        lines.append(f"Plan: #{plan_id}")
    return "\n".join(lines)


def cmd_get_run(args):
    result = _api_get(f"run/{args.project}/{args.run_id}")
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(_format_run_detail(result))


def _format_results_list(entities, run_id):
    lines = []
    seen = _dedupe_results(entities)
    results = sorted(seen.values(), key=lambda r: r["case_id"])
    lines.append(f"Run #{run_id}: {len(results)} cases (latest result per case)")
    lines.append("")
    for r in results:
        cid = f"#{r['case_id']}"
        status = r.get("status", "?")
        end = (r.get("end_time") or "N/A")[:16]
        lines.append(f"  Case {cid:<6} {status:<10} {end}")
    return "\n".join(lines)


def _dedupe_results(entities):
    seen = {}
    for r in entities:
        cid = r["case_id"]
        if cid not in seen or (r.get("end_time") or "") > (seen[cid].get("end_time") or ""):
            seen[cid] = r
    return seen


def _fetch_all_results(project, run_id):
    all_entities = []
    limit = 100
    offset = 0
    while True:
        params = {"run": run_id, "limit": limit, "offset": offset}
        result = _api_get(f"result/{project}", params=params)
        entities = result.get("entities", [])
        all_entities.extend(entities)
        if len(entities) < limit:
            break
        offset += limit
    return _dedupe_results(all_entities)


def _fetch_all_results_raw(project, run_id):
    all_entities = []
    limit = 100
    offset = 0
    while True:
        params = {"run": run_id, "limit": limit, "offset": offset}
        result = _api_get(f"result/{project}", params=params)
        entities = result.get("entities", [])
        all_entities.extend(entities)
        if len(entities) < limit:
            break
        offset += limit
    return all_entities


def _param_combo_count(params):
    if not params:
        return 1
    if isinstance(params, dict):
        values = params.values()
    else:
        values = [p.get("values", []) for p in params]
    total = 1
    for v in values:
        total *= len(v) if isinstance(v, list) else 1
    return total


def cmd_list_results(args):
    all_entities = []
    limit = 100
    offset = 0
    while True:
        params = {"run": args.run_id, "limit": limit, "offset": offset}
        result = _api_get(f"result/{args.project}", params=params)
        entities = result.get("entities", [])
        all_entities.extend(entities)
        if len(entities) < limit:
            break
        offset += limit
    if args.json:
        print(json.dumps(all_entities, ensure_ascii=False, indent=2))
    else:
        print(_format_results_list(all_entities, args.run_id))


def _fetch_all_suite_names(project):
    suite_names = {}
    params = {"limit": 100, "offset": 0}
    result = _api_get(f"suite/{project}", params=params)
    for s in result.get("entities", []):
        suite_names[s["id"]] = s.get("title", f"#{s['id']}")
    return suite_names


def cmd_run_untested(args):
    t0 = time.time()

    run = _api_get(f"run/{args.project}/{args.run_id}")
    plan_id = args.plan or run.get("plan_id")
    if not plan_id:
        print(
            f"ERROR: Run #{args.run_id} has no plan. Use --plan <id> to specify.", file=sys.stderr
        )
        sys.exit(1)

    plan = _api_get(f"plan/{args.project}/{plan_id}")
    plan_cases = plan.get("cases", [])
    plan_case_ids = sorted(c["case_id"] for c in plan_cases)

    raw_results = _fetch_all_results_raw(args.project, args.run_id)
    result_counts = {}
    for r in raw_results:
        result_counts[r["case_id"]] = result_counts.get(r["case_id"], 0) + 1

    def fetch_case(cid):
        return _api_get(f"case/{args.project}/{cid}")

    with ThreadPoolExecutor(max_workers=10) as pool:
        case_results = list(pool.map(fetch_case, plan_case_ids))
        suite_names_future = pool.submit(_fetch_all_suite_names, args.project)
    case_map = {c["id"]: c for c in case_results}
    suite_names = suite_names_future.result()

    untested_info = []
    total_combos = 0

    for cid in plan_case_ids:
        c = case_map.get(cid)
        if not c:
            c = _api_get(f"case/{args.project}/{cid}")
        params = c.get("params", [])
        combos = _param_combo_count(params)
        total_combos += combos
        tested = result_counts.get(cid, 0)

        if tested < combos:
            untested_info.append(
                {
                    "id": cid,
                    "title": c.get("title", "?"),
                    "automation": AUTOMATION_MAP.get(c.get("automation"), "?"),
                    "suite_id": c.get("suite_id"),
                    "tested": tested,
                    "total": combos,
                }
            )

    elapsed = time.time() - t0

    by_suite = {}
    for info in untested_info:
        sid = info["suite_id"]
        by_suite.setdefault(sid, []).append(info)

    tested_total = len(raw_results)
    lines = []
    lines.append(f"Run #{args.run_id}: {run['title']}")
    lines.append(f"Plan #{plan_id}: {plan['title']} ({len(plan_case_ids)} cases)")
    lines.append(
        f"Combinations: {total_combos} | Tested: {tested_total} | Untested: {total_combos - tested_total}"
    )
    lines.append("")

    lines.append(f"({elapsed:.1f}s)")
    lines.append("")

    if not untested_info:
        print(f"Run #{args.run_id}: all {total_combos} combinations tested! ({elapsed:.1f}s)")
        return

    for sid in sorted(by_suite.keys(), key=lambda s: suite_names.get(s, "")):
        cases = by_suite[sid]
        sname = suite_names.get(sid, f"Suite #{sid}")
        lines.append(f"  [{sname}] ({len(cases)} cases)")
        for info in cases:
            auto = info["automation"]
            count = f"{info['tested']}/{info['total']}" if info["total"] > 1 else ""
            lines.append(f"    #{info['id']:<6} {info['title']:<50} [{auto}] {count}".rstrip())
        lines.append("")

    print("\n".join(lines).rstrip())


def main():
    parser = argparse.ArgumentParser(prog="qase-cli", description="Qase test case management CLI")
    parser.add_argument(
        "-p",
        "--project",
        default=DEFAULT_PROJECT,
        help=f"Qase project code (default: {DEFAULT_PROJECT})",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("get-case", help="Get a specific test case by ID")
    p.add_argument("case_id", type=int, help="Test case ID")
    p.add_argument("--json", action="store_true", help="Output as JSON")
    p.set_defaults(func=cmd_get_case)

    p = sub.add_parser("list-cases", help="List test cases in a suite")
    p.add_argument("suite_id", type=int, help="Suite ID")
    p.add_argument("--json", action="store_true", help="Output as JSON")
    p.set_defaults(func=cmd_list_cases)

    p = sub.add_parser(
        "update-case", help="Update a test case (automation status, steps, fields, params)"
    )
    p.add_argument("case_id", type=int, help="Test case ID")
    p.add_argument(
        "--automation", "-a", choices=list(AUTOMATION_REVERSE.keys()), help="Set automation status"
    )
    p.add_argument(
        "--field",
        "-f",
        dest="fields",
        action="append",
        help="Set arbitrary field (key=value, repeatable)",
    )
    p.add_argument(
        "--params", "-pm", help='Set params as JSON string, e.g. \'{"key":["v1","v2"]}\''
    )
    p.add_argument("--steps", "-s", help="Gherkin steps text (inline)")
    p.add_argument("--steps-file", "-sf", help="Read Gherkin steps from file")
    p.add_argument("--yes", "-y", action="store_true", help="Skip confirmation")
    p.set_defaults(func=cmd_update_case)

    p = sub.add_parser("list-suites", help="List all test suites")
    p.add_argument("--json", action="store_true", help="Output as JSON")
    p.set_defaults(func=cmd_list_suites)

    p = sub.add_parser("list-plans", help="List test plans")
    p.add_argument("--json", action="store_true", help="Output as JSON")
    p.set_defaults(func=cmd_list_plans)

    p = sub.add_parser("get-plan", help="Get plan details with case list")
    p.add_argument("plan_id", type=int, help="Plan ID")
    p.add_argument("--json", action="store_true", help="Output as JSON")
    p.set_defaults(func=cmd_get_plan)

    p = sub.add_parser("list-runs", help="List test runs")
    p.add_argument("--limit", type=int, default=25, help="Max runs to return (default: 25)")
    p.add_argument("--json", action="store_true", help="Output as JSON")
    p.set_defaults(func=cmd_list_runs)

    p = sub.add_parser("get-run", help="Get test run details")
    p.add_argument("run_id", type=int, help="Run ID")
    p.add_argument("--json", action="store_true", help="Output as JSON")
    p.set_defaults(func=cmd_get_run)

    p = sub.add_parser("list-results", help="List results for a test run")
    p.add_argument("run_id", type=int, help="Run ID")
    p.add_argument("--json", action="store_true", help="Output as JSON")
    p.set_defaults(func=cmd_list_results)

    p = sub.add_parser("run-untested", help="List untested cases in a run (requires plan)")
    p.add_argument("run_id", type=int, help="Run ID")
    p.add_argument("--plan", type=int, help="Plan ID (auto-detected from run, or override)")
    p.set_defaults(func=cmd_run_untested)

    args = parser.parse_args()
    try:
        args.func(args)
    except requests.exceptions.ConnectionError:
        print("ERROR: Cannot connect to Qase API", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.Timeout:
        print("ERROR: API request timed out", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
