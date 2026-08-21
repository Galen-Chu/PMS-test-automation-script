# Setup Guide

Complete installation and configuration guide for the PMS Test Automation Framework.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Selenium Grid Setup](#selenium-grid-setup)
- [Running Tests](#running-tests)
- [Troubleshooting](#troubleshooting)

## Prerequisites

### Required Software

| Software | Version | Purpose |
|----------|---------|---------|
| Python | 3.12+ | Test framework |
| pip | Latest | Package manager |
| Docker | 20.10+ | Selenium Grid (optional) |
| Git | Latest | Version control |
| Chrome/Firefox/Edge | Latest | Browsers |

### Check Prerequisites

```bash
# Check Python version
python --version  # Should be 3.12 or higher

# Check pip
pip --version

# Check Docker (optional)
docker --version
docker-compose --version

# Check Git
git --version
```

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/Galen-Chu/PMS-test-automation-script.git
cd pms-test-automation-script
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Verify installation:**
```bash
pip list
```

Expected packages:
- selenium
- pytest
- allure-pytest
- tensorflow
- opencv-python

### 4. Install Browser Drivers (Optional)

If not using Selenium Grid:

**ChromeDriver:**
```bash
# Download from: https://chromedriver.chromium.org/
# Add to PATH
```

**GeckoDriver (Firefox):**
```bash
# Download from: https://github.com/mozilla/geckodriver/releases
# Add to PATH
```

## Configuration

### 1. Create pytest.ini

```bash
cp pytest.ini.example pytest.ini
```

Edit `pytest.ini` with your settings:

```ini
[pytest]
disable_test_id_escaping_and_forfeit_all_rights_to_community_support = true
env =
    ENV = staging
    WEB_URL = https://your-staging-url.com
    BASE_URL = https://your-auth-url.com
    REDIRECT_URL = https://your-redirect-url.com
    CLIENT_ID = your_client_id
    LANGUAGE = en-US
    ENV_NUM = 1
    VERSION = 131
    USERNAME = test_user
    PASSWORD = test_password
    SELENIUM_HUB = http://localhost:4444/wd/hub
```

### 2. Environment Variables (Alternative)

Create `.env` file:

```bash
cp .env.example .env
```

Edit `.env`:

```bash
ENV=staging
WEB_URL=https://your-staging-url.com
USERNAME=test_user
PASSWORD=test_password
```

### 3. Verify Configuration

```bash
# Quick test
pytest src/tests/test_login.py -v
```

## Selenium Grid Setup

### Option 1: Docker Compose (Recommended)

```bash
# Start Selenium Grid
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f selenium-hub

# Verify Selenium Grid is running
# Open browser: http://localhost:4444
```

**Stop Selenium Grid:**
```bash
docker-compose down
```

### Option 2: Manual Setup

1. **Download Selenium Server:**
   ```bash
   wget https://github.com/SeleniumHQ/selenium/releases/download/selenium-4.35.0/selenium-server-4.35.1.jar
   ```

2. **Start Hub:**
   ```bash
   java -jar selenium-server-4.35.1.jar hub
   ```

3. **Start Node (separate terminal):**
   ```bash
   java -jar selenium-server-4.35.1.jar node
   ```

### Verify Selenium Grid

```bash
# Check hub status
curl http://localhost:4444/status

# Expected response:
# {"value":{"ready":true,"message":"Selenium Grid ready"}}
```

## Running Tests

### Basic Commands

```bash
# Run all tests
pytest

# Run specific test file
pytest src/tests/test_login.py

# Run specific test
pytest src/tests/test_login.py::test_login_success

# Run with verbose output
pytest -v

# Run with print statements
pytest -s
```

### Parallel Execution

```bash
# Run with 4 parallel workers
pytest -n 4

# Run with auto-detection of CPU cores
pytest -n auto

# Distribute tests by file
pytest -n 4 --dist loadfile
```

### Test Markers

```bash
# Run smoke tests only
pytest -m smoke

# Run regression tests
pytest -m regression

# Skip slow tests
pytest -m "not slow"

# Combine markers
pytest -m "smoke and not slow"
```

### Allure Reports

```bash
# Run tests with Allure
pytest --alluredir=allure-results

# Generate and view report
allure serve allure-results

# Generate static report
allure generate allure-results -o allure-report
allure open allure-report
```

## Project Structure Setup

### Create Required Directories

```bash
# Create directories if they don't exist
mkdir -p allure-results
mkdir -p allure-report
mkdir -p logs
mkdir -p screenshots
```

### Verify Directory Structure

```
pms-test-automation-script/
├── src/
│   ├── locators/
│   ├── pages/
│   ├── tests/
│   └── utils/
├── ml-models/
│   ├── captcha_model.keras
│   └── char_mappings.pkl
├── config/
├── docs/
├── reports/
├── pytest.ini           # Created from example
├── .env                 # Created from example
└── requirements.txt
```

## Troubleshooting

### Common Issues

#### 1. WebDriver Exception

**Error:**
```
selenium.common.exceptions.WebDriverException: Message: 'chromedriver' executable needs to be in PATH
```

**Solution:**
```bash
# Option 1: Use Selenium Grid
docker-compose up -d

# Option 2: Install chromedriver
# Download from https://chromedriver.chromium.org/
# Add to PATH
```

#### 2. Module Not Found

**Error:**
```
ModuleNotFoundError: No module named 'selenium'
```

**Solution:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate      # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

#### 3. Session Storage File Not Found

**Error:**
```
FileNotFoundError: session_storages.json
```

**Solution:**
```bash
# Create empty session storage file
echo "{}" > src/utils/session_storages.json

# Or run login test first to create it
pytest src/tests/test_login.py
```

#### 4. TensorFlow/CUDA Issues

**Error:**
```
Could not load dynamic library 'cudart64_110.dll'
```

**Solution:**
```bash
# TensorFlow will fall back to CPU automatically
# This is expected if you don't have CUDA installed

# To suppress warnings:
export TF_CPP_MIN_LOG_LEVEL=2  # macOS/Linux
set TF_CPP_MIN_LOG_LEVEL=2     # Windows
```

#### 5. Allure Command Not Found

**Error:**
```
'allure' is not recognized as an internal or external command
```

**Solution:**
```bash
# Install Allure CLI
# macOS:
brew install allure

# Windows (with Scoop):
scoop install allure

# Or use npm:
npm install -g allure-commandline
```

#### 6. Selenium Grid Not Responding

**Error:**
```
urllib.error.URLError: <urlopen error [Errno 111] Connection refused>
```

**Solution:**
```bash
# Check if Selenium Grid is running
docker-compose ps

# Restart Selenium Grid
docker-compose restart

# Check logs
docker-compose logs selenium-hub

# If still not working, recreate:
docker-compose down
docker-compose up -d
```

### Debug Mode

Enable verbose logging:

```bash
# pytest verbose
pytest -v --tb=long

# Selenium verbose
# Add to conftest.py:
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Health Check Script

Create `health_check.py`:

```python
import requests
import subprocess

def check_selenium_grid():
    try:
        response = requests.get('http://localhost:4444/status')
        if response.status_code == 200:
            print("✅ Selenium Grid is running")
        else:
            print("❌ Selenium Grid is not responding")
    except:
        print("❌ Selenium Grid is not running")

def check_python_version():
    result = subprocess.run(['python', '--version'], capture_output=True)
    print(f"✅ Python version: {result.stdout.decode()}")

def check_dependencies():
    try:
        import selenium
        import pytest
        import allure
        print("✅ All dependencies installed")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")

if __name__ == "__main__":
    print("=== Health Check ===")
    check_python_version()
    check_dependencies()
    check_selenium_grid()
```

Run:
```bash
python health_check.py
```

## Next Steps

- Read [Framework Guide](FRAMEWORK_GUIDE.md) to learn how to write tests
- Read [Best Practices](BEST_PRACTICES.md) for testing guidelines
- Review [Architecture](../ARCHITECTURE.md) to understand the framework

## Getting Help

- Check [Troubleshooting](#troubleshooting) section
- Review [FAQ](FAQ.md)
- Open an issue on GitHub
- Check the logs in `logs/` directory

---

**Need help?** Create an issue on GitHub or check the documentation.
