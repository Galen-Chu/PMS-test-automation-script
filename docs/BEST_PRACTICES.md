# Testing Best Practices

Guidelines and best practices for writing maintainable, reliable, and efficient test automation.

## Table of Contents

- [Test Design Principles](#test-design-principles)
- [Page Object Best Practices](#page-object-best-practices)
- [Locator Strategies](#locator-strategies)
- [Test Data Management](#test-data-management)
- [Error Handling](#error-handling)
- [Performance Optimization](#performance-optimization)
- [Security Considerations](#security-considerations)

## Test Design Principles

### 1. FIRST Principles

- **F**ast: Tests should run quickly
- **I**ndependent: Tests should not depend on each other
- **R**epeatable: Tests should produce same results every time
- **S**elf-validating: Tests should have clear pass/fail criteria
- **T**imely: Tests should be written close to the code being tested

### 2. AAA Pattern

Structure tests with Arrange-Act-Assert:

```python
def test_reservation_creation():
    # Arrange
    guest_data = {"name": "John Doe", "room": "Standard"}

    # Act
    reservation_id = browser.reservation.create(guest_data)

    # Assert
    assert browser.reservation.exists(reservation_id)
```

### 3. Single Responsibility

Each test should verify one thing:

```python
# Good - Tests one thing
def test_reservation_can_be_created():
    browser.reservation.create(valid_data)
    assert browser.reservation.exists()

# Avoid - Tests multiple things
def test_reservation_workflow():
    browser.reservation.create()
    browser.reservation.modify()
    browser.reservation.cancel()
    # What are we testing?
```

### 4. Test Independence

```python
# Good - Independent test
def test_create_reservation(browser):
    reservation_id = f"RES_{uuid.uuid4()}"  # Unique ID
    browser.reservation.create(reservation_id)
    assert browser.reservation.exists(reservation_id)

# Avoid - Dependent on other tests
def test_modify_reservation():
    # Assumes test_create_reservation ran first
    browser.reservation.modify("RES_123")
```

## Page Object Best Practices

### 1. Business-Focused Methods

```python
# Good - Business intent
class ReservationPage(BasePage):
    def create_reservation(self, guest_name, room_type):
        """Create a new reservation"""
        self.click_toolbar_item("新增")
        self.set_value_by_label("姓名", guest_name)
        self.select("房型", room_type)
        self.click_toolbar_item("儲存")

# Avoid - Low-level details
class ReservationPage(BasePage):
    def click_button(self, xpath):
        self.driver.find_element(By.XPATH, xpath).click()
```

### 2. Return Self for Chaining

```python
class LoginPage(BasePage):
    def input_username(self, username):
        self.input(self.locator.input_username, username)
        return self  # Enable chaining

    def input_password(self, password):
        self.input(self.locator.input_password, password)
        return self

    def click_login(self):
        self.click(self.locator.btn_login)
        return self

# Usage
login_page.input_username("user").input_password("pass").click_login()
```

### 3. Encapsulate Assertions

```python
# Good - Assertion in page object
class LoginPage(BasePage):
    def is_login_successful(self):
        """Check if login was successful"""
        return self.has_element(self.locator.welcome_message)

# Test
assert login_page.is_login_successful()

# Also good - Detailed assertion in test
def test_login():
    login_page.login("user", "pass")
    assert "Welcome" in login_page.get_welcome_message()
```

### 4. Use Meaningful Names

```python
# Good
class ReservationPage:
    def create_new_reservation(self): pass
    def search_by_guest_name(self, name): pass
    def get_total_reservation_count(self): pass

# Avoid
class ReservationPage:
    def action1(self): pass
    def search(self, x): pass
    def get_count(self): pass
```

## Locator Strategies

### 1. Priority Order

1. **ID** (Fastest, most reliable)
   ```python
   btn_submit = (By.ID, "submit-button")
   ```

2. **CSS Selector** (Fast, readable)
   ```python
   btn_submit = (By.CSS_SELECTOR, "button[type='submit']")
   ```

3. **XPath** (Flexible, but slower)
   ```python
   btn_submit = (By.XPATH, "//button[contains(text(), 'Submit')]")
   ```

4. **Class/Name** (Least reliable)
   ```python
   btn_submit = (By.CLASS_NAME, "submit")  # Avoid if possible
   ```

### 2. Use Stable Attributes

```python
# Good - Stable attributes
input_email = (By.ID, "email")
btn_submit = (By.CSS_SELECTOR, "[data-testid='submit-button']")

# Avoid - Fragile attributes
input_email = (By.XPATH, "/html/body/div[3]/form/input[2]")  # Position-based
btn_submit = (By.CSS_SELECTOR, ".btn-primary")  # Generic class
```

### 3. Use Relative Locators

```python
# Good - Relative to label
input_email = (By.XPATH, "//label[text()='Email']/following-sibling::input")

# Avoid - Absolute path
input_email = (By.XPATH, "/html/body/div/form/div[3]/input")
```

### 4. Make Locators Readable

```python
# Good
btn_create_reservation = (By.XPATH, "//button[contains(@class, 'create') and contains(text(), '新增')]")

# Avoid
btn1 = (By.XPATH, "//button[contains(@class, 'create')]")
```

## Test Data Management

### 1. Use Fixtures for Common Data

```python
# conftest.py
@pytest.fixture
def valid_guest_data():
    return {
        "name": "Test Guest",
        "email": "test@example.com",
        "phone": "+1-555-0123"
    }

# Test
def test_create_reservation(browser, valid_guest_data):
    browser.reservation.create(valid_guest_data)
```

### 2. Use Factories for Dynamic Data

```python
from faker import Faker

@pytest.fixture
def guest_factory():
    fake = Faker()

    def _create_guest():
        return {
            "name": fake.name(),
            "email": fake.email(),
            "phone": fake.phone_number()
        }

    return _create_guest

# Test
def test_with_random_data(browser, guest_factory):
    guest = guest_factory()
    browser.reservation.create(guest)
```

### 3. Externalize Configuration

```python
# pytest.ini or .env
WEB_URL=https://staging.example.com
USERNAME=test_user
PASSWORD=test_password

# Test
import os

def test_login(browser):
    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')
    browser.login.login(username, password)
```

### 4. Clean Up Test Data

```python
@pytest.fixture
def reservation(browser):
    """Create and cleanup reservation"""
    # Setup
    reservation_id = browser.reservation.create(valid_data)
    yield reservation_id

    # Teardown
    browser.reservation.delete(reservation_id)
```

## Error Handling

### 1. Use Explicit Waits

```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Good - Explicit wait
def wait_for_element(page, locator, timeout=10):
    return WebDriverWait(page.driver, timeout).until(
        EC.presence_of_element_located(locator)
    )

# Avoid - Implicit wait (global)
# driver.implicitly_wait(10)  # Don't set globally
```

### 2. Implement Retry Logic

```python
from selenium.common.exceptions import StaleElementReferenceException

def click_with_retry(page, locator, retries=3):
    """Click element with retry on stale reference"""
    for attempt in range(retries):
        try:
            element = page.driver.find_element(*locator)
            element.click()
            return
        except StaleElementReferenceException:
            if attempt == retries - 1:
                raise
            time.sleep(1)
```

### 3. Handle Timeouts Gracefully

```python
from selenium.common.exceptions import TimeoutException

def test_element_may_not_exist(browser):
    """Test that handles missing element"""
    try:
        element = wait_for_element(browser, locator, timeout=5)
        assert element.is_displayed()
    except TimeoutException:
        # Element doesn't exist - expected in some cases
        pass
```

### 4. Provide Meaningful Error Messages

```python
def test_reservation(browser):
    reservation_id = browser.reservation.create(data)

    # Good - Clear error message
    assert browser.reservation.exists(reservation_id), \
        f"Reservation {reservation_id} was not found in the list after creation"

    # Avoid - Generic error
    assert browser.reservation.exists(reservation_id)
```

## Performance Optimization

### 1. Reuse the Logged-in Session

The `logged_in_driver` fixture handles login once per session and
restores it across runs:

```python
def test_reservation(logged_in_driver):
    # Already logged in - faster!
    web = DriverHelper.get_logged_in_browser([ReservationPage])
    web.reservation_page.search()
```

### 2. Run Tests in Parallel

```bash
# Run 4 tests concurrently
pytest -n 4

# Distribute by file (faster)
pytest -n 4 --dist loadfile
```

### 3. Minimize Waits

```python
# Bad - Multiple sleeps
browser.login.login("user", "pass")
time.sleep(2)
browser.home.click_menu()
time.sleep(2)

# Good - Wait for specific conditions
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable(home.menu_item)
)
```

### 4. Use Efficient Selectors

```python
# Fast - ID selector
element = driver.find_element(By.ID, "submit")

# Slower - Complex XPath
element = driver.find_element(By.XPATH, "//div[@class='form']/button[contains(@class, 'submit') and not(@disabled)]")
```

## Security Considerations

### 1. Never Hardcode Credentials

```python
# Bad
browser.login.login("admin", "password123")

# Good
username = os.getenv('TEST_USERNAME')
password = os.getenv('TEST_PASSWORD')
browser.login.login(username, password)
```

### 2. Use Environment Variables

```python
# .env (not in version control)
TEST_USERNAME=your_username
TEST_PASSWORD=your_password
API_KEY=your_api_key

# .gitignore
.env
pytest.ini
credentials.json
```

### 3. Sanitize Sensitive Data in Reports

```python
@allure.step("Login with user")
def login_safely(page, username, password):
    """Login without exposing password in reports"""
    page.input_username(username)
    # Don't log password
    allure.attach("***", name="Password", attachment_type="text")
    page.input_password(password)
    page.click_login()
```

### 4. Use Test-Specific Accounts

```python
# Good - Dedicated test account
TEST_USER = {
    "username": "test_autobot",
    "role": "tester",
    "permissions": ["read", "write_test_data"]
}

# Avoid - Production credentials
PROD_USER = {
    "username": "admin",  # Too much access!
    "password": "prod_password"
}
```

## Code Quality

### 1. Follow PEP 8

```python
# Good
def test_create_reservation_with_valid_data():
    """Test creating a reservation with valid data."""
    reservation_id = create_reservation(guest_data)
    assert reservation_exists(reservation_id)

# Avoid
def testCreateReservationWithValidData():
    reservationId=createReservation(guestData)
    assert reservationExists(reservationId)
```

### 2. Use Type Hints

```python
from typing import Dict, Optional

def create_reservation(
    self,
    guest_data: Dict[str, str],
    room_type: str = "Standard"
) -> Optional[str]:
    """
    Create a new reservation.

    Args:
        guest_data: Guest information dictionary
        room_type: Type of room to reserve

    Returns:
        Reservation ID if successful, None otherwise
    """
    pass
```

### 3. Write Docstrings

```python
class ReservationPage(BasePage):
    """Page object for reservation management.

    This class provides methods to interact with the reservation
    page, including creating, modifying, and searching reservations.

    Example:
        >>> page = ReservationPage(driver)
        >>> page.create_reservation({"name": "John"}, "Standard")
        >>> assert page.has_reservation("John")
    """

    def create_reservation(self, guest_data: dict) -> str:
        """Create a new reservation.

        Args:
            guest_data: Dictionary containing guest information

        Returns:
            Reservation ID

        Raises:
            ReservationError: If reservation creation fails
        """
        pass
```

### 4. Use Linting

```bash
# Install linters
pip install pylint mypy black

# Run pylint
pylint src/

# Run type checker
mypy src/

# Format code
black src/
```

## Test Organization

### 1. Group Related Tests

```python
# test_reservation.py
class TestReservationCreation:
    """Tests for reservation creation"""

    def test_create_with_valid_data(self, browser):
        pass

    def test_create_with_invalid_data(self, browser):
        pass

class TestReservationModification:
    """Tests for reservation modification"""

    def test_modify_dates(self, browser):
        pass

    def test_modify_room_type(self, browser):
        pass
```

### 2. Use Tags/Marks

```python
import pytest

@pytest.mark.smoke
@pytest.mark.critical
def test_login():
    pass

@pytest.mark.regression
@pytest.mark.reservation
def test_create_reservation():
    pass

@pytest.mark.slow
def test_bulk_import():
    pass
```

### 3. Separate Test Types

```
tests/
├── smoke/              # Critical path tests
│   └── test_login.py
├── regression/         # Full regression suite
│   ├── test_reservation.py
│   └── test_guest.py
└── integration/        # End-to-end tests
    └── test_full_flow.py
```

## Continuous Improvement

### 1. Review and Refactor

- Review test code regularly
- Remove duplicate tests
- Update locators when UI changes
- Improve test execution time

### 2. Monitor Test Health

- Track flaky tests
- Monitor test execution time
- Review failure rates
- Update dependencies regularly

### 3. Document Changes

- Update documentation when adding features
- Document test data requirements
- Keep README current
- Maintain changelog

---

**Remember:** Good tests are an investment in quality. Take the time to write them well!

**See Also:**
- [Framework Guide](FRAMEWORK_GUIDE.md)
- [Setup Guide](SETUP.md)
- [Architecture Guide](../ARCHITECTURE.md)
