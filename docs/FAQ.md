# Frequently Asked Questions (FAQ)

## Table of Contents

- [Getting Started](#getting-started)
- [Configuration](#configuration)
- [Test Execution](#test-execution)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)
- [Advanced Topics](#advanced-topics)

---

## Getting Started

### Q: What are the system requirements?

**A:** Minimum requirements:
- Python 3.11 or higher
- 4GB RAM (8GB recommended)
- 10GB free disk space
- Modern web browser (Chrome, Firefox, or Edge)
- Docker Desktop (for Selenium Grid)

### Q: Can I run tests without Docker?

**A:** Yes! You can run tests locally:
```bash
# Install browser drivers
pip install webdriver-manager

# Run tests
pytest src/tests/
```

### Q: How long does it take to set up the framework?

**A:**
- Basic setup: 10-15 minutes
- With Docker Selenium Grid: 20-30 minutes
- Full setup with all features: 45-60 minutes

### Q: Do I need to know Python to use this framework?

**A:** Basic Python knowledge helps, but:
- Tests are written in simple, readable format
- Documentation provides examples
- Page Object Model makes tests self-documenting

---

## Configuration

### Q: How do I configure test environment?

**A:** Create `pytest.ini` from template:
```bash
cp pytest.ini.example pytest.ini
```

Edit with your values:
```ini
[pytest]
env =
    WEB_URL=https://your-app.com
    USERNAME=your_username
    PASSWORD=your_password
```

### Q: Can I use environment variables instead of pytest.ini?

**A:** Yes! Create `.env` file:
```bash
cp .env.example .env
```

Or set directly:
```bash
export WEB_URL=https://staging.example.com
export USERNAME=test_user
pytest src/tests/
```

### Q: How do I configure different browsers?

**A:** In `pytest.ini` or environment:
```ini
BROWSER=chrome    # chrome, firefox, edge
HEADLESS=true     # Run in headless mode
```

Or via command line:
```bash
pytest --browser firefox --headless
```

### Q: Can I run tests in parallel?

**A:** Yes! Use pytest-xdist:
```bash
# Auto-detect CPU cores
pytest -n auto

# Specific number of workers
pytest -n 4

# Distribute by file
pytest -n 4 --dist loadfile
```

---

## Test Execution

### Q: How do I run specific tests?

**A:** Multiple ways:

```bash
# Single test file
pytest src/tests/test_login.py

# Single test function
pytest src/tests/test_login.py::test_login_success

# Test class
pytest src/tests/test_reservation.py::TestReservationCreation

# Tests with specific marker
pytest -m smoke
pytest -m "regression and not slow"

# Tests matching pattern
pytest -k "reservation"
```

### Q: How do I run tests with different environments?

**A:**
```bash
# Staging
pytest --env=staging

# Production (be careful!)
pytest --env=production -m smoke

# Custom
pytest --env-url=https://custom.example.com
```

### Q: Can I stop tests on first failure?

**A:** Yes:
```bash
# Stop on first failure
pytest -x

# Stop after N failures
pytest --maxfail=3
```

### Q: How do I re-run failed tests?

**A:**
```bash
# Run only failed tests from last run
pytest --lf

# Run failed tests first, then all
pytest --ff
```

### Q: How do I run tests with verbose output?

**A:**
```bash
# Verbose output
pytest -v

# Extra verbose
pytest -vv

# Show print statements
pytest -s

# Show local variables on failure
pytest --tb=long
```

---

## Troubleshooting

### Q: Tests fail with "Element not found" error

**A:** Common causes and solutions:

1. **Element not loaded yet:**
```python
# Add explicit wait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(locator)
)
```

2. **Wrong locator:**
```python
# Verify locator in browser DevTools
# Update locator in *_locator.py file
```

3. **Dynamic ID/class:**
```python
# Use contains() or starts-with()
btn = (By.XPATH, "//button[contains(@id, 'submit')]")
```

### Q: WebDriver crashes with "Session not created" error

**A:**
```bash
# Check browser version matches driver version
chrome --version

# Update driver
pip install --upgrade webdriver-manager

# Or use Docker Selenium Grid
docker-compose up -d
```

### Q: Tests timeout waiting for page load

**A:** Increase timeout:
```python
# In test or conftest.py
driver.set_page_load_timeout(30)

# Or in pytest.ini
PAGE_LOAD_TIMEOUT=30
```

### Q: How do I debug failing tests?

**A:**
```bash
# Run with detailed output
pytest -vv --tb=long --capture=no

# Add screenshots on failure (already configured in conftest.py)

# Use debugger
pytest --pdb  # Start debugger on failure
pytest --trace  # Start debugger immediately
```

### Q: "StaleElementReferenceException" error

**A:** Element changed or disappeared:
```python
# Solution: Re-find element
for attempt in range(3):
    try:
        element = driver.find_element(*locator)
        element.click()
        break
    except StaleElementReferenceException:
        time.sleep(1)
```

### Q: Tests pass locally but fail in CI

**A:** Common causes:
1. **Timing issues:** Add explicit waits
2. **Environment differences:** Check config
3. **Resource limitations:** Reduce parallel workers
4. **Network issues:** Increase timeouts

---

## Best Practices

### Q: Should I use explicit or implicit waits?

**A:** Use **explicit waits**:
```python
# Good: Explicit wait
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable(locator)
)

# Avoid: Implicit wait (global)
# driver.implicitly_wait(10)  # Don't do this
```

### Q: How should I organize test data?

**A:** Use fixtures and data files:

```python
# conftest.py
@pytest.fixture
def valid_guest_data():
    return load_json("data/guest_valid.json")

# Test
def test_create_reservation(browser, valid_guest_data):
    browser.reservation.create(valid_guest_data)
```

### Q: Should tests be independent?

**A:** **Yes!** Each test should:
- Set up its own data
- Not depend on other tests
- Clean up after itself

```python
# Good: Independent
def test_reservation(browser):
    reservation_id = create_reservation()
    assert exists(reservation_id)
    delete(reservation_id)

# Bad: Dependent
def test_setup():
    create_reservation()  # Other tests depend on this

def test_verify():
    # Assumes test_setup ran
    verify_reservation()
```

### Q: How do I handle test data cleanup?

**A:** Use fixtures with cleanup:

```python
@pytest.fixture
def guest_account(browser):
    # Setup
    guest_id = browser.guest.create(test_data)
    yield guest_id

    # Teardown
    browser.guest.delete(guest_id)
```

---

## Advanced Topics

### Q: How do I implement custom pytest markers?

**A:**
```python
# Register in pytest.ini
[pytest]
markers =
    smoke: Smoke tests
    regression: Regression tests
    slow: Slow running tests

# Use in test
@pytest.mark.smoke
def test_login():
    pass
```

### Q: Can I run tests in a specific order?

**A:** Yes, using pytest-dependency:
```python
@pytest.mark.dependency()
def test_login():
    pass

@pytest.mark.dependency(depends=["test_login"])
def test_reservation():
    pass
```

### Q: How do I generate test data dynamically?

**A:** Use Faker:
```python
from faker import Faker

fake = Faker()

@pytest.fixture
def random_guest():
    return {
        "name": fake.name(),
        "email": fake.email(),
        "phone": fake.phone_number()
    }
```

### Q: How do I run tests on multiple browsers simultaneously?

**A:** Use pytest parametrize:
```python
@pytest.mark.parametrize("browser", ["chrome", "firefox", "edge"])
def test_login(browser_type):
    driver = get_driver(browser_type)
    # Test with each browser
```

### Q: Can I integrate this with CI/CD pipelines?

**A:** Yes! Framework includes:
- GitHub Actions workflows
- Docker support
- Allure reporting
- JUnit XML output

```yaml
# .github/workflows/test.yml
- name: Run tests
  run: pytest --alluredir=allure-results
```

### Q: How do I handle CAPTCHA in tests?

**A:** Framework includes ML captcha solver:
```python
from utils.captcha.captcha_helper import CaptchaTrainer

# Automatic in login page
browser.login.login(username, password)  # Solves captcha automatically

# Manual use
solver = CaptchaTrainer()
captcha_text = solver.predict_captcha("captcha.png")
```

### Q: How do I report bugs found during testing?

**A:**
1. **Create GitHub Issue:**
   - Use bug report template
   - Include test case name
   - Attach screenshots (auto-captured)
   - Include environment details

2. **Mark test as expected failure:**
```python
@pytest.mark.xfail(reason="Bug #123")
def test_feature():
    pass
```

### Q: Can I extend the framework with custom utilities?

**A:** Yes! Add to `src/utils/`:
```python
# src/utils/api_helper.py
class APIHelper:
    @staticmethod
    def get_token():
        pass

# Use in tests
from utils.api_helper import APIHelper
```

### Q: How do I contribute to the framework?

**A:**
1. Fork repository
2. Create feature branch
3. Make changes
4. Run tests
5. Submit PR

See [CONTRIBUTING.md](../CONTRIBUTING.md) for details.

---

## Performance

### Q: How can I make tests run faster?

**A:**
1. **Use session storage** (already implemented):
```python
# Login once, reuse session
DriverHelper.save_session_storages()
```

2. **Run in parallel:**
```bash
pytest -n 4
```

3. **Use headless mode:**
```bash
pytest --headless
```

4. **Reduce waits:**
```python
# Use specific waits instead of sleep()
WebDriverWait(driver, 5).until(...)
```

5. **Mark slow tests:**
```python
@pytest.mark.slow
def test_slow_operation():
    pass

# Skip slow tests
pytest -m "not slow"
```

### Q: How do I profile test performance?

**A:**
```bash
# pytest with durations
pytest --durations=10

# Show slowest tests
pytest --durations=0  # Show all
```

---

## More Questions?

- 📖 Check [Documentation](../docs/)
- 🐛 [Report Bug](https://github.com/Galen-Chu/PMS-test-automation-script/issues)
- 💬 [Discussions](https://github.com/Galen-Chu/PMS-test-automation-script/discussions)
- 📧 Contact maintainer

---

*Last updated: March 11, 2026*
