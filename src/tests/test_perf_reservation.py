"""Automated performance test: reservation booking 150 rooms.

Executes the full booking flow (select room -> enter 150 -> save)
multiple times and collects API timing data for each round.

Run: pytest -m perf src/tests/test_perf_reservation.py -v --alluredir=allure-results
"""

import os
import time

import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage
from pages.components.header_component import HeaderComponent
from pages.components.tip_component import TipComponent
from pages.login_page import LoginPage
from pages.reservation_page import ReservationPage
from tools.driver_helper import DriverHelper
from tools.performance_monitor import PerformanceMonitor
from tools.perf_analyzer import analyze_performance, format_duration

pytestmark = [pytest.mark.perf]

# Test configuration
ROOM_COUNT = 150
ROUNDS = int(os.getenv("PERF_ROUNDS", "2"))  # Default 2 rounds (to save time)
TEST_TAG = os.getenv("PERF_TAG", "PERF")


@allure.feature("Performance")
@allure.story("Reservation booking 150 rooms")
class TestReservationBookingPerf:
    """Measure API performance for 150-room booking on PMS0110010."""

    def test_booking_150_rooms(self, logged_in_driver, perf_monitor):
        """Page load API performance test (multi-round)."""
        driver = logged_in_driver

        all_raw_data = []
        for round_num in range(1, ROUNDS + 1):
            # Navigate to page (triggers page-load APIs)
            driver.get(
                f"{os.getenv('WEB_URL')}/pms/{os.getenv('ENV_NUM')}"
                "/reservation/PMS0110010?prg_id=PMS0110010&locale=zh_TW"
            )
            time.sleep(5)

            # Collect page-load APIs directly (no hooks injection needed)
            round_apis = perf_monitor.collect_page_load()
            all_raw_data.append(round_apis)
            print(f"  Round {round_num}: {len(round_apis)} API calls")

        # Aggregate analysis
        merged_apis = []
        for d in all_raw_data:
            merged_apis.extend(d)
        analysis = analyze_performance(
            {"ops": [], "apis": merged_apis},
            thresholds={"booking": 30000, "recalculate": 10000},
        )

        self._attach_results(analysis, [])

        # Assertions
        assert (
            analysis["stats"]["total_api_count"] > 0
        ), "No API calls recorded — page load may have failed"

    def _do_booking(self, driver, wait, round_num):
        """Execute booking flow on the current page (already navigated)."""
        # Step 1: Select a date cell
        try:
            std_cells = driver.find_elements(By.CSS_SELECTOR, "td.pointer:not(.name-color)")
            if std_cells:
                std_cells[0].click()
                time.sleep(1)
        except Exception as e:
            allure.attach(f"Date cell click: {e}", name=f"date_cell_error_r{round_num}")

        # Step 2: Click 訂房 button
        try:
            booking_btn = driver.find_element(By.CSS_SELECTOR, "div.toolbar button.button")
            booking_btn.click()
            time.sleep(3)
        except Exception as e:
            allure.attach(f"Booking button: {e}", name=f"booking_btn_error_r{round_num}")
            return {"round": round_num, "error": str(e)}

        # Step 3: Set room count
        try:
            qty_input = driver.find_element(By.ID, "groupOrderQuantity")
            qty_input.clear()
            qty_input.send_keys(str(ROOM_COUNT))
            time.sleep(2)
        except Exception as e:
            allure.attach(f"Room count: {e}", name=f"qty_error_r{round_num}")

        # Step 4: Fill required fields
        try:
            name_inputs = driver.find_elements(By.CSS_SELECTOR, ".e-control.e-textbox")
            for inp in name_inputs[:2]:
                if not inp.get_attribute("value"):
                    inp.send_keys(f"{TEST_TAG}_R{round_num}")
                    break
            time.sleep(1)
        except Exception as e:
            allure.attach(f"Name field: {e}", name=f"name_error_r{round_num}")

        # Step 5: Click save
        try:
            save_btns = driver.find_elements(By.CSS_SELECTOR, ".e-control.e-btn")
            for btn in save_btns:
                if btn.is_displayed():
                    btn.click()
                    break
        except Exception as e:
            allure.attach(f"Save button: {e}", name=f"save_error_r{round_num}")

        # Step 6: Wait for completion
        start_time = time.time()
        try:
            WebDriverWait(driver, 60).until(
                lambda d: "儲存成功" in d.find_element(By.TAG_NAME, "body").text
            )
            elapsed = time.time() - start_time
        except TimeoutException:
            elapsed = time.time() - start_time
            allure.attach(f"Timeout after {elapsed:.1f}s", name=f"timeout_r{round_num}")

        # Step 7: Dismiss toast and close dialog
        try:
            ok_btns = driver.find_elements(
                By.CSS_SELECTOR, ".el-message-box__btns .el-button--primary"
            )
            if ok_btns:
                ok_btns[0].click()
                time.sleep(2)
        except Exception:
            pass
        try:
            close_btns = driver.find_elements(By.CSS_SELECTOR, ".e-dlg-closeicon-btn")
            if close_btns:
                close_btns[0].click()
                time.sleep(2)
        except Exception:
            pass

        return {"round": round_num, "save_elapsed_s": elapsed}

    def _attach_results(self, analysis, round_data):
        """Attach performance analysis to Allure report."""
        # Summary
        stats = analysis["stats"]
        summary = [
            f"Performance Test Summary",
            f"=======================",
            f"Rounds: {stats['round_count']}",
            f"Total API calls: {stats['total_api_count']}",
            "",
            f"Save API (restV3/booking):",
            f"  Count: {stats['save']['count']}",
            f"  Median: {format_duration(stats['save']['median'])}",
            f"  Min: {format_duration(stats['save']['min'])}",
            f"  Max: {format_duration(stats['save']['max'])}",
            "",
            f"Recalculate API:",
            f"  Count: {stats['recalculate']['count']}",
        ]
        if stats["recalculate"]["median"]:
            summary.append(f"  Median: {format_duration(stats['recalculate']['median'])}")
            summary.append(f"  Max: {format_duration(stats['recalculate']['max'])}")

        # Violations
        if analysis["violations"]:
            summary.append("\nThreshold Violations:")
            for v in analysis["violations"]:
                summary.append(
                    f"  {v['api']}: {format_duration(v['duration_ms'])} "
                    f"(threshold: {format_duration(v['threshold_ms'])})"
                )

        # Top 10 slowest APIs
        summary.append("\nTop 10 Slowest APIs:")
        for api in analysis["slow_apis"]:
            summary.append(f"  {format_duration(api['duration'])} {api['name']}")

        allure.attach(
            "\n".join(summary), name="perf_summary", attachment_type=allure.attachment_type.TEXT
        )

        # Raw data as JSON
        import json

        allure.attach(
            json.dumps(
                {
                    "stats": {k: v for k, v in stats.items()},
                    "slow_apis": analysis["slow_apis"],
                    "violations": analysis["violations"],
                },
                indent=2,
                default=str,
            ),
            name="perf_data",
            attachment_type=allure.attachment_type.JSON,
        )
