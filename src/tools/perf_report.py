"""HTML performance report generator.

Produces a standalone HTML report from performance test analysis data.
Called directly by perf tests — no manual post-processing needed.
Adapts display based on measurement type (page load vs booking flow).
"""

import html
import json
from datetime import datetime
from pathlib import Path

from tools.perf_analyzer import format_duration


def _esc(text: str) -> str:
    """跳脫 API 名稱等動態字串，避免破壞 HTML 結構"""
    return html.escape(str(text))


_STYLE = """
<style>
  body { font-family: system-ui, -apple-system, sans-serif; margin: 20px; background: #f9f9f7; color: #0b0b0b; }
  .card { background: #fcfcfb; border: 1px solid #e1e0d9; border-radius: 8px; padding: 16px; margin: 16px 0; }
  h1 { font-size: 22px; margin: 0; }
  h2 { font-size: 16px; margin: 10px 0; }
  table { border-collapse: collapse; width: 100%; font-size: 13px; }
  th, td { padding: 6px 10px; text-align: left; border-bottom: 1px solid #e1e0d9; }
  th { color: #52514e; font-weight: 600; font-size: 12px; }
  .stat { font-size: 28px; font-weight: 650; }
  .label { font-size: 12px; color: #898781; }
  .violation { color: #d03b3b; font-weight: 600; }
  .pass { color: #0ca30c; font-weight: 600; }
  .sub { font-size: 12px; color: #52514e; line-height: 1.5; }
  .bars { margin: 4px 0; }
  .bar { height: 14px; background: #2a78d6; border-radius: 3px; display: inline-block; vertical-align: middle; }
  .bar-label { font-size: 12px; color: #52514e; vertical-align: middle; margin-left: 4px; }
</style>
"""


def generate_page_load_report(apis: list, metadata: dict) -> str:
    """Generate report for page-load performance test."""
    meta = metadata or {}
    total = len(apis)
    durations = [a["duration"] for a in apis]
    slowest = sorted(apis, key=lambda x: x["duration"], reverse=True)
    max_dur = max(durations) if durations else 0

    parts = [
        "<!DOCTYPE html><html><head><meta charset='UTF-8'>",
        f"<title>Page Load Performance Report</title>{_STYLE}</head><body>",
        "<h1>Page Load Performance Report</h1>",
        f"<div class='sub'>Test: {meta.get('test', 'N/A')} | "
        f"Env: {meta.get('env', 'N/A')} | "
        f"Date: {meta.get('date', datetime.now().strftime('%Y-%m-%d %H:%M'))}</div>",
    ]

    # Summary cards
    parts.append("<div style='display:flex;gap:12px;flex-wrap:wrap'>")
    parts.append(_card("Total API Calls", str(total)))
    parts.append(_card("Slowest API", format_duration(max_dur)))
    parts.append(_card("Avg Duration", format_duration(sum(durations) / total if total else 0)))
    parts.append("</div>")

    # API bar chart (top 15)
    if slowest:
        parts.append("<div class='card'><h2>API Response Times (Top 15)</h2>")
        max_val = slowest[0]["duration"] or 1
        for api in slowest[:15]:
            pct = (api["duration"] / max_val) * 100
            color = "#d03b3b" if api["duration"] > 10000 else "#2a78d6"
            parts.append(
                f"<div class='bars'>"
                f"<span class='bar' style='width:{pct:.0f}%;background:{color}'></span>"
                f"<span class='bar-label'>{format_duration(api['duration'])} — {_esc(api['name'])}</span>"
                f"</div>"
            )
        parts.append("</div>")

    # Full API table
    if slowest:
        parts.append("<div class='card'><h2>All API Calls</h2>")
        parts.append("<table><tr><th>#</th><th>API</th><th>Duration</th></tr>")
        for i, api in enumerate(slowest, 1):
            parts.append(f"<tr><td>{i}</td><td>{_esc(api['name'])}</td>")
            dur_str = format_duration(api["duration"])
            color = " style='color:#d03b3b'" if api["duration"] > 10000 else ""
            parts.append(f"<td{color}>{dur_str}</td></tr>")
        parts.append("</table></div>")

    parts.append("</body></html>")
    return "\n".join(parts)


