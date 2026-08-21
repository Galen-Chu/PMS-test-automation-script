import os
import pytest
import allure

from tools.driver_helper import DriverHelper

# pytest registers fixtures from conftest modules only; re-export the
# data fixtures here so every test module under tests/ can request them.
from tests.fixtures.data_fixtures import *  # noqa: E402,F401,F403


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):  # pylint: disable=unused-argument
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        try:
            allure.attach(
                DriverHelper.DRIVER.get_screenshot_as_png(),
                name="異常截圖",
                attachment_type=allure.attachment_type.PNG,
            )
        except Exception as e:  # pylint: disable=broad-exception-caught
            print(e)

    if rep.when == "teardown":
        try:
            if DriverHelper.DRIVER is not None:
                DriverHelper.DRIVER.quit()
                DriverHelper.DRIVER = None
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
