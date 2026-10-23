# Refactoring Roadmap

Status: **Active.** Last re-baselined: 2026-10-23 (end of day), after
the A-series and the P1–P7 delivery batches landed on main.

This roadmap comes from a POM-architecture self-review (2026-09-08),
re-verified against the code on 2026-10-23. Items are candidates for
future work sessions, not commitments. Line references drift —
re-check before starting.

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
- **Locator isolation**: every page binds its locator explicitly
  (constructor injection since P1); tests contain zero selectors.
- **Two-level base** (since P2): `BasePage` (generic Selenium layer) →
  `AthenaBasePage` (PMS widgets) → pages/components/dialogs.
- **Fluent interface**: `return self` chaining throughout the page layer.
- **Allure integration at every layer**: steps, evidence-attaching asserts,
  automatic failure screenshots in `conftest.py`.
- **Session-scoped browser lifecycle** (A2+A4, 2026-10): `shared_driver` /
  `logged_in_driver` fixtures, keep-alive thread, cross-run session
  persistence, persistent Chrome profile, typed `Browser` bundle (P5).
- **Performance suite** (2026-10): `performance_monitor` /
  `perf_analyzer` / `perf_report` plus perf tests behind the `perf`
  marker, hardened 2026-10-23 (#68); CI regression excludes them
  (`-m "not perf"`).
- **ML captcha solver** with lazy import and OCR fallback (A3 retrained
  model, 5.6x faster than pytesseract); captcha image goes to the
  system temp dir, VERSION config centralized in `AppConfig` (P6).

## Item Status (2026-10-23)

| Item | Status | Issue |
|------|--------|-------|
| P1 explicit locator binding | **done** | #63 |
| P2 split BasePage into generic + app layers | **done** | #64 |
| P3 wait strategy | **in progress** — foundation + page-layer batch landed | #62 (open) |
| P4 `format_locator` rename | **done** | #67 |
| P5 fixture browser lifecycle + typed Browser | **done** | #65 |
| P6 LoginPage captcha/VERSION hardening | **done** | #66 |
| P7 naming quick wins | **done** | #61 |
| A-series cleanup (dead code, docs, credentials) | **done** | #60 |
| Performance-suite review | **done** | #68 |

## Open Items

### P3 campaign — replace sleeps with explicit waits (#62)

**Landed so far:**

- Foundation: `wait_present` / `wait_until` helpers; `has_element` is
  an explicit presence check with the implicit wait zeroed for its
  duration; `select()` / `select_date()` wait for their target.
- Batch 1 (page layer): ~45 sleeps in pages/components/dialogs
  converted — dropdown options, submenu expansion
  (`expanded_menu_item` locator), dialog readiness, filtered-option
  waits (transport waits on the combobox value). Deliberately kept:
  maindesk dropdown-filter pads, `clear_deposit_nos` toggle pads,
  login-page captcha refresh (no DOM condition), base click-retry
  backoff.

**Remaining campaign:** share_steps + dynamic_steps layer (~250
sites), then test suites one at a time (~1,000 sites), each batch
validated on the QA environment before the next. Remove the global
`implicitly_wait(10)` (conftest) only after raw `find_element` calls
are gone — the final, largest behavior change.

### A-series follow-up (user action, not code)

`verify_a3_login.py` was committed with real QA credentials (sanitized
2026-10-23, moved to `src/tools/`). The old values remain in git
history — **rotate the QA password**.

## Supplemental (Not Code, No Issue Yet)

- **Standard page-set factory**: every test still starts with
  `pages = [...]` + `DriverHelper.get_logged_in_browser(pages, path)`.
  A fixture/factory returning a standard page set would remove the
  repetition (leftover idea from P5).
- **Navigation return types**: methods currently `return self` even when
  navigating away. Convention "cross-page action returns the new page
  object" (e.g. `login() → HomePage`) would catch flow errors at call
  time. Currently this semantics lives only in `ShareSteps`.
- **ARCHITECTURE.md "Design Trade-offs" section**: document *why not*
  Screenplay, why asserts live in BasePage (Allure evidence beats "pages
  don't assert" purism), and the pytest-dependency/cache trade-off (tests
  are order-dependent by design; single-test runs need care).

## Suggested Order

1. P3 campaign batch 2 (steps layer) → batch 3+ (test suites), each
   QA-validated before the next; removing the global implicit wait last.
2. Supplemental docs section.
3. Standard page-set factory if the `pages = [...]` repetition starts
   to hurt.

## History

- 2026-10-23 (third batch): P4 rename (#67), P5 typed Browser (#65),
  P6 AppConfig/tempfile/retry (#66), P3 batch 1 page layer (#62 open),
  performance-suite review fixes (#68), CI regression excludes perf.
- 2026-10-23 (second batch): P1 and P2 delivered (#63, #64); P3
  foundation landed; dependabot #56-59 merged; roadmap issues now track
  execution per the workflow.
- 2026-10-23 (first batch): re-baselined after the A-series; P7
  delivered (#61); A-series debt cleanup (#60) — dead code, docs sync,
  credential sanitization.
- 2026-09-08: original roadmap from the POM self-review.
