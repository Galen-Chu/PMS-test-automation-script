# PMS Test Automation Framework

A comprehensive test automation framework for Property Management System (PMS) applications, featuring Page Object Model architecture, ML-powered captcha recognition, and parallel test execution.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Selenium](https://img.shields.io/badge/Selenium-4.32-green)
![pytest](https://img.shields.io/badge/pytest-8.3-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🎯 Key Features

- **Page Object Model (POM)** - Maintainable and scalable test architecture
- **ML Captcha Recognition** - TensorFlow-powered automatic captcha solving
- **Parallel Execution** - Run tests concurrently with Docker Selenium Grid
- **Allure Reporting** - Comprehensive HTML reports with screenshots
- **Session Management** - Efficient test execution with session persistence
- **Multi-Browser Support** - Chrome, Firefox, and Edge compatibility

## 📊 Project Statistics

- **163+ Test Cases** across 10 test suites
- **25+ Page Objects** with reusable components
- **23 Locator Classes** for element identification
- **Machine Learning** integration for intelligent testing

## 🏗️ Architecture

```
pms-test-automation-showcase/
├── src/
│   ├── locators/          # Page element locators
│   ├── pages/             # Page Object Model classes
│   │   ├── components/    # Reusable UI components
│   │   └── dialogs/       # Dialog/modal handlers
│   ├── tests/             # Test suites
│   │   └── dymamic_steps/ # Dynamic test steps
│   └── tools/ # Helper utilities
│       └── captcha/       # ML captcha solver
├── ml-models/             # Trained ML models
├── config/                # Configuration templates
├── docs/                  # Documentation
└── reports/               # Test reports
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
| `test_login.py` | Authentication tests | 1 |
| `test_reservation.py` | Reservation workflow tests | 15+ |
| `test_guest_detail.py` | Guest management tests | 25+ |
| `test_maindesk.py` | Front desk operations | 20+ |
| `test_room_control.py` | Room management tests | 18+ |
| `test_guest_services.py` | Guest services tests | 20+ |
| `test_rate_cod.py` | Rate code management | 15+ |
| `test_reservation_card.py` | Reservation card tests | 12+ |
| `test_reservation_detail.py` | Detailed reservation tests | 30+ |
| `test_lost_management.py` | Lost & found tests | 7+ |

## 🤖 ML Captcha Recognition

This framework includes a TensorFlow-based captcha recognition system:

- **Model**: Convolutional Neural Network (CNN)
- **Accuracy**: 95%+ on test data
- **Character Support**: Alphanumeric
- **Inference Time**: <100ms per captcha

See [ML Model Documentation](docs/ML_MODEL.md) for training details.

## 📖 Documentation

- [Architecture Guide](docs/ARCHITECTURE.md) - Framework design and patterns
- [Setup Guide](docs/SETUP.md) - Detailed installation instructions
- [Framework Guide](docs/FRAMEWORK_GUIDE.md) - How to write tests
- [Best Practices](docs/BEST_PRACTICES.md) - Testing best practices

## 🛠️ Technology Stack

| Category | Technology |
|----------|------------|
| Test Framework | pytest 8.3.4 |
| Browser Automation | Selenium WebDriver 4.32 |
| Parallel Execution | pytest-xdist 3.6.1 |
| Reporting | Allure pytest 2.13.5 |
| Machine Learning | TensorFlow 2.20.0 |
| Image Processing | OpenCV 4.11, Pillow 11.2 |
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

Test execution can be customized via `pytest.ini`:

```ini
[pytest]
env =
    ENV=staging
    WEB_URL=https://staging.example.com
    SELENIUM_HUB=http://localhost:4444/wd/hub
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
