# Contributing to PMS Test Automation Showcase

Thank you for your interest in contributing to this project! This document provides guidelines and instructions for contributing.

## 🎯 Ways to Contribute

- **Bug Reports**: Submit issues for bugs found
- **Feature Requests**: Suggest new features or enhancements
- **Code Contributions**: Submit pull requests for bug fixes or features
- **Documentation**: Improve or add documentation
- **Examples**: Add test examples or use cases

## 🐛 Reporting Bugs

Before submitting a bug report, please:

1. **Check existing issues** to avoid duplicates
2. **Use a clear title** that describes the problem
3. **Provide detailed information**:
   - Environment (Python version, OS, browser)
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Screenshots (if applicable)
   - Logs/error messages

### Bug Report Template

```markdown
**Description**
A clear description of the bug.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected Behavior**
What you expected to happen.

**Actual Behavior**
What actually happened.

**Environment**
- Python: [e.g. 3.12]
- OS: [e.g. Windows 11]
- Browser: [e.g. Chrome 120]
- Selenium: [e.g. 4.32.0]

**Screenshots**
If applicable, add screenshots.

**Additional Context**
Any other context about the problem.
```

## 💡 Requesting Features

Feature requests are welcome! Please:

1. **Check existing issues** for similar requests
2. **Use a clear title** describing the feature
3. **Explain the use case** and why it would be useful
4. **Provide examples** if possible

## 🔧 Development Setup

### Prerequisites

- Python 3.11+
- Git
- Docker (for Selenium Grid)
- Chrome/Firefox browser

### Local Development

1. **Fork and Clone**
   ```bash
   git clone https://github.com/Galen-Chu/PMS-test-automation-script.git
   cd pms-test-automation-script
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

4. **Setup Configuration**
   ```bash
   cp pytest.ini.example pytest.ini
   # Edit pytest.ini with your test configuration
   ```

5. **Run Tests**
   ```bash
   pytest src/tests/
   ```

## 📝 Code Style Guidelines

### Python Code Style

- Follow **PEP 8** style guide
- Use **meaningful variable names**
- Add **docstrings** to classes and functions
- Maximum line length: **100 characters**
- Use **type hints** where appropriate

### Example

```python
from typing import Dict, Optional
from selenium.webdriver.remote.webdriver import WebDriver

class LoginPage(BasePage):
    """Page object for login functionality.

    This class provides methods to interact with the login page,
    including username/password input and form submission.

    Example:
        >>> login_page = LoginPage(driver)
        >>> login_page.login("user@example.com", "password123")
    """

    def login(self, username: str, password: str) -> bool:
        """Perform login with provided credentials.

        Args:
            username: User's email or username
            password: User's password

        Returns:
            True if login successful, False otherwise

        Raises:
            LoginError: If login fails due to invalid credentials
        """
        self.input(self.locator.input_username, username)
        self.input(self.locator.input_password, password)
        self.click(self.locator.btn_login)
        return self.is_login_successful()
```

### Test Code Style

- Use **AAA pattern** (Arrange, Act, Assert)
- **One assertion per test** when possible
- **Descriptive test names** that explain what is being tested
- Add **docstrings** explaining test purpose

```python
def test_reservation_with_valid_guest_data_should_be_created():
    """Test that a reservation is created successfully with valid data.

    Verifies that:
    - Reservation appears in list after creation
    - Reservation data is correctly stored
    - Confirmation message is displayed
    """
    # Arrange
    guest_data = {
        "name": "John Doe",
        "email": "john@example.com",
        "room_type": "Standard"
    }

    # Act
    reservation_id = browser.reservation.create(guest_data)

    # Assert
    assert browser.reservation.exists(reservation_id), \
        f"Reservation {reservation_id} not found in list"
```

## 🧪 Testing Guidelines

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest src/tests/test_login.py

# Run with markers
pytest -m smoke
pytest -m "not slow"

# Run in parallel
pytest -n 4

# Run with coverage
pytest --cov=src --cov-report=html
```

### Test Requirements

- All new code must have **test coverage**
- Tests must be **independent** and **repeatable**
- Use **fixtures** for common setup
- Mock external dependencies when appropriate

## 📋 Pull Request Process

### Before Submitting

1. **Update from main**
   ```bash
   git checkout main
   git pull upstream main
   git checkout your-feature-branch
   git merge main
   ```

2. **Run tests**
   ```bash
   pytest src/tests/
   ```

3. **Check code style**
   ```bash
   black src/ --check
   pylint src/
   ```

4. **Update documentation** if needed

### PR Guidelines

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make focused changes**
   - One feature/fix per PR
   - Keep changes minimal and focused

3. **Write clear commit messages**
   ```
   feat: add captcha retry logic for better reliability

   - Implement 3 retry attempts for captcha recognition
   - Add exponential backoff between retries
   - Log retry attempts for debugging

   Closes #123
   ```

4. **Update documentation**
   - Update README if needed
   - Add inline comments for complex logic
   - Update CHANGELOG.md

5. **Submit PR**
   - Use descriptive title
   - Fill out PR template
   - Link related issues
   - Request review

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] New tests added
- [ ] Documentation updated

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] No new warnings introduced
- [ ] Tests added/updated
- [ ] Local tests pass
```

## 📖 Documentation Guidelines

### Code Documentation

- **Docstrings** for all public classes and functions
- **Inline comments** for complex logic
- **Type hints** for better IDE support

### README Updates

Update README when:
- Adding new features
- Changing configuration
- Modifying setup process
- Adding new dependencies

## 🏷️ Issue Labels

- `bug` - Something isn't working
- `enhancement` - New feature or request
- `documentation` - Improvements or additions to documentation
- `good first issue` - Good for newcomers
- `help wanted` - Extra attention is needed
- `priority: high` - High priority
- `priority: low` - Low priority

## 📞 Getting Help

- **GitHub Issues**: For bug reports and feature requests
- **Discussions**: For questions and general discussion
- **Wiki**: For detailed guides and examples

## 📜 Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

## 🙏 Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes
- Project README

---

Thank you for contributing! 🎉
