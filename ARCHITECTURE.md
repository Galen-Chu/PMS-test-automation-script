# Architecture Guide

This document provides a comprehensive overview of the PMS Test Automation Framework architecture, design patterns, and implementation decisions.

## Table of Contents

- [Overview](#overview)
- [Design Patterns](#design-patterns)
- [Project Structure](#project-structure)
- [Core Components](#core-components)
- [Data Flow](#data-flow)
- [Testing Strategy](#testing-strategy)

## Overview

The framework is built using the **Page Object Model (POM)** pattern, which separates test logic from UI structure. This architecture provides:

- **Maintainability**: UI changes only require updates in one place
- **Reusability**: Page objects can be reused across multiple tests
- **Readability**: Tests read like business requirements
- **Reliability**: Centralized element locators reduce fragility

## Design Patterns

### 1. Page Object Model (POM)

Each page in the application has a corresponding Page Object class:

```python
class LoginPage(BasePage):
    def login(self, username, password):
        """Perform login operation"""
        self.input(self.locator.input_username, username)
        self.input(self.locator.input_password, password)
        self.click(self.locator.btn_login)
        return self
```

**Benefits:**
- Encapsulates UI operations
- Single source of truth for page interactions
- Easy to maintain when UI changes

### 2. Component Pattern

Reusable UI components are separated from full pages:

```
pages/
├── components/
│   ├── header_component.py
│   ├── panel_component.py
│   └── dialog_component.py
└── dialogs/
    └── confirmation_dialog.py
```

**Use Case:** Headers, footers, and panels appear on multiple pages.

### 3. Locator Pattern

Element locators are separated into dedicated classes:

```python
class LoginLocator:
    input_username = (By.XPATH, "//input[@id='username']")
    input_password = (By.XPATH, "//input[@id='password']")
    btn_login = (By.XPATH, "//button[@type='submit']")
```

**Benefits:**
- Centralized element definitions
- Easy to update selectors
- Clear separation of concerns

### 4. Inheritance Pattern

Base classes provide common functionality:

```python
class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.locator = self._get_locator()

    def click(self, locator):
        """Generic click with retry logic"""
        # Implementation...

    def input(self, locator, value):
        """Generic input method"""
        # Implementation...
```

**Hierarchy:**
```
BasePage
├── LoginPage
├── HomePage
├── ReservationPage
└── ...
```

### 5. Factory Pattern

Dynamic page object creation via DriverHelper:

```python
def create_web_browser(pages):
    driver = webdriver.Chrome()
    web = type("Expando", (object,), {})()

    for page in pages:
        page_name = decamelize(page.__name__)
        web[page_name] = page(driver)

    return web
```

## Project Structure

```
pms-test-automation-showcase/
│
├── src/
│   ├── locators/           # Element locators
│   │   ├── base_locator.py
│   │   ├── login_locator.py
│   │   └── ...
│   │
│   ├── pages/              # Page objects
│   │   ├── base_page.py
│   │   ├── login_page.py
│   │   ├── components/     # Reusable components
│   │   └── dialogs/        # Dialog handlers
│   │
│   ├── tests/              # Test suites
│   │   ├── conftest.py     # Pytest configuration
│   │   ├── test_login.py
│   │   ├── dymamic_steps/  # Dynamic test steps
│   │   └── ...
│   │
│   └── tools/ # Utility modules
│       ├── driver_helper.py
│       ├── date_helper.py
│       ├── random_helper.py
│       └── captcha/        # ML captcha solver
│           └── captcha_helper.py
│
├── ml-models/              # Trained ML models
│   ├── captcha_model.keras
│   └── char_mappings.pkl
│
├── config/                 # Configuration templates
│   └── README.md
│
├── docs/                   # Documentation
│   ├── examples/
│   └── images/
│
├── reports/                # Test reports
│
├── pytest.ini.example      # Pytest configuration template
├── requirements.txt        # Python dependencies
├── docker-compose.yml      # Selenium Grid setup
└── README.md               # Project documentation
```

## Core Components

### 1. DriverHelper

Manages WebDriver lifecycle and session storage:

```python
class DriverHelper:
    @staticmethod
    def create_web_browser(pages):
        # Create driver
        # Load session storage (for faster testing)
        # Initialize page objects
        # Return web object with all pages

    @staticmethod
    def save_session_storages():
        # Persist session data for reuse
```

**Features:**
- Session persistence to avoid repeated logins
- Multi-browser support
- Selenium Grid integration

### 2. BasePage

Foundation class for all page objects:

```python
class BasePage:
    # Element interactions
    def click(locator)
    def input(locator, value)

    # Assertions
    def assert_data(title, real, expect)
    def assert_data_in_list(title, reals, expect)

    # Utilities
    def screenshot(file_name)
    def sleep(seconds)

    # Framework-specific methods
    def search()
    def select(field, value)
    def toolbar_item_enabled(item, panel=None)
```

### 3. CaptchaHelper

ML-powered captcha recognition:

```python
class CaptchaTrainer:
    def load_data(data_path)
    def build_model()          # CNN architecture
    def train_model()          # Train and save model
    def predict_captcha(image) # Predict captcha text
```

**Architecture:**
- Input: 160x60 grayscale image
- 3 Conv2D layers with pooling
- Dropout for regularization
- 4 output layers (one per character)
- Output: 4-character string

### 4. Test Configuration

pytest configuration with environment variables:

```python
# conftest.py
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Capture screenshot on failure
    # Attach to Allure report
```

## Data Flow

### Test Execution Flow

```
┌─────────────────┐
│  Test Starts    │
└────────┬────────┘
         │
         v
┌─────────────────┐
│ Initialize      │
│ WebDriver       │
└────────┬────────┘
         │
         v
┌─────────────────┐
│ Navigate to     │
│ Application     │
└────────┬────────┘
         │
         v
┌─────────────────┐      ┌──────────────┐
│ Login Page      │─────>│ Captcha      │
│                 │      │ Recognition  │
└────────┬────────┘      └──────────────┘
         │
         v
┌─────────────────┐
│ Execute Test    │
│ Scenario        │
└────────┬────────┘
         │
         v
    ┌────┴────┐
    │ Success?│
    └────┬────┘
         │
    ┌────┴────┐
    │         │
   Yes        No
    │         │
    v         v
 ┌─────┐  ┌──────────────┐
 │Next │  │Screenshot &  │
 │Test │  │Attach Report │
 └─────┘  └──────┬───────┘
                 │
                 v
         ┌──────────────┐
         │ Generate     │
         │ Allure Report│
         └──────────────┘
```

### Page Object Interaction Flow

```
Test File
    │
    ├──> LoginPage.login(username, password)
    │         │
    │         ├──> Input username (using LoginLocator)
    │         ├──> Input password (using LoginLocator)
    │         ├──> Click login button
    │         └──> Return HomePage object
    │
    ├──> HomePage.navigate_to_reservations()
    │         │
    │         └──> Click reservations menu
    │
    └──> ReservationPage.create_reservation(data)
              │
              ├──> Fill form fields
              ├──> Click submit
              └──> Assert success message
```

## Testing Strategy

### Test Pyramid

```
        ┌──────────────┐
        │   E2E Tests  │  <- 10%
        └──────────────┘
      ┌────────────────────┐
      │  Integration Tests │  <- 30%
      └────────────────────┘
    ┌──────────────────────────┐
    │    Functional Tests      │  <- 60%
    └──────────────────────────┘
```

### Test Categories

1. **Smoke Tests** (`@pytest.mark.smoke`)
   - Critical path validation
   - Login, basic navigation
   - Run on every commit

2. **Regression Tests** (`@pytest.mark.regression`)
   - Full feature coverage
   - Run nightly

3. **Integration Tests**
   - Multi-module interactions
   - End-to-end workflows

### Parallel Execution

Using pytest-xdist for concurrent execution:

```bash
# Run 4 workers in parallel
pytest -n 4

# Distribute by file
pytest -n 4 --dist loadfile

# Distribute by test
pytest -n 4 --dist loadscope
```

**Best Practices:**
- Use `pytest-dependency` for test ordering
- Isolate test data between tests
- Use session storage for efficiency
- Clean up test data after execution

### Dependency Management

```python
@pytest.mark.dependency(depends=["test_login"])
def test_reservation():
    # Only runs if test_login passes
    pass
```

## Error Handling

### Retry Logic

Built-in retry for flaky elements:

```python
def click(self, locator, retries=5, delay=1):
    for attempt in range(retries):
        try:
            element = self.driver.find_element(*locator)
            element.click()
            return
        except (ElementClickInterceptedException,
                StaleElementReferenceException) as e:
            if attempt < retries - 1:
                sleep(delay)
            else:
                raise
```

### Screenshot on Failure

Automatic screenshot capture:

```python
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        allure.attach(driver.get_screenshot_as_png(),
                     name="Failure Screenshot",
                     attachment_type=allure.attachment_type.PNG)
```

## Performance Optimization

### Session Storage Persistence

```python
# First test: Login
driver.get(login_url)
# ... perform login ...
DriverHelper.save_session_storages()

# Subsequent tests: Skip login
session_data = load_session_storages()
driver.execute_script(f"sessionStorage.setItem('{key}', '{value}');")
driver.get(app_url)  # Already logged in!
```

**Impact:**
- Reduces test time by 60-70%
- Avoids repeated captcha solving
- Minimizes authentication overhead

### Lazy Loading

Page objects are created on-demand:

```python
# Only create needed pages
web = DriverHelper.create_web_browser([
    LoginPage,
    ReservationPage
])

# Other pages not instantiated
```

## Best Practices

1. **Single Responsibility**: Each page object handles one page
2. **DRY (Don't Repeat Yourself)**: Common methods in BasePage
3. **Meaningful Names**: `create_reservation()` not `test_01()`
4. **Assertions in Tests**: Keep assertions in test files, not page objects
5. **Independent Tests**: Each test should be self-contained
6. **Explicit Waits**: Use explicit waits over implicit waits
7. **Data Management**: Use fixtures for test data

## Future Enhancements

- [ ] API testing integration
- [ ] Visual regression testing
- [ ] Performance testing hooks
- [ ] Mobile testing support
- [ ] AI-powered test generation
- [ ] Enhanced parallel execution strategies

---

For more details, see:
- [Setup Guide](docs/SETUP.md)
- [Framework Guide](docs/FRAMEWORK_GUIDE.md)
- [Best Practices](docs/BEST_PRACTICES.md)
