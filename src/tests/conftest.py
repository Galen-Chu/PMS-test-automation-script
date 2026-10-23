import os
import time
import threading
import pytest
import allure
from selenium.common.exceptions import UnexpectedAlertPresentException

from tools.driver_helper import DriverHelper
from tools.performance_monitor import PerformanceMonitor
from tools.session_persistence import SessionPersistence

# pytest registers fixtures from conftest modules only; re-export the
# data fixtures here so every test module under tests/ can request them.
from tests.fixtures.data_fixtures import *  # noqa: E402,F401,F403

# Persistent Chrome profile directory (survives browser restarts)
CHROME_PROFILE_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".chrome-profile"
)


# ============================================================================
# Session-scoped fixtures
# ============================================================================


def _create_driver():
    """Create Chrome with persistent profile (cookies survive restarts)"""
    from selenium.webdriver.chrome.options import Options as ChromeOptions
    from selenium.webdriver.chrome.service import Service
    from selenium import webdriver

    options = ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument(f"--user-data-dir={CHROME_PROFILE_DIR}")
    options.add_experimental_option(
        "prefs",
        {"profile.default_content_setting_values": {"notifications": 2}},
    )

    selenium_hub = os.getenv("SELENIUM_HUB")
    if selenium_hub:
        return webdriver.Remote(command_executor=selenium_hub, options=options)

    return webdriver.Chrome(service=Service(), options=options)


def _accept_js_alert(driver):
    """關閉未處理的 JS alert（如 context 未建立時 PMS 前端的 comp_cod 錯誤���窗）"""
    try:
        driver.switch_to.alert.accept()
        return True
    except Exception:
        return False


def _ensure_hotel_context(driver):
    """登入後走 EIP 建立飯店 context（comp_cod 等）。

    實測（2026-10-23, env 16）：PMS session cookie 由登入 callback 設定；
    EIP 頁面會由前端 JS 轉跳 auth，且本環境不自動返回，因此不能以
    URL 條件等待——固定等待即可，過程中的 JS alert 需關閉。"""
    web_url = os.getenv("WEB_URL", "")
    eip_url = f"{web_url}/eip/{os.getenv('ENV_NUM')}"
    driver.get(eip_url)
    time.sleep(8)  # 覆蓋 EIP→auth 轉跳與 context 寫入（實測 5 秒即足夠）
    _accept_js_alert(driver)


def _is_logged_in(driver):
    """Check if the current session is still valid by visiting PMS"""
    try:
        pms_url = f"{os.getenv('WEB_URL')}/pms/{os.getenv('ENV_NUM')}/reservation/PMS0110010"
        driver.get(pms_url)
        time.sleep(5)
        body = ""
        for _ in range(3):
            try:
                body = driver.find_element("tag name", "body").text
                break
            except UnexpectedAlertPresentException:
                _accept_js_alert(driver)
        return "請重新登入" not in body
    except Exception:
        return False


class SessionKeepAlive:
    """Background thread that periodically touches EIP to prevent idle timeout"""

    def __init__(self, driver, interval=180):
        self.driver = driver
        self.interval = interval
        self._stop = threading.Event()
        self._thread = None

    def start(self):
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def _run(self):
        eip_url = f"{os.getenv('WEB_URL')}/eip/{os.getenv('ENV_NUM')}"
        while not self._stop.is_set():
            if self._stop.wait(self.interval):
                break
            try:
                # Execute a lightweight JS call instead of full page navigation
                self.driver.execute_script("fetch('/')")
            except Exception:
                pass

    def stop(self):
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=5)


@pytest.fixture(scope="session")
def shared_driver():
    """Session-scoped Chrome with persistent profile + keep-alive"""
    driver = _create_driver()
    driver.implicitly_wait(10)
    DriverHelper.DRIVER = driver

    keep_alive = SessionKeepAlive(driver, interval=180)
    keep_alive.start()

    yield driver

    keep_alive.stop()
    driver.quit()
    DriverHelper.DRIVER = None


@pytest.fixture(scope="session")
def logged_in_driver(shared_driver):
    """Login once; persist session for faster subsequent runs."""
    from pages.login_page import LoginPage

    # Strategy 1: Restore saved cookies + sessionStorage
    if SessionPersistence.restore(shared_driver):
        if SessionPersistence.check_alive(shared_driver):
            print("[session] Restored from saved state (cookies + storage)")
        else:
            print("[session] Saved state expired, trying persistent profile...")
            # Strategy 2: Persistent Chrome profile cookies
            if _is_logged_in(shared_driver):
                print("[session] Reused from persistent Chrome profile")
            else:
                _do_login(shared_driver, LoginPage)
    else:
        # Strategy 2: Persistent Chrome profile cookies
        if _is_logged_in(shared_driver):
            print("[session] Reused from persistent Chrome profile")
        else:
            _do_login(shared_driver, LoginPage)

    # 經 EIP 建立飯店 context（comp_cod 等），完成前 PMS 無法使用
    _ensure_hotel_context(shared_driver)

    # Save session for next run
    SessionPersistence.save(shared_driver)
    print("[session] Session state saved for next run")

    yield shared_driver


def _do_login(driver, login_page_class):
    """Perform full login and save session."""
    print("[session] Performing full login...")
    driver.get(DriverHelper.build_auth_url())
    time.sleep(3)
    login_page = login_page_class(driver)
    login_page.login(os.getenv("USERNAME"), os.getenv("PASSWORD"))
    _accept_js_alert(driver)
    # 登入迴圈離開 auth 後仍停留在 callback URL：session cookie 的交換
    # 是非同步的，太早導航會腰斬它（PMS 之後讀不到 context → comp_cod 崩潰）
    time.sleep(3)
    SessionPersistence.save(driver)


@pytest.fixture(scope="function")
def perf_monitor(logged_in_driver):
    """Per-test performance monitor (injects hooks, collects API timings).

    Usage in test:
        def test_xxx(self, logged_in_driver, perf_monitor):
            perf_monitor.start()
            # ... page operations ...
            perf_monitor.attach_to_allure("test_xxx")
    """
    return PerformanceMonitor(logged_in_driver)


# ============================================================================
# Hooks
# ============================================================================


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):  # pylint: disable=unused-argument
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        try:
            allure.attach(
                DriverHelper.DRIVER.get_screenshot_as_png(),
                name="error_screenshot",
                attachment_type=allure.attachment_type.PNG,
            )
        except Exception as e:  # pylint: disable=broad-exception-caught
            print(e)


def pytest_configure(config):
    alluredir = config.getoption("--alluredir")
    if alluredir:
        properties_content = f"""
        TestEnv={os.getenv('ENV')}
        PmsVersion={os.getenv('VERSION')}
        """.strip()
        file_path = f"{alluredir}/environment.properties"
        os.makedirs(alluredir, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(properties_content)
