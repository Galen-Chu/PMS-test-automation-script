"""Session persistence: save/restore browser session across test runs.

Saves cookies and sessionStorage after login, restores them on next run
to avoid the ~2 min captcha-based re-login cycle.
"""

import json
import os
import time
from pathlib import Path

SESSION_FILE = Path(__file__).resolve().parent.parent / ".session_state.json"


class SessionPersistence:
    """Manages saving and restoring browser session state."""

    @staticmethod
    def save(driver):
        """Save cookies and sessionStorage to disk after successful login."""
        state = {"cookies": driver.get_cookies(), "saved_at": time.time()}

        try:
            storage = driver.execute_script(
                "var d={}; for(var i=0;i<sessionStorage.length;i++){"
                "var k=sessionStorage.key(i); d[k]=sessionStorage.getItem(k)}"
                "return d;"
            )
            state["session_storage"] = storage or {}
        except Exception:
            state["session_storage"] = {}

        SESSION_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")

    @staticmethod
    def restore(driver):
        """Load saved cookies and sessionStorage into the driver.

        Returns True if restore was attempted (file exists).
        """
        if not SESSION_FILE.exists():
            return False

        try:
            state = json.loads(SESSION_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, KeyError):
            return False

        # Check freshness (reject if older than 30 minutes)
        age = time.time() - state.get("saved_at", 0)
        if age > 1800:
            return False

        # Navigate to target domain first so cookies can be set
        web_url = os.getenv("WEB_URL", "")
        driver.get(web_url)

        # Restore cookies
        for cookie in state.get("cookies", []):
            try:
                # Remove problematic fields
                clean = {
                    k: v
                    for k, v in cookie.items()
                    if k in ("name", "value", "domain", "path", "expiry", "secure", "httpOnly")
                }
                driver.add_cookie(clean)
            except Exception:
                pass  # Skip invalid cookies

        # Restore sessionStorage
        storage = state.get("session_storage", {})
        if storage:
            pairs = "; ".join(f"sessionStorage.setItem('{k}', '{v}')" for k, v in storage.items())
            try:
                driver.execute_script(pairs)
            except Exception:
                pass

        return True

    @staticmethod
    def clear():
        """Remove saved session file."""
        if SESSION_FILE.exists():
            SESSION_FILE.unlink()

    @staticmethod
    def check_alive(driver):
        """Lightweight check: hit a PMS API endpoint to verify session.

        Returns True if session appears valid.
        """
        try:
            web_url = os.getenv("WEB_URL", "")
            env_num = os.getenv("ENV_NUM", "")
            driver.get(f"{web_url}/pms/{env_num}/reservation/PMS0110010")
            time.sleep(3)
            body = driver.find_element("tag name", "body").text
            # Check for the session expired dialog
            expired_markers = ["請重新登入"]  # ["請重新登入"]
            return not any(m in body for m in expired_markers)
        except Exception:
            return False
