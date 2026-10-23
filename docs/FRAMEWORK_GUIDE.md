# Framework Guide

Learn how to write tests using the PMS Test Automation Framework.

## Table of Contents

- [Writing Your First Test](#writing-your-first-test)
- [Page Object Model](#page-object-model)
- [Locators](#locators)
- [Working with Elements](#working-with-elements)
- [Assertions](#assertions)
- [Test Data](#test-data)
- [Dynamic Test Steps](#dynamic-test-steps)
- [Best Practices](#best-practices)

## Writing Your First Test

### Basic Test Structure

```python
# src/tests/test_example.py
import allure
from pages.components.header_component import HeaderComponent
from pages.maindesk_page import MaindeskPage
from tools.driver_helper import DriverHelper

def test_example(logged_in_driver):
    """Login is already handled by the logged_in_driver fixture"""
    # Build the page objects this test needs on the shared driver
    pages = [HeaderComponent, MaindeskPage]
    web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

    # Act + assert
    web.header_component.expand_menu("接待")
```

### Using pytest Fixtures

Session-scoped fixtures live in `src/tests/conftest.py`:

- `shared_driver` — one Chrome for the whole run (persistent profile,
  keep-alive thread); quits in teardown
- `logged_in_driver` — guarantees a logged-in state (saved session →
  Chrome profile → full login) and saves the session for the next run
- `perf_monitor` — per-test performance hooks for `@pytest.mark.perf`

```python
# Test using the fixtures
def test_with_fixture(logged_in_driver):
    """Browser is up and logged in already"""
    web = DriverHelper.get_logged_in_browser([MaindeskPage])
    web.maindesk_page.search()
```

## Page Object Model

### Creating a Page Object

```python
# src/pages/reservation_page.py
from pages.base_page import BasePage
from locators.reservation_locator import ReservationLocator

class ReservationPage(BasePage):
    """Reservation page interactions"""

    def __init__(self, driver):
        super().__init__(driver)
        self.locator = ReservationLocator()

    def create_new_reservation(self, guest_name, room_type):
        """Create a new reservation"""
        self.click_toolbar_item("新增")
        self.set_value_by_label("姓名", guest_name)
        self.select("房型", room_type)
        self.click_toolbar_item("儲存")
        return self

    def has_reservation(self, guest_name):
        """Check if reservation exists"""
        return self.has_target_ikey(guest_name)

    def get_reservation_count(self):
        """Get total reservation count"""
        return self.get_diplaying_items_count()
```

### Creating a Component

```python
# src/pages/components/header_component.py
from pages.base_page import BasePage
from locators.header_locator import HeaderLocator

class HeaderComponent(BasePage):
    """Reusable header component"""

    def click_menu(self, menu_name):
        """Click navigation menu"""
        locator = self.formator_locator(
            self.locator.menu_item,
            menu_name
        )
        self.click(locator)
        return self

    def get_user_name(self):
        """Get logged-in username"""
        return self.driver.find_element(
            *self.locator.user_name
        ).text
```

## Locators

### Creating Locator Class

```python
# src/locators/reservation_locator.py
from selenium.webdriver.common.by import By
from locators.base_locator import BaseLocator

class ReservationLocator(BaseLocator):
    """Locators for Reservation page"""

    # Form elements
    input_guest_name = (By.XPATH, "//input[@id='guestName']")
    input_arrival_date = (By.XPATH, "//input[@id='arrivalDate']")

    # Dropdowns
    dropdown_room_type = (By.XPATH, "//select[@id='roomType']")

    # Buttons
    btn_new_reservation = (By.XPATH, "//button[contains(text(),'新增')]")
    btn_save = (By.XPATH, "//button[contains(text(),'儲存')]")

    # Table elements
    table_reservations = (By.XPATH, "//table[@id='reservations']")
    row_reservation = (By.XPATH, "//tr[@data-reservation-id='%s']")
```

### Using Locators

```python
# Static locator
self.click(self.locator.btn_save)

# Parameterized locator
locator = self.formator_locator(
    self.locator.row_reservation,
    reservation_id
)
self.click(locator)
```

### Locator Best Practices

1. **Use meaningful variable names:**
   ```python
   # Good
   btn_submit = (By.XPATH, "//button[@type='submit']")
   input_email = (By.XPATH, "//input[@type='email']")

   # Avoid
   button1 = (By.XPATH, "//button")
   ```

2. **Prefer ID and CSS selectors:**
   ```python
   # Fast and reliable
   btn_login = (By.ID, "loginButton")
   input_password = (By.CSS_SELECTOR, "input[type='password']")

   # Use XPath when necessary
   btn_dynamic = (By.XPATH, "//button[contains(text(), '動態文字')]")
   ```

3. **Use relative XPaths:**
   ```python
   # Good - relative
   btn_submit = (By.XPATH, "//button[contains(@class, 'submit')]")

   # Avoid - absolute
   btn_submit = (By.XPATH, "/html/body/div[3]/div[2]/button[5]")
   ```

## Working with Elements

### Basic Interactions

```python
# Click element
page.click(page.locator.btn_submit)

# Input text
page.input(page.locator.input_name, "John Doe")

# Clear and input
page.input_with_clear(page.locator.input_email, "john@example.com")

# Select from dropdown
page.select("Room Type", "Standard")
```

### Advanced Interactions

```python
# Wait for element
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable(page.locator.btn_save)
)

# Mouse hover
actions = ActionChains(driver)
element = driver.find_element(*page.locator.menu_item)
actions.move_to_element(element).perform()

# Scroll to element
page.pointer_to_element(page.locator.footer)

# Execute JavaScript
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
```

### Working with Tables

```python
# Get row count
count = page.get_diplaying_items_count()

# Check if row exists
exists = page.has_target_ikey("RES001")

# Click specific row
page.click_target_ikey("RES001")
```

### Working with Dates

```python
# Select date
page.click_date_icon("arrivalDate")
page.select_date("2024", "12", "25")
```

## Assertions

### Using Framework Assertions

```python
# Assert equality
page.assert_data("Room Type", actual_type, "Standard")

# Assert item in list
page.assert_data_in_list(
    "Status",
    ["Confirmed", "Pending", "Cancelled"],
    "Confirmed"
)

# Assert item not in list
page.assert_data_not_in_list(
    "Status",
    ["Pending", "Cancelled"],
    "Confirmed"
)

# Assert count greater than 0
page.assert_data_has_count("Reservations", count)
```

### Using pytest Assertions

```python
# Basic assertion
assert actual_value == expected_value

# With custom message
assert actual_value == expected_value, "Values don't match"

# Assert in list
assert "Confirmed" in status_list

# Assert greater than
assert count > 0, "No reservations found"
```

## Test Data

### Using Test Fixtures

```python
# src/tests/conftest.py
import pytest

@pytest.fixture
def guest_data():
    """Provide test guest data"""
    return {
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "+1-234-567-8900",
        "room_type": "Standard"
    }

# Use in test
def test_create_reservation(browser, guest_data):
    browser.reservation.create_new_reservation(
        guest_data["name"],
        guest_data["room_type"]
    )
```

### Using Data Files

```python
# src/tests/data/reservation_data.json
{
    "valid_guest": {
        "name": "Test Guest",
        "email": "test@example.com"
    },
    "invalid_guest": {
        "name": "",
        "email": "invalid-email"
    }
}
```

```python
# Load data in test
import json

def test_with_json_data():
    with open('src/tests/data/reservation_data.json') as f:
        data = json.load(f)

    guest = data['valid_guest']
    # Use guest data...
```

### Using Faker for Random Data

```python
from faker import Faker

fake = Faker()

def test_with_random_data():
    guest_name = fake.name()
    email = fake.email()
    phone = fake.phone_number()

    # Use random data...
```

## Dynamic Test Steps

### Creating Dynamic Steps

```python
# src/tests/dymamic_steps/reservation_steps.py
import allure

class ReservationSteps:
    @staticmethod
    @allure.step("Create basic reservation")
    def create_basic_reservation(page, guest_name):
        """Reusable reservation creation step"""
        page.click_toolbar_item("新增")
        page.set_value_by_label("姓名", guest_name)
        page.click_toolbar_item("儲存")
        return page

    @staticmethod
    @allure.step("Verify reservation created")
    def verify_reservation_exists(page, guest_name):
        """Verify reservation was created"""
        assert page.has_reservation(guest_name), \
            f"Reservation for {guest_name} not found"
```

### Using Dynamic Steps

```python
# src/tests/test_reservation.py
from tests.dymamic_steps.reservation_steps import ReservationSteps

def test_create_reservation(browser):
    """Test creating a reservation using steps"""
    # Navigate to reservation page
    browser.home.navigate_to_reservations()

    # Use dynamic step
    ReservationSteps.create_basic_reservation(
        browser.reservation,
        "John Doe"
    )

    # Verify
    ReservationSteps.verify_reservation_exists(
        browser.reservation,
        "John Doe"
    )
```

## Parallel Testing

### Writing Parallel-Safe Tests

```python
# Good - Each test is independent
def test_create_reservation_1(browser):
    reservation_id = f"RES_{random.randint(1000, 9999)}"
    browser.reservation.create(reservation_id)
    assert browser.reservation.exists(reservation_id)

def test_create_reservation_2(browser):
    reservation_id = f"RES_{random.randint(1000, 9999)}"
    browser.reservation.create(reservation_id)
    assert browser.reservation.exists(reservation_id)

# Avoid - Tests depend on each other
def test_setup_data():
    # Creates data that other tests use
    pass

def test_use_data():
    # Depends on test_setup_data
    pass
```

### Using pytest-xdist

```python
# Run tests in parallel
pytest -n 4 src/tests/

# Distribute by file
pytest -n 4 --dist loadfile src/tests/

# Distribute by test function
pytest -n 4 --dist each src/tests/
```

## Test Organization

### File Structure

```python
# src/tests/
├── conftest.py              # Shared fixtures
├── test_login.py            # Login tests
├── test_reservation.py      # Reservation tests
├── test_guest_services.py   # Guest service tests
└── dymamic_steps/           # Reusable test steps
    ├── __init__.py
    ├── base_steps/
    └── reservation_steps.py
```

### Naming Conventions

```python
# Test files: test_<feature>.py
test_login.py
test_reservation.py

# Test classes: Test<Feature>
class TestLogin:
    pass

# Test functions: test_<action>_<expected_result>
def test_login_with_valid_credentials_success():
    pass

def test_login_with_invalid_credentials_fail():
    pass
```

## Test Markers

### Custom Markers

```python
# pytest.ini
[pytest]
markers =
    smoke: Smoke tests (critical path)
    regression: Regression tests
    slow: Slow running tests
    guest: Guest-related tests
    reservation: Reservation-related tests
```

### Using Markers

```python
import pytest

@pytest.mark.smoke
def test_login():
    """Critical smoke test"""
    pass

@pytest.mark.regression
@pytest.mark.reservation
def test_create_reservation():
    """Reservation regression test"""
    pass

@pytest.mark.slow
def test_bulk_import():
    """Slow bulk import test"""
    pass
```

### Running Marked Tests

```bash
# Run smoke tests
pytest -m smoke

# Run reservation tests but not slow ones
pytest -m "reservation and not slow"

# Run all except slow
pytest -m "not slow"
```

## Reporting

### Adding Allure Steps

```python
import allure

@allure.step("Login as {username}")
def login(page, username, password):
    """Login step with Allure reporting"""
    page.input_username(username)
    page.input_password(password)
    page.click_login()

@allure.step("Create reservation for {guest_name}")
def create_reservation(page, guest_name):
    """Reservation step with Allure reporting"""
    page.create_new_reservation(guest_name)
```

### Adding Attachments

```python
import allure

def test_with_screenshot(browser):
    """Test with screenshot attachment"""
    browser.login.login("user", "pass")

    # Attach screenshot
    allure.attach(
        browser.driver.get_screenshot_as_png(),
        name="Login Success",
        attachment_type=allure.attachment_type.PNG
    )

    # Attach text
    allure.attach(
        "Test completed successfully",
        name="Result",
        attachment_type=allure.attachment_type.TEXT
    )
```

### Adding Descriptions

```python
import allure

@allure.description("""
This test verifies the reservation creation workflow:
1. Login to the system
2. Navigate to reservation page
3. Create new reservation
4. Verify reservation appears in list
""")
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Reservation Management")
@allure.story("Create Reservation")
def test_create_reservation_complete(browser):
    """Complete reservation creation test"""
    pass
```

## Best Practices

### 1. Keep Tests Independent

```python
# Good - Self-contained
def test_create_reservation(browser):
    # Setup
    reservation_id = generate_unique_id()

    # Execute
    browser.reservation.create(reservation_id)

    # Verify
    assert browser.reservation.exists(reservation_id)

    # Cleanup (if needed)
    browser.reservation.delete(reservation_id)
```

### 2. Use Meaningful Names

```python
# Good
def test_reservation_with_valid_data_should_be_created_successfully():
    pass

# Avoid
def test_01():
    pass
```

### 3. Follow AAA Pattern

```python
def test_reservation_flow():
    # Arrange - Setup test data
    guest_name = "John Doe"
    room_type = "Standard"

    # Act - Perform action
    browser.reservation.create(guest_name, room_type)

    # Assert - Verify result
    assert browser.reservation.exists(guest_name)
```

### 4. Handle Waits Properly

```python
# Good - Explicit wait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable(page.locator.btn_save)
)

# Avoid - Hard-coded sleep
import time
time.sleep(5)  # Don't do this!
```

### 5. Clean Up Resources

The `shared_driver` session fixture owns teardown: it stops the
keep-alive thread and quits the browser after the whole session.
Tests never call `driver.quit()` themselves.

---

**Next Steps:**
- Review [Best Practices](BEST_PRACTICES.md)
- Check [Architecture Guide](../ARCHITECTURE.md)
- Explore [Examples](examples/)
