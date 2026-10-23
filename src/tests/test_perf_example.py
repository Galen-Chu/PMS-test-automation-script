"""Example performance test using perf_monitor fixture.

Demonstrates how to integrate performance monitoring into existing tests.
Run with: pytest -m perf -v --alluredir=allure-results
"""

import allure
import pytest

from pages.athena_base_page import AthenaBasePage
from pages.components.header_component import HeaderComponent
from pages.components.tip_component import TipComponent
from pages.reservation_page import ReservationPage
from tools.driver_helper import DriverHelper

pytestmark = [pytest.mark.perf]


@allure.feature("Performance")
class TestReservationPerformance:
    @allure.story("PMS0110010 page load timing")
    def test_reservation_page_load_perf(self, logged_in_driver, perf_monitor):
        """Measure PMS0110010 (by room type) page load performance.

        Reports API timings to Allure; slow APIs are informational
        (threshold assertions can be added per-project).
        """
        pages = [AthenaBasePage, HeaderComponent, TipComponent, ReservationPage]
        perf_monitor.start()
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")
        perf_monitor.mark("page_loaded")

        data = perf_monitor.attach_to_allure("reservation_page_load")

        # Verify monitoring captured data
        apis = data.get("apis", [])
        assert len(apis) > 0, "No API calls captured by performance monitor"
