import allure
import pytest
from pages.athena_base_page import AthenaBasePage
from pages.booking_quantity_forecast_report_page import BookingQuantityForecastReportPage
from pages.components.header_component import HeaderComponent
from tools.driver_helper import DriverHelper
from tools import report_reader


@allure.feature("訂房報表 - 訂房數量預估報表(依參數)")
class TestBookingQuantityForecastReport:

    @allure.story("訂房數量預估報表(依參數) - 依預設範圍查詢顯示報表")
    @pytest.mark.xdist_group("test_booking_quantity_forecast_report")
    @pytest.mark.dependency(name="test_query_booking_quantity_forecast_report", scope="session")
    # pylint: disable=too-many-locals
    def test_query_booking_quantity_forecast_report(self, logged_in_driver, report_staging):
        pages = [BookingQuantityForecastReportPage, HeaderComponent, AthenaBasePage]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        with allure.step("Given 使用者進入「訂房數量預估報表(依參數)」頁面"):
            web.header_component.expand_menu("訂房").sleep(1)
            web.header_component.to_func_page("訂房數量預估報表(依參數)").sleep(1)
            # qry_dat 預設 = 滾房租日 +3 月，動態讀取作為 echo 預期值（環境無關）
            start_date, end_date = web.booking_quantity_forecast_report_page.get_qry_dat_range()
            web.athena_base_page.screenshot("Given 使用者進入「訂房數量預估報表(依參數)」頁面")

        with allure.step("And 點擊[放大鏡]搜尋按鈕"):
            web.booking_quantity_forecast_report_page.query().sleep(1)
            web.athena_base_page.screenshot("And 點擊[放大鏡]搜尋按鈕")

        with allure.step("Then 依查詢條件顯示報表"):
            pdf_url = web.booking_quantity_forecast_report_page.get_report_pdf_url()
            pdf_path = report_reader.download(
                pdf_url, save_to=str(report_staging / "booking_quantity_forecast.pdf")
            )
            result = web.booking_quantity_forecast_report_page.parse_report(pdf_path)

            # Tier 1-1 查詢回顯：起訖日期 == qry_dat 預設值
            web.athena_base_page.assert_data(
                "查詢回顯-起訖日期",
                result["echo"].get("起訖日期"),
                f"{start_date} ~ {end_date}",
            )

            # Tier 1-2 結構：表頭主要欄位存在
            for field, present in result["header_fields_present"].items():
                web.athena_base_page.assert_data(f"結構-表頭「{field}」存在", present, True)

            # Tier 1-3 格式：頁數 > 0 + 有日行資料 + 有合計行
            web.athena_base_page.assert_data("格式-頁數 > 0", result["page_count"] > 0, True)
            web.athena_base_page.assert_data("格式-有日行資料", len(result["day_rows"]) > 0, True)
            web.athena_base_page.assert_data("格式-有合計行", result["total_row"] is not None, True)

            # Tier 1-4 同列自洽不變量（每行：全部收入 == 房租+餐飲、總人數 == 大+小）
            all_rows = (
                result["day_rows"]
                + result["monthly_rows"]
                + ([result["total_row"]] if result["total_row"] else [])
            )
            for row in all_rows:
                label = row["date"]
                rent = report_reader.to_num(row.get("rent")) or 0
                fb = report_reader.to_num(row.get("fb")) or 0
                total_income = report_reader.to_num(row.get("total_income")) or 0
                adult = report_reader.to_num(row.get("adult")) or 0
                child = report_reader.to_num(row.get("child")) or 0
                guests = report_reader.to_num(row.get("guests")) or 0
                web.athena_base_page.assert_data(
                    f"同列自洽-{label} 全部收入==房租+餐飲", total_income, rent + fb
                )
                web.athena_base_page.assert_data(
                    f"同列自洽-{label} 總人數==大+小", guests, adult + child
                )

            # Tier 1-5 跨行彙總不變量（合計行數值 == 所有月累計加總）
            if result["total_row"] and result["monthly_rows"]:
                for col in ("total_rooms", "occupied", "rent", "fb", "total_income", "guests"):
                    monthly_sum = report_reader.sum_column(result["monthly_rows"], col)
                    total_val = report_reader.to_num(result["total_row"].get(col))
                    web.athena_base_page.assert_data(
                        f"彙總-合計 {col} == 月累計加總", total_val, monthly_sum
                    )

            # PDF viewer 是 Chrome plugin，無 DOM render-complete 信號可等，截圖前給渲染緩衝
            web.athena_base_page.sleep(3)
            web.athena_base_page.screenshot("Then 依查詢條件顯示報表")
