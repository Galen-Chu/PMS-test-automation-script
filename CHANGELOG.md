# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- GitHub Actions CI/CD pipeline
- Docker support for containerized testing
- Comprehensive documentation suite
- ML-powered captcha recognition
- Parallel test execution support
- Upstream sync (2026-08): front desk (綜合櫃台) suite - guest
  functions, remarks, car plates, room assignment; reservation card
  refactor; transport services / booking reminders / handover items;
  pre-credit, message edit, spare parts components
- Test data infrastructure: allocation system (`tools/test_data_helper`,
  `tests/test_data.json`), fixture package with generators/builders and
  static JSON/CSV data, data-driven example suite (38 tests)
- CLI toolchain: interactive Selenium CLI, Qase API CLI, knowledge docs
- Page structure documentation (10 pages) + PMS menu map

### Changed
- Dependency modernization: pytest 8 -> 9.1.1 (with xdist 3.8,
  pytest-env 1.7, allure-pytest/commons 2.16 pair), Selenium 4.47,
  TensorFlow 2.21, numpy 2.4, scikit-learn 1.9, OpenCV 5.0,
  Pillow 12.3, black 26, mypy 2.3, pylint 4; GitHub Actions all
  bumped to current majors
- CI streamlined (~85% fewer runs): main-branch + path-filtered
  triggers, single-job regression matrix, concurrency cancellation,
  test exit codes surfaced in run summaries instead of bare `|| true`

### Fixed
- Package layout: `src/utils` renamed back to `src/tools` and
  `pythonpath = src` added - imports were unresolvable and CI had
  never actually collected a test (masked by `|| true`)
- `dymamic_steps` -> `dynamic_steps` directory typo
- Allure Pages deploy: gh-pages action v3 (retired node16) -> v4 with
  proper permissions
- Black gate: CI pinned to match requirements-dev (was unpinned and
  drifting)
- Captcha module lazily imported at login - collecting unrelated
  tests no longer requires TensorFlow
- Fixtures registered via tests conftest; faker 40 ISO-date
  compatibility in reservation factory

## [1.0.0] - 2026-03-11

### Added
- Initial release of PMS Test Automation Showcase
- Page Object Model architecture with 30+ page objects
- 23 locator classes for element identification
- 10 test suites with 163+ test cases
- TensorFlow-based captcha recognition system
- Docker Selenium Grid configuration
- Allure reporting integration
- Session management for optimized test execution
- Comprehensive documentation (README, ARCHITECTURE, guides)
- Configuration templates (pytest.ini.example, .env.example)
- CI/CD workflow with GitHub Actions
- Code quality checks (pylint, black, bandit)
- Multi-browser support (Chrome, Firefox, Edge)
- Parallel execution capability

### Security
- All sensitive data sanitized from codebase
- Configuration uses environment variables
- No credentials or URLs in source code
- Security scanning in CI pipeline

### Documentation
- README.md with project overview
- ARCHITECTURE.md with design patterns
- docs/SETUP.md with installation guide
- docs/FRAMEWORK_GUIDE.md with usage examples
- docs/BEST_PRACTICES.md with testing guidelines
- CONTRIBUTING.md with contribution guidelines

## [0.1.0] - 2026-03-11

### Added
- Initial project structure
- Basic Page Object Model implementation
- Core test framework setup
- Configuration management

---

## Version History

- **1.0.0** - First public release with complete framework
- **0.1.0** - Initial development version

## Upcoming Features

### [1.1.0] - Planned
- API testing support
- Visual regression testing
- Performance testing integration
- Mobile testing support
- Enhanced reporting with historical trends

### [1.2.0] - Planned
- AI-powered test generation
- Self-healing tests
- Advanced parallel execution strategies
- Cloud browser testing integration

---

[Unreleased]: https://github.com/Galen-Chu/pms-test-automation-showcase/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/Galen-Chu/pms-test-automation-showcase/releases/tag/v1.0.0
[0.1.0]: https://github.com/Galen-Chu/pms-test-automation-showcase/releases/tag/v0.1.0
