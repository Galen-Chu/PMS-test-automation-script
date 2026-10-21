"""Automated performance tests for PMS reservation module.

Two test classes:
1. TestPageLoadPerf — measures page load API timings (no user interaction)
2. TestBookingFlowPerf — measures booking flow API timings (save, recalculate)

Both generate HTML reports + raw JSON data automatically.

Run:
    pytest -m perf src/tests/test_perf_reservation.py -v --alluredir=allure-results
    PERF_ROUNDS=4 pytest -m perf ...  (default 2 rounds)
"""

import json
import os
import time
from datetime import datetime
from pathlib import Path

import allure
import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from tools.perf_analyzer import analyze_performance, format_duration
from tools.perf_report import save_perf_report

pytestmark = [pytest.mark.perf]

ROUNDS = int(os.getenv("PERF_ROUNDS", "2"))
ROOM_COUNT = int(os.getenv("PERF_ROOMS", "150"))
REPORT_DIR = Path("perf-reports")
REPORT_DIR.mkdir(exist_ok=True)
ENV_LABEL = os.getenv("ENV", "qa").upper()
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M")


@allure.feature("Performance")
class TestPageLoadPerf:
    """Measure PMS0110010 page load API performance."""

    @allure.story("PMS0110010 page load")
    def test_page_load(self, logged_in_driver, perf_monitor):
        """Navigate to page N times, collect API timings each round."""
        driver = logged_in_driver
        all_apis = []

        for rd in range(1, ROUNDS + 1):
            driver.get(
                f"{os.getenv('WEB_URL')}/pms/{os.getenv('ENV_NUM')}"
                "/reservation/PMS0110010?prg_id=PMS0110010&locale=zh_TW"
            )
            time.sleep(5)
            apis = perf_monitor.collect_page_load()
            all_apis.extend(apis)
            print(f"  Round {rd}: {len(apis)} APIs")

        # Generate report
        output = str(REPORT_DIR / f"page_load_{TIMESTAMP}.html")
        meta = {
            "test": f"PMS0110010 Page Load ({ROUNDS} rounds)",
            "env": ENV_LABEL,
            "date": TIMESTAMP,
        }
        save_perf_report(all_apis, output, meta, report_type="page_load")

        # Attach to Allure
        slowest = sorted(all_apis, key=lambda x: x["duration"], reverse=True)
        summary = [
            f"Page Load Performance ({ROUNDS} rounds, {len(all_apis)} APIs)",
            "",
            "Top 10 Slowest:",
        ] + [f"  {format_duration(a['duration'])} {a['name']}" for a in slowest[:10]]
        allure.attach("\n".join(summary), name="perf_page_load")
        allure.attach.file(
            output, name="perf_report_html", attachment_type=allure.attachment_type.HTML
        )

        assert len(all_apis) > 0, "No APIs collected — page load may have failed"


