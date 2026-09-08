# Refactoring Roadmap

Status: **Proposed — not scheduled.** Last reviewed: 2026-09-08.

This roadmap comes from a POM-architecture self-review of the framework
(2026-09-08). Items are candidates for future work sessions, not commitments.
Each item is self-contained so a session can pick one, decide, and deliver it
independently. Line references are as of the review date and will drift.

## What Already Works Well (Do Not Regress)

These are the framework's strengths; refactors must preserve them:

- **Three-layer architecture**: tests → business steps (`share_steps.py`) →
  page objects. The steps layer keeps multi-page flows out of both tests
  and pages.
- **Component pattern**: 11 components + 3 dialogs separate shared widgets
  (header, tip, panels) from full-page objects.
- **Locator isolation**: 27 locator classes mirror 27 page objects; tests
  contain zero selectors.
- **Fluent interface**: `return self` chaining throughout the page layer.
- **Allure integration at every layer**: steps, evidence-attaching asserts,
  automatic failure screenshots in `conftest.py`.
- **Real-world hardening**: sessionStorage save/restore for login reuse,
  local/remote (Selenium Grid) driver switching, ML captcha solver with
  lazy import, xdist groups + pytest-dependency for stateful flows.

## Priority Items

### P1. Explicit locator binding (replace `globals()` reflection)

- **Problem**: `BasePage.__init__` (`src/pages/base_page.py:47-51`) resolves
  the locator class via `globals()[f"{prefix}Locator"]`, which forces
  `base_page.py:16-41` to import all 27 locator modules. BasePage becomes a
  god module; a page/locator rename fails at **runtime**, not import time.
- **Approach**: each page declares its own locator explicitly — constructor
  injection (`super().__init__(driver, LoginLocator())`) or a class
  attribute. Delete the 27 imports and the reflection.
- **Effort**: M (mechanical, 27 files + base, low risk).
- **Value**: removes the largest coupling smell; best single refactor story.

### P2. Split BasePage into generic + application layers

- **Problem**: `base_page.py` (12 KB) mixes generic Selenium wrappers
  (click/input/waits) with PMS-specific widgets (toolbar, ikey, calendar,
  `select`), from `base_page.py:154` onward.
- **Approach**: two-level base — `BasePage` (generic) → `AthenaBasePage`
  (app widgets: toolbar/ikey/date) → concrete pages. Components and dialogs
  inherit from the app level.
- **Effort**: M. Best done after P1.

### P3. Wait strategy: replace sleeps, stop switching implicit waits

- **Problem**: fixed `sleep()` in base methods (`select()` at
  `base_page.py:159-165`, `select_date()` at `:303-317`) and tests
  (`.sleep(10)`); `has_element` (`base_page.py:97-105`) toggles
  `implicitly_wait` 2↔10 — mixing implicit and explicit waits is a
  documented Selenium anti-pattern that makes `WebDriverWait` timing
  unpredictable.
- **Approach**: standardize on explicit waits (`wait_visible` /
  `wait_clickable` already exist but are underused); replace `has_element`'s
  implicit-wait switching with a short explicit presence check; audit
  `sleep()` call sites and convert those that mask real conditions.
- **Effort**: M, incremental (one page/suite at a time, CI-verifiable).
- **Value**: stability + the most-asked interview topic on this codebase.

### P4. `format_locator`: replace `literal_eval` string round-trip

- **Problem**: `formator_locator` (`base_page.py:54-55`) does
  `literal_eval(str(locator) % values)` — breaks on quotes/`%` inside
  values, obscure failures.
- **Approach**: format the selector string first, then build the tuple:
  `def format_locator(locator, *values): return (locator[0], locator[1] % values)`.
  Rename `formator_locator` → `format_locator` while touching every call
  site (or alias first, migrate later).
- **Effort**: S-M.

### P5. Fixture-based browser lifecycle

- **Problem**: every test starts with `pages = [...]` +
  `DriverHelper.create_web_browser(pages)` boilerplate (e.g.
  `test_reservation.py:26-27`); driver lifecycle runs through the
  `DriverHelper.DRIVER` class global; the dynamic `type("Expando", ...)`
  attribute bag has no IDE completion; parameter name `sys`
  (`driver_helper.py`) shadows the `sys` module.
- **Approach**: a `browser` pytest fixture in `conftest.py` that yields a
  standard page set; tests request `web` and never see `DriverHelper`.
  Replace the Expando with a small typed `Browser` class.
- **Effort**: M (touches all 17 test files mechanically).
- **Value**: removes the most visible daily friction; cleanest demo of
  fixture-driven design.

### P6. LoginPage: extract captcha solving, centralize VERSION branching

- **Problem**: `login_page.py:19-47` embeds the OCR/TF retry loop (magic
  30-attempt cap), writes `image.png` to the working directory, and calls
  pytesseract inline. `int(os.getenv("VERSION")) >= 130` branching is
  duplicated in three places — page, locator (evaluated at **import**
  time), and `driver_helper.py`.
- **Approach**: page exposes `captcha_image_bytes()` and
  `input_captcha(text)`; the solving strategy moves to `tools/captcha`
  (already exists) with `tempfile` instead of CWD files. VERSION logic
  collapses into one config object.
- **Effort**: M.

### P7. Naming and copy-paste cleanup (quick wins, ≤ 1 hour total)

- `get_by_data_field` (`base_page.py:263-266`) is a copy of
  `click_by_data_field` — a **getter that clicks**. Fix to actually read.
- Typo: `get_diplaying_items_count` → `get_displaying_items_count`
  (`base_page.py:285`).
- Numbered variants leak missing abstraction: `click_target_ikey/_2/_3`
  (`base_page.py:243-256`), `click_toolbar_item/_2` (`:189-207`) —
  parameterize by panel/grid or give semantic names.

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

Quick wins (P7) → P3 → P1 → P2 → P4 → P5 → P6 → supplements.
Each step lands green on CI before the next begins.
