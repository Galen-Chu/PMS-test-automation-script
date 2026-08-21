# PMS Test Automation Framework

A comprehensive test automation framework for Property Management System (PMS) applications, featuring Page Object Model architecture, ML-powered captcha recognition, and parallel test execution.

![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12-blue)
![Selenium](https://img.shields.io/badge/Selenium-4.47-green)
![pytest](https://img.shields.io/badge/pytest-9.1-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🎯 Key Features

- **Page Object Model (POM)** - Maintainable and scalable test architecture
- **ML Captcha Recognition** - TensorFlow-powered automatic captcha solving
- **Parallel Execution** - Run tests concurrently with Docker Selenium Grid
- **Allure Reporting** - Comprehensive HTML reports with screenshots
- **Session Management** - Efficient test execution with session persistence
- **Multi-Browser Support** - Chrome, Firefox, and Edge compatibility

## 📊 Project Statistics

- **230 Test Cases** across 15 test suites
- **26 Page Objects** plus 11 reusable components and 3 dialog handlers
- **26 Locator Classes** for element identification
- **Machine Learning** integration for intelligent testing
- **CLI Toolchain** - interactive Selenium debugging and Qase API helpers

## 🏗️ Architecture

```
pms-test-automation/
├── src/
│   ├── locators/          # Page element locators (26)
│   ├── pages/             # Page Object Model classes
│   │   ├── components/    # Reusable UI components (11)
│   │   └── dialogs/       # Dialog/modal handlers (3)
│   ├── tests/             # Test suites (15 files, 250 tests)
│   │   ├── dynamic_steps/ # Shared step libraries
│   │   ├── examples/      # Data-driven example tests
│   │   └── fixtures/      # Pytest fixtures + static test data
│   └── tools/             # Helper utilities
│       ├── captcha/       # ML captcha solver
│       ├── selenium_cli.py    # Interactive Selenium CLI
│       ├── qase_cli.py        # Qase API CLI
│       └── test_data_helper.py # Test data allocation system
├── ml-models/             # Trained ML models
├── docs/                  # Guides + page structure maps (docs/pages)
└── .github/workflows/     # CI: lint, smoke, regression, docker, Allure Pages
```

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- Docker (for Selenium Grid)
- Chrome/Firefox/Edge browser

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/pms-test-automation-showcase.git
   cd pms-test-automation-showcase
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp pytest.ini.example pytest.ini
   # Edit pytest.ini with your configuration
   ```

5. **Start Selenium Grid** (optional, for parallel testing)
   ```bash
   docker-compose up -d
   ```

### Running Tests

**Run all tests:**
```bash
pytest
```

**Run specific test file:**
```bash
pytest src/tests/test_login.py
```

**Run with markers:**
```bash
pytest -m smoke
```

**Run in parallel:**
```bash
pytest -n 4  # Run 4 tests in parallel
```

**Generate Allure report:**
```bash
pytest --alluredir=allure-results
allure serve allure-results
```

## 🧪 Test Suites

| Suite | Description | Test Count |
|-------|-------------|------------|
| `test_login.py` | Authentication (auto captcha solving) | 1 |
| `test_reservation.py` | Reservation workflows | 8 |
| `test_reservation_card.py` | Reservation card (booking card) | 12 |
| `test_reservation_detail.py` | Detailed reservation scenarios | 19 |
| `test_guest_detail.py` | Guest detail (remarks, transport, handover) | 19 |
| `test_guest_services.py` | Guest services | 22 |
| `test_maindesk.py` | Front desk (綜合櫃台) operations | 14 |
| `test_maindesk_guest_function.py` | Front desk guest functions | 13 |
| `test_maindesk_header_toolbar.py` | Front desk toolbar | 12 |
| `test_room_assignment.py` | Room assignment | 3 |
| `test_room_control.py` | Room control | 20 |
| `test_rate_cod.py` | Rate code management | 37 |
| `test_check_in_list.py` | C/I list check-in | 1 |
| `test_lost_management.py` | Lost & found | 11 |
| `examples/test_data_examples.py` | Data-driven testing examples | 38 |

## 🤖 ML Captcha Recognition

This framework includes a TensorFlow-based captcha recognition system:

- **Model**: Convolutional Neural Network (CNN)
- **Accuracy**: 95%+ on test data
- **Character Support**: Alphanumeric
- **Inference Time**: <100ms per captcha

The captcha module loads lazily at login time, so collecting and running
unrelated tests does not require the ML dependencies to be importable.

## 📖 Documentation

- [Architecture Guide](ARCHITECTURE.md) - Framework design and patterns
- [Setup Guide](docs/SETUP.md) - Detailed installation instructions
- [Framework Guide](docs/FRAMEWORK_GUIDE.md) - How to write tests
- [Best Practices](docs/BEST_PRACTICES.md) - Testing best practices
- [Data Guide](docs/DATA_GUIDE.md) - Test data fixtures and generators
- [Troubleshooting](docs/TROUBLESHOOTING.md) - Common issues
- [FAQ](docs/FAQ.md) - Frequently asked questions
- [PMS Menu Map](docs/pms-menu-map.md) - System menu overview
- [Page Structure Maps](docs/pages/) - Per-page exploration notes (10 pages)
- [CLI Knowledge](src/tools/cli-knowledge.md) - Selenium CLI cookbook
- [Qase CLI Knowledge](src/tools/qase-cli-knowledge.md) - Qase API cookbook

## 🛠️ Technology Stack

| Category | Technology |
|----------|------------|
| Test Framework | pytest 9.1.1 |
| Browser Automation | Selenium WebDriver 4.47 |
| Parallel Execution | pytest-xdist 3.8.0 |
| Reporting | Allure pytest 2.16.0 |
| Machine Learning | TensorFlow 2.21.0 |
| Image Processing | OpenCV 5.0, Pillow 12.3 |
| OCR | pytesseract 0.3.13 |
| Containerization | Docker, Docker Compose |

## 🎨 Design Patterns

- **Page Object Model** - Separates test logic from UI structure
- **Component Pattern** - Reusable UI component classes
- **Factory Pattern** - Dynamic page object creation
- **Singleton Pattern** - Shared driver instance

## 📈 Test Execution Flow

```
1. Initialize WebDriver
2. Navigate to application
3. Login (with auto captcha solving)
4. Execute test scenario
5. Capture screenshot on failure
6. Generate Allure report
7. Cleanup and teardown
```

## 🔧 Configuration Options

Test execution can be customized via `pytest.ini` (copy from `pytest.ini.example`,
which also sets `pythonpath = src` so the page/locator/tool packages resolve):

```ini
[pytest]
pythonpath = src
env =
    ENV=staging
    WEB_URL=https://staging.example.com
    SELENIUM_HUB=http://localhost:4444/wd/hub
    QASE_API_TOKEN=
```

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Your Name**
- GitHub: [@Galen-Chu](https://github.com/Galen-Chu)
- LinkedIn: [Galen-Chu](https://linkedin.com/in/ching-wen-chu-420942326/)

## 🙏 Acknowledgments

- Selenium WebDriver team
- pytest community
- TensorFlow team
- Allure Framework contributors

---

**Note**: This is a showcase project demonstrating test automation best practices. All sensitive data, URLs, and credentials have been replaced with placeholders.