def generate_booking_report(analysis: dict, metadata: dict) -> str:
    """Generate report for booking flow performance test."""
    meta = metadata or {}
    stats = analysis.get("stats", {})
    save_stats = stats.get("save", {})
    recalc_stats = stats.get("recalculate", {})

    parts = [
        "<!DOCTYPE html><html><head><meta charset='UTF-8'>",
        f"<title>Booking Performance Report</title>{_STYLE}</head><body>",
        "<h1>Booking Flow Performance Report</h1>",
        f"<div class='sub'>Test: {meta.get('test', 'N/A')} | "
        f"Env: {meta.get('env', 'N/A')} | "
        f"Date: {meta.get('date', datetime.now().strftime('%Y-%m-%d %H:%M'))}</div>",
    ]

    # Summary cards
    parts.append("<div style='display:flex;gap:12px;flex-wrap:wrap'>")
    if save_stats.get("count"):
        parts.append(_card("Save API Median", format_duration(save_stats.get("median"))))
        parts.append(_card("Save API Max", format_duration(save_stats.get("max"))))
    else:
        parts.append(_card("Save API", "No data"))
    if recalc_stats.get("count"):
        parts.append(_card("Recalc Median", format_duration(recalc_stats.get("median"))))
    parts.append(_card("Rounds", str(stats.get("round_count", 0))))
    parts.append(_card("Total APIs", str(stats.get("total_api_count", 0))))
    has_violations = bool(analysis.get("violations"))
    parts.append(
        _card(
            "Threshold",
            "FAIL" if has_violations else "PASS",
            "violation" if has_violations else "pass",
        )
    )
    parts.append("</div>")

    # Round details
    rounds = analysis.get("rounds", [])
    if rounds:
        parts.append("<div class='card'><h2>Round Details</h2>")
        parts.append("<table><tr><th>Round</th><th>Save API</th><th>Recalculate</th></tr>")
        for i, rd in enumerate(rounds, 1):
            parts.append(
                f"<tr><td>{i}</td>"
                f"<td>{format_duration(rd.get('save_duration_ms'))}</td>"
                f"<td>{format_duration(rd.get('recalc_duration_ms'))}</td></tr>"
            )
        parts.append("</table></div>")

    # Top 10 slowest APIs with bar chart
    slow_apis = analysis.get("slow_apis", [])
    if slow_apis:
        parts.append("<div class='card'><h2>Top 10 Slowest APIs</h2>")
        max_val = slow_apis[0]["duration"] if slow_apis else 1
        for api in slow_apis:
            pct = (api["duration"] / max_val) * 100
            color = "#d03b3b" if api["duration"] > 10000 else "#2a78d6"
            parts.append(
                f"<div class='bars'>"
                f"<span class='bar' style='width:{pct:.0f}%;background:{color}'></span>"
                f"<span class='bar-label'>{format_duration(api['duration'])} — {_esc(api['name'])}</span>"
                f"</div>"
            )
        parts.append("</div>")

    # Violations
    violations = analysis.get("violations", [])
    if violations:
        parts.append("<div class='card'><h2>Threshold Violations</h2>")
        parts.append(
            "<table><tr><th>API</th><th>Duration</th><th>Threshold</th><th>Exceeded</th></tr>"
        )
        for v in violations:
            parts.append(
                f"<tr class='violation'><td>{_esc(v['api'])}</td>"
                f"<td>{format_duration(v['duration_ms'])}</td>"
                f"<td>{format_duration(v['threshold_ms'])}</td>"
                f"<td>{format_duration(v['exceeded_by_ms'])}</td></tr>"
            )
        parts.append("</table></div>")

    parts.append("</body></html>")
    return "\n".join(parts)


def _card(label: str, value: str, css_class: str = "") -> str:
    cls = f" {css_class}" if css_class else ""
    return (
        f"<div class='card' style='min-width:140px'>"
        f"<div class='label'>{label}</div>"
        f"<div class='stat{cls}'>{value}</div></div>"
    )


def save_perf_report(
    data, output_path: str, metadata: dict | None = None, report_type: str = "page_load"
):
    """Generate and save HTML report + raw JSON data.

    Args:
        data: API list (page_load) or analysis dict (booking)
        output_path: HTML file path
        metadata: env, date, test name
        report_type: "page_load" or "booking"
    """
    meta = metadata or {}
    if report_type == "booking":
        html = generate_booking_report(data, meta)
        raw = data
    else:
        html = generate_page_load_report(data, meta)
        raw = {"apis": data}

    # Save HTML
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text(html, encoding="utf-8")

    # Save raw JSON alongside
    json_path = str(Path(output_path).with_suffix(".json"))
    Path(json_path).write_text(
        json.dumps(raw, indent=2, ensure_ascii=False, default=str), encoding="utf-8"
    )
    print(f"  Report: {output_path}")
    print(f"  Raw data: {json_path}")
