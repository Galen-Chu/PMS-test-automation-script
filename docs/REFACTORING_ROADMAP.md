# Refactoring Roadmap

Status: **Active.** Last re-baselined: 2026-10-23, after the A-series
(session fixtures, A3 captcha model, performance suite) landed on main.

This roadmap comes from a POM-architecture self-review (2026-09-08),
re-verified against the code on 2026-10-23. Items are candidates for
future work sessions, not commitments. Each item is self-contained so a
session can pick one, decide, and deliver it independently. Line
references drift — re-check before starting.

## Workflow (agreed 2026-09-08)

No schedule is committed; issues are intentionally **not** opened in
advance. When development on an item begins, the first action of that
session is:

1. Open one GitHub issue per item being started (label: `refactoring`),
   with the matching section of this file linked in the issue body.
2. Track execution state in the issues — this file stays the overview
   and is updated only when priorities, sequencing, or item status
   change.
3. Close issues via commit/PR references (`closes #N`).

## What Already Works Well (Do Not Regress)

- **Three-layer architecture**: tests → business steps (`share_steps.py`) →
  page objects. The steps layer keeps multi-page flows out of both tests
  and pages.
- **Component pattern**: 11 components + 3 dialogs (canonical copies in
  `pages/components/` and `pages/dialogs/`; stale root-level duplicates
  removed 2026-10-07).
- **Locator isolation**: locator classes mirror page objects; tests
  contain zero selectors.
- **Fluent interface**: `return self` chaining throughout the page layer.
- **Allure integration at every layer**: steps, evidence-attaching asserts,
  automatic failure screenshots in `conftest.py`.
- **Session-scoped browser lifecycle** (A2+A4, 2026-10): `shared_driver` /
  `logged_in_driver` fixtures, keep-alive thread, cross-run session
  persistence, persistent Chrome profile. Login happens at most once per
  session.
- **Performance suite** (2026-10): `performance_monitor` /
  `perf_analyzer` / `perf_report` plus perf tests behind the `perf` marker.
- **ML captcha solver** with lazy import and OCR fallback (A3 retrained
  model, 5.6x faster than pytesseract).

## Item Status (2026-10-23)

| Item | Status | Remaining |
|------|--------|-----------|
| P1 explicit locator binding | **done** 2026-10-23 | #63 |
| P2 split BasePage into generic + app layers | **done** 2026-10-23 | #64 |
| P3 wait strategy | in progress | #62 — foundation landed; ~1,300 `sleep()` sites remain |
| P4 `format_locator` | **done** via A-series | optional rename `formator_locator` → `format_locator` |
| P5 fixture browser lifecycle | **mostly done** via A2+A4 | typed `Browser` class; per-test `pages=[...]` boilerplate |
| P6 LoginPage captcha/VERSION | partial | `image.png` in CWD; 30-retry magic; VERSION branching |
| P7 naming quick wins | **done** 2026-10-23 | — |
| A1 follow-ups (below) | open | performance-suite review |

## Open Items

### P3. Wait strategy: replace sleeps, stop switching implicit waits

**Foundation landed 2026-10-23 (#62 stays open):** `wait_present`
helper added; `has_element` is now an explicit presence check with the
implicit wait zeroed for its duration; `select()` / `select_date()`
wait for their target element instead of fixed sleeps. Needs a QA-run
smoke before the campaign scales.

**Remaining campaign:** convert the ~1,300 `sleep()` call sites that
mask real conditions, one page/suite at a time with QA-environment
validation; remove the global `implicitly_wait(10)` (conftest) only
after raw `find_element` calls are gone — that is the final, largest
behavior change.

### P5 (remainder). Typed Browser + de-boilerplated tests

Delivered by A2+A4: session-scoped fixtures, one login per run,
teardown owned by `shared_driver`. Still open:

- `get_logged_in_browser` builds the attribute bag via
  `type("Expando", (object,), ...)` (`driver_helper.py`) — no IDE
  completion, no type checking. Replace with a small typed `Browser`
  class (dataclass holding named page attributes).
- Every test still starts with `pages = [...]` +
  `DriverHelper.get_logged_in_browser(pages, path)`. Consider a fixture
  or factory that returns a standard page set so most tests stop
  repeating the list.

### P6 (remainder). LoginPage captcha/VERSION hardening

Delivered by A-series: `_solve_captcha` extracted (ML-first, OCR
fallback), URL-based login-success detection. Still open:

- `captcha_screenshot` writes `image.png` to the working directory
  (`login_page.py`) — use `tempfile`.
- The 30-attempt retry cap is a magic number embedded in the page;
  move the retry policy next to the solving strategy.
- `int(os.getenv("VERSION")) >= 130` branching (`login_page.py:33`)
  should collapse into one config object with a sane failure mode when
  VERSION is unset (currently a bare TypeError).

### P4 (remainder). Optional rename

`formator_locator` → `format_locator` while touching every call site,
or alias first and migrate later. The `literal_eval` round-trip itself
is already gone (A-series encoding fix, 2026-10).

## A-series Follow-ups

- **Performance-suite review**: `performance_monitor.py`,
  `perf_analyzer.py`, `perf_report.py`, `session_persistence.py`
  (~800 lines) and the two perf test files landed 2026-10-21 without an
  architecture/quality pass. Review thread-safety of the injected JS
  hooks, report generation determinism, and whether perf tests should
  be excluded from default runs (`-m "not perf"`).
- **QA credential exposure**: `verify_a3_login.py` was committed with
  real QA credentials (sanitized 2026-10-23, moved to `src/tools/`).
  The old values remain in git history — rotate the QA password.
- Done on 2026-10-23: dead `create_web_browser` removed; docs synced to
  the fixture lifecycle; P7 naming cleanups.

## Supplemental (Documentation, Not Code)

- **Navigation return types**: methods currently `return self` even when
  navigating away. Convention "cross-page action returns the new page
  object" (e.g. `login() → HomePage`) would catch flow errors at call
  time. Currently this semantics lives only in `ShareSteps`.
- **ARCHITECTURE.md "Design Trade-offs" section**: document *why not*
  Screenplay, why asserts live in BasePage (Allure evidence beats "pages
  don't assert" purism), and the pytest-dependency/cache trade-off (tests
  are order-dependent by design; single-test runs need care). These are
  the questions interviewers ask; answering them in the doc turns the
  architecture guide into a narrative.

## Suggested Order

P3 campaign (suite-by-suite, QA-validated) → P5 remainder → P6
remainder → P4 rename → supplements, with the performance-suite review
slotted whenever convenient. Each step lands green on CI before the
next begins.

## History

- 2026-10-23 (second batch): P1 and P2 delivered (#63, #64); P3
  foundation landed (#62 open for the campaign); dependabot #56-59
  merged; roadmap issues now track execution per the workflow.
- 2026-10-23: re-baselined. P4 core + most of P5 + part of P6 landed via
  the A-series; P7 delivered (commit ceb051e); A-series debt cleanup
  (dead code, docs sync, credential sanitization) done.
- 2026-09-08: original roadmap from the POM self-review.
