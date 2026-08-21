# Troubleshooting Guide

Comprehensive troubleshooting guide for common issues and solutions.

## Table of Contents

- [Installation Issues](#installation-issues)
- [Configuration Issues](#configuration-issues)
- [Test Execution Issues](#test-execution-issues)
- [WebDriver Issues](#webdriver-issues)
- [Docker Issues](#docker-issues)
- [CI/CD Issues](#cicd-issues)
- [Performance Issues](#performance-issues)

---

## Installation Issues

### Issue: Python version incompatible

**Error:**
```
ERROR: Package 'pytest' requires Python >=3.8 but you have Python 3.7
```

**Solution:**
```bash
# Check Python version
python --version

# Install Python 3.12
# Windows: Download from python.org
# macOS: brew install python@3.12
# Linux: sudo apt install python3.12

# Create virtual environment with correct version
python3.12 -m venv venv
source venv/bin/activate
```

### Issue: pip install fails with permission error

**Error:**
```
ERROR: Could not install packages due to an OSError: [Errno 13] Permission denied
```

**Solution:**
```bash
# Option 1: Use virtual environment (recommended)
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Option 2: User install
pip install --user -r requirements.txt

# Option 3: Use --break-system-packages flag (not recommended)
pip install --break-system-packages -r requirements.txt
```

### Issue: TensorFlow installation fails

**Error:**
```
ERROR: Could not find a version that satisfies the requirement tensorflow
```

**Solution:**
```bash
# For macOS with M1/M2
pip install tensorflow-macos tensorflow-metal

# For Linux/Windows
pip install tensorflow==2.20.0

# If still fails, install without ML dependencies
pip install -r requirements.txt --no-deps
pip install selenium pytest allure-pytest
```

### Issue: Chromedriver version mismatch

**Error:**
```
selenium.common.exceptions.SessionNotCreatedException: Message: session not created: This version of ChromeDriver only supports Chrome version 120
```

**Solution:**
```bash
# Option 1: Use webdriver-manager (auto-update)
pip install webdriver-manager

# Option 2: Use Docker Selenium Grid
docker-compose up -d

# Option 3: Manually update driver
# Download correct version from:
# https://chromedriver.chromium.org/downloads
```

---

## Configuration Issues

### Issue: Environment variables not loaded

**Error:**
```
KeyError: 'WEB_URL'
```

**Solution:**
```bash
# Check if pytest.ini exists
ls pytest.ini

# If not, create from template
cp pytest.ini.example pytest.ini

# Or set environment variables
export WEB_URL=https://example.com
export USERNAME=test_user
export PASSWORD=test_password
```

### Issue: pytest.ini not being read

**Error:**
Tests don't use configured values

**Solution:**
```bash
# Verify pytest.ini location (must be in project root)
ls pytest.ini

# Check file syntax
cat pytest.ini

# Verify env section
pytest --version
pytest --co  # List tests to verify config
```

### Issue: Allure report not generated

**Error:**
```
'allure' is not recognized as an internal or external command
```

**Solution:**
```bash
# Install Allure CLI
# macOS
brew install allure

# Windows (with Scoop)
scoop install allure

# Or use npm
npm install -g allure-commandline

# Generate report
pytest --alluredir=allure-results
allure serve allure-results
```

---

## Test Execution Issues

### Issue: No tests collected

**Error:**
```
collected 0 items
```

**Solution:**
```bash
# Check test file naming (must start with test_ or end with _test.py)
ls src/tests/

# Verify test function naming (must start with test_)
grep -r "def test_" src/tests/

# Check pytest discovery
pytest --co --collect-only

# Run with explicit path
pytest src/tests/test_login.py
```

### Issue: Import errors in tests

**Error:**
```
ModuleNotFoundError: No module named 'pages'
```

**Solution:**
```bash
# Ensure you're in project root
pwd

# Check PYTHONPATH
echo $PYTHONPATH

# Set PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

# Or use pytest pythonpath
# pytest.ini:
[pytest]
pythonpath = . src
```

### Issue: Tests timeout

**Error:**
```
TimeoutError: Message: timeout: Timed out receiving message from renderer
```

**Solution:**
```python
# Increase timeout in pytest.ini
PAGE_LOAD_TIMEOUT=60
IMPLICIT_WAIT=10

# Or in code
driver.set_page_load_timeout(60)
driver.implicitly_wait(10)

# Use explicit waits instead
WebDriverWait(driver, 30).until(
    EC.presence_of_element_located(locator)
)
```

### Issue: Element not interactable

**Error:**
```
selenium.common.exceptions.ElementNotInteractableException: Message: element not interactable
```

**Solution:**
```python
# Wait for element to be clickable
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable(locator)
).click()

# Scroll element into view
element = driver.find_element(*locator)
driver.execute_script("arguments[0].scrollIntoView();", element)
element.click()

# Use JavaScript click
driver.execute_script("arguments[0].click();", element)
```

---

## WebDriver Issues

### Issue: WebDriverException: unknown error

**Error:**
```
selenium.common.exceptions.WebDriverException: Message: unknown error: Chrome failed to start
```

**Solution:**
```bash
# Check Chrome is installed
google-chrome --version  # Linux
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version  # macOS

# Add Chrome options
options = ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--headless')  # For CI

# Use Docker Selenium Grid instead
docker-compose up -d
```

### Issue: StaleElementReferenceException

**Error:**
```
selenium.common.exceptions.StaleElementReferenceException: Message: stale element reference
```

**Solution:**
```python
# Re-find element before interaction
def click_with_retry(driver, locator, max_attempts=3):
    for attempt in range(max_attempts):
        try:
            element = driver.find_element(*locator)
            element.click()
            return
        except StaleElementReferenceException:
            if attempt == max_attempts - 1:
                raise
            time.sleep(0.5)

# Use explicit wait
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(locator)
)
```

### Issue: Session not created (browser crash)

**Error:**
```
selenium.common.exceptions.SessionNotCreatedException: Message: session not created from tab crashed
```

**Solution:**
```python
# Add Chrome options
options = ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.add_argument('--disable-software-rasterizer')

# Increase shared memory (Docker)
docker run --shm-size=2g ...
```

### Issue: Certificate error

**Error:**
```
NET::ERR_CERT_AUTHORITY_INVALID
```

**Solution:**
```python
# Ignore certificate errors
options = ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')

# For Selenium Grid
capabilities = DesiredCapabilities.CHROME
capabilities['acceptSslCerts'] = True
```

---

## Docker Issues

### Issue: Docker Compose fails to start

**Error:**
```
ERROR: Couldn't connect to Docker daemon
```

**Solution:**
```bash
# Start Docker Desktop (Windows/macOS)
# Or Docker service (Linux)
sudo systemctl start docker

# Check Docker status
docker ps

# Restart Docker
# Windows/macOS: Restart Docker Desktop
# Linux:
sudo systemctl restart docker
```

### Issue: Selenium Grid not responding

**Error:**
```
urllib.error.URLError: <urlopen error [Errno 111] Connection refused>
```

**Solution:**
```bash
# Check if containers are running
docker-compose ps

# Check logs
docker-compose logs selenium-hub

# Restart Selenium Grid
docker-compose restart

# Or recreate
docker-compose down
docker-compose up -d

# Wait for Grid to be ready
timeout=60
while ! curl -s http://localhost:4444/status | grep -q '"ready":true'; do
  timeout=$((timeout-1))
  if [ $timeout -eq 0 ]; then
    echo "Selenium Grid not ready"
    exit 1
  fi
  sleep 1
done
```

### Issue: Container out of memory

**Error:**
```
Container killed due to memory usage
```

**Solution:**
```yaml
# docker-compose.yml
services:
  chrome:
    shm_size: '2gb'
    deploy:
      resources:
        limits:
          memory: 4G
```

```bash
# Or increase Docker memory limit
# Docker Desktop -> Settings -> Resources -> Memory
```

### Issue: VNC not accessible

**Error:**
Cannot access VNC viewer

**Solution:**
```bash
# Check VNC port mapping
docker-compose ps

# Verify ports in docker-compose.yml
ports:
  - "5900:5900"  # Chrome VNC
  - "5901:5901"  # Edge VNC
  - "5902:5902"  # Firefox VNC

# Connect with VNC client
# Host: localhost
# Port: 5900
# Password: secret (default)
```

---

## CI/CD Issues

### Issue: GitHub Actions workflow not triggering

**Error:**
Workflow doesn't run on push

**Solution:**
```yaml
# Check workflow triggers
on:
  push:
    branches: [ main, master ]  # Must match your branch
  pull_request:
    branches: [ main ]

# Verify branch name
git branch

# Check workflow file location
ls .github/workflows/
```

### Issue: Tests pass locally but fail in CI

**Error:**
Tests fail in GitHub Actions

**Solution:**
```yaml
# Add debug steps in workflow
- name: Debug
  run: |
    echo "Python version: $(python --version)"
    echo "Pip version: $(pip --version)"
    echo "Environment: $ENV"

# Check timing issues
- name: Run tests with verbose
  run: pytest -vv --tb=long

# Upload artifacts on failure
- name: Upload screenshots
  if: failure()
  uses: actions/upload-artifact@v4
  with:
    name: screenshots
    path: screenshots/
```

### Issue: Allure report deployment fails

**Error:**
GitHub Pages deployment fails

**Solution:**
```yaml
# Check permissions
permissions:
  contents: read
  pages: write
  id-token: write

# Verify GitHub Pages settings
# Repository -> Settings -> Pages -> Source: GitHub Actions

# Use correct action
- name: Deploy to GitHub Pages
  uses: peaceiris/actions-gh-pages@v3
  with:
    github_token: ${{ secrets.GITHUB_TOKEN }}
    publish_dir: ./allure-report
```

---

## Performance Issues

### Issue: Tests run slowly

**Error:**
Test suite takes too long

**Solution:**
```bash
# Run in parallel
pytest -n 4

# Use headless mode
pytest --headless

# Skip slow tests
pytest -m "not slow"

# Profile test durations
pytest --durations=10

# Use session storage (already implemented)
# Verify it's working
pytest -v | grep "session"
```

### Issue: Browser memory leak

**Error:**
Browser memory usage grows over time

**Solution:**
```python
# Close browser after each test
@pytest.fixture
def browser():
    driver = get_driver()
    yield driver
    driver.quit()

# Clear cookies periodically
driver.delete_all_cookies()

# Restart browser every N tests
# conftest.py
def pytest_runtest_teardown(item, nextitem):
    if item.location[1] % 10 == 0:
        DriverHelper.restart_driver()
```

### Issue: Database bloat from test data

**Error:**
Test data accumulates

**Solution:**
```python
# Use fixtures with cleanup
@pytest.fixture
def test_data(browser):
    # Setup
    data_id = create_test_data()

    yield data_id

    # Cleanup
    delete_test_data(data_id)

# Or cleanup at end of session
def pytest_sessionfinish(session):
    cleanup_all_test_data()
```

---

## Debugging Tools

### Enable Debug Mode

```bash
# Verbose output
pytest -vv --tb=long -s

# Python debugger
pytest --pdb

# Stop on first failure
pytest -x --pdb

# Show local variables
pytest --tb=long --showlocals
```

### Screenshot on Failure

Already configured in `conftest.py`:
```python
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        allure.attach(driver.get_screenshot_as_png())
```

### Logging

```python
# Add logging to tests
import logging
logging.basicConfig(level=logging.DEBUG)

# Log to file
logging.basicConfig(
    filename='test.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```

---

## Still Having Issues?

1. **Check existing issues:**
   https://github.com/Galen-Chu/pms-test-automation-script/issues

2. **Create new issue:**
   - Use issue template
   - Include error messages
   - Provide environment details
   - Attach screenshots

3. **Debug checklist:**
   - [ ] Python version correct?
   - [ ] All dependencies installed?
   - [ ] Configuration files exist?
   - [ ] Browser drivers updated?
   - [ ] Docker running (if used)?
   - [ ] Environment variables set?
   - [ ] Tests run manually first?

---

*Last updated: March 11, 2026*