@allure.feature("Performance")
class TestBookingFlowPerf:
    """Measure PMS0110010 booking flow API performance (save, recalculate)."""

    @allure.story("Booking 150 rooms flow")
    def test_booking_flow(self, logged_in_driver, perf_monitor):
        """Full booking flow: select STD -> open dialog -> 150 rooms -> save."""
        driver = logged_in_driver

        for rd in range(1, ROUNDS + 1):
            print(f"  Round {rd}: starting booking flow...")
            result = self._do_booking_round(driver, perf_monitor, rd)
            print(f"  Round {rd}: {result}")

        # Collect and analyze
        perf_monitor.stop()
        apis = perf_monitor.get_api_timings()
        analysis = analyze_performance(
            {"ops": perf_monitor.get_click_log(), "apis": apis},
            thresholds={"booking": 30000, "recalculate": 10000},
        )

        # Generate report
        output = str(REPORT_DIR / f"booking_{TIMESTAMP}.html")
        meta = {
            "test": f"PMS0110010 Booking {ROOM_COUNT} Rooms ({ROUNDS} rounds)",
            "env": ENV_LABEL,
            "date": TIMESTAMP,
        }
        save_perf_report(analysis, output, meta, report_type="booking")

        # Attach to Allure
        self._attach_allure(analysis, output)
        assert analysis["stats"]["total_api_count"] > 0, "No APIs collected"

    def _do_booking_round(self, driver, pm, rd):
        """Execute one booking round: navigate -> select -> dialog -> save."""
        # Step 1: Navigate
        driver.get(
            f"{os.getenv('WEB_URL')}/pms/{os.getenv('ENV_NUM')}"
            "/reservation/PMS0110010?prg_id=PMS0110010&locale=zh_TW"
        )
        time.sleep(5)

        # Step 2: Start monitoring AFTER page loads
        pm.start()

        # Step 3: Click STD row date cells via JS (more reliable than Selenium selectors)
        clicked = driver.execute_script("""
            var rows = document.querySelectorAll('tr');
            for (var i = 0; i < rows.length; i++) {
                if (rows[i].textContent.indexOf('STD(') !== -1) {
                    var cells = rows[i].querySelectorAll('td.pointer');
                    if (cells.length > 5) {
                        cells[3].click();
                        return 'clicked_start';
                    }
                }
            }
            return 'no_std_row';
        """)
        time.sleep(1)

        if clicked == "no_std_row":
            pm.stop()
            return "ERROR: STD row not found"

        # Step 4: Click next date cell (end date)
        driver.execute_script("""
            var rows = document.querySelectorAll('tr');
            for (var i = 0; i < rows.length; i++) {
                if (rows[i].textContent.indexOf('STD(') !== -1) {
                    var cells = rows[i].querySelectorAll('td.pointer');
                    if (cells.length > 5) {
                        cells[4].click();
                        return 'clicked_end';
                    }
                }
            }
            return 'no_cell';
        """)
        time.sleep(1)

        # Step 5: Click booking button
        try:
            btns = driver.find_elements(By.CSS_SELECTOR, "div.toolbar button.button")
            if btns:
                btns[0].click()
                time.sleep(3)
            else:
                pm.stop()
                return "ERROR: booking button not found"
        except Exception as e:
            pm.stop()
            return f"ERROR: {e}"

        # Step 6: Set room count in dialog
        try:
            qty = driver.find_element(By.ID, "groupOrderQuantity")
            qty.clear()
            qty.send_keys(str(ROOM_COUNT))
            time.sleep(2)
        except Exception:
            pass  # Dialog may not have opened; continue

        # Step 7: Fill booking name
        try:
            inputs = driver.find_elements(By.CSS_SELECTOR, ".e-control.e-textbox")
            for inp in inputs[:3]:
                if not inp.get_attribute("value"):
                    inp.send_keys(f"PERF_R{rd}")
                    break
            time.sleep(1)
        except Exception:
            pass

        # Step 8: Click save button
        try:
            save_btns = driver.find_elements(By.CSS_SELECTOR, ".e-control.e-btn")
            for btn in save_btns:
                if btn.is_displayed():
                    btn.click()
                    break
        except Exception:
            pass

        # Step 9: Wait for completion
        start = time.time()
        try:
            WebDriverWait(driver, 60).until(
                lambda d: "儲存成功" in d.find_element(By.TAG_NAME, "body").text
            )
            elapsed = time.time() - start
        except TimeoutException:
            elapsed = time.time() - start

        # Step 10: Dismiss toast + close dialog
        self._dismiss_and_close(driver)

        return f"save_wait={elapsed:.1f}s"

    def _dismiss_and_close(self, driver):
        """Dismiss toast and close dialog."""
        try:
            ok = driver.find_elements(By.CSS_SELECTOR, ".el-message-box__btns .el-button--primary")
            if ok:
                ok[0].click()
                time.sleep(1)
        except Exception:
            pass
        try:
            close = driver.find_elements(By.CSS_SELECTOR, ".e-dlg-closeicon-btn")
            if close:
                close[0].click()
                time.sleep(1)
        except Exception:
            pass

    def _attach_allure(self, analysis, report_path):
        """Attach performance summary and report to Allure."""
        stats = analysis.get("stats", {})
        save = stats.get("save", {})
        lines = [
            f"Booking Flow Performance ({ROUNDS} rounds)",
            f"Total APIs: {stats.get('total_api_count', 0)}",
            "",
            f"Save API: count={save.get('count', 0)}, "
            f"median={format_duration(save.get('median'))}",
        ]
        recalc = stats.get("recalculate", {})
        if recalc.get("count"):
            lines.append(
                f"Recalculate: count={recalc['count']}, "
                f"median={format_duration(recalc.get('median'))}"
            )
        if analysis.get("violations"):
            lines.append(f"\nViolations: {len(analysis['violations'])}")
            for v in analysis["violations"]:
                lines.append(f"  {v['api']}: {format_duration(v['duration_ms'])}")

        allure.attach("\n".join(lines), name="perf_booking")
        allure.attach.file(
            report_path, name="perf_report_html", attachment_type=allure.attachment_type.HTML
        )
