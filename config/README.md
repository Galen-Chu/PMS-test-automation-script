# Configuration Guide

This directory contains configuration templates for the PMS Test Automation Framework.

## Setup Instructions

### 1. pytest Configuration

Copy the example file and customize it for your environment:

```bash
cp pytest.ini.template pytest.ini
```

Edit `pytest.ini` and replace placeholder values with your actual:
- Application URLs
- Authentication credentials
- Environment settings

### 2. Environment Variables (Alternative)

You can also use a `.env` file for environment variables:

```bash
cp .env.example .env
```

### 3. Docker Selenium Grid

To run tests with Docker Selenium Grid:

```bash
# Start Selenium Grid
docker-compose up -d

# Verify it's running
docker-compose ps

# View logs
docker-compose logs -f

# Stop when done
docker-compose down
```

Access Selenium Grid console at: http://localhost:4444

## Configuration Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| ENV | Environment name | demo, staging, production |
| WEB_URL | Base web application URL | https://demo.example.com |
| BASE_URL | Authentication endpoint | https://auth.example.com/... |
| REDIRECT_URL | OAuth callback URL | https://demo.example.com/callback |
| CLIENT_ID | OAuth client identifier | internal |
| LANGUAGE | UI language | en-US, zh-TW |
| ENV_NUM | Environment number | 1, 40 |
| VERSION | Application version | 131 |
| USERNAME | Test user username | autotest |
| PASSWORD | Test user password | ******** |
| SELENIUM_HUB | Selenium Grid hub URL | http://localhost:4444/wd/hub |

## Security Notes

- **Never commit** `pytest.ini` or `.env` files to version control
- These files are already included in `.gitignore`
- Use environment-specific credentials for testing
- Rotate test credentials regularly
