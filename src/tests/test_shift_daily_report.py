import allure
import pytest
from pages.athena_base_page import AthenaBasePage
from pages.shift_daily_report_page import ShiftDailyReportPage
from pages.components.header_component import HeaderComponent
from tools.driver_helper import DriverHelper
from tools.test_data_helper import get_test_data
from tools import report_reader


@allure.feature("出納報表 - 交班日報表")
class TestShiftDailyReport:

    @allure.story("交班日報表 - 查詢顯示報表")
    @pytest.mark.xdist_group("test_shift_daily_report")
    @pytest.mark.dependency(name="test_query_shift_daily_report", scope="session")
    def test_query_shift_daily_report(self, logged_in_driver, report_staging):
        data = get_test_data("test_shift_daily_report", "query_shift_daily_report")

        pages = [ShiftDailyReportPage, HeaderComponent, AthenaBasePage]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        with allure.step("Given 使用者選取進入「出納報表_交班報表類_交班日報表」頁面"):
            web.header_component.expand_menu("出納").sleep(1)
            web.header_component.to_func_page("交班日報表").sleep(1)
            web.athena_base_page.screenshot(
                "Given 使用者選取進入「出納報表_交班報表類_交班日報表」頁面"
            )

        with allure.step("When 選擇廳別並點擊「藍色放大鏡」進行查詢"):
            web.shift_daily_report_page.select_hall(data["hall_option"]).sleep(1)
            batch_date = web.shift_daily_report_page.get_batch_date()
            web.shift_daily_report_page.query().sleep(1)
            web.athena_base_page.screenshot("When 選擇廳別並點擊「藍色放大鏡」進行查詢")

        with allure.step("Then 依查詢條件顯示報表"):
            pdf_url = web.shift_daily_report_page.get_report_pdf_url()
            pdf_path = report_reader.download(
                pdf_url, save_to=str(report_staging / "shift_daily_report.pdf")
            )
            # PDF 不主動 attach；失敗時由 conftest failure hook 掃 report/ 附上（成功不附，控容量）
            result = web.shift_daily_report_page.parse_report(pdf_path)

            # Tier 1-1 查詢回顯：報表頁尾反映送出的查詢參數
            web.athena_base_page.assert_data(
                "查詢回顯-廳別", result["echo"].get("廳別"), data["hall_code"]
            )
            web.athena_base_page.assert_data(
                "查詢回顯-查詢日期", result["echo"].get("查詢日期"), batch_date
            )

            # Tier 1-2 結構：預期欄位表頭都在
            for header in ("代號", "名稱", "金額", "付款方式", "付款金額"):
                web.athena_base_page.assert_data(
                    f"結構-表頭「{header}」存在", header in result["text"], True
                )

            # Tier 1-3 彙總不變量：明細加總 == 顯示合計（與實際金額無關，抓彙總 bug）
            web.athena_base_page.assert_data(
                "收入明細加總 == 顯示合計",
                report_reader.sum_column(result["left_items"], "amount"),
                report_reader.to_num(result["left_total"]["amount"]),
            )
            web.athena_base_page.assert_data(
                "付款方式加總 == 顯示合計",
                report_reader.sum_column(result["right_items"], "amount"),
                report_reader.to_num(result["right_total"]["amount"]),
            )

            # Tier 1-4 格式：頁數 > 0
            web.athena_base_page.assert_data("格式-頁數 > 0", result["page_count"] > 0, True)
            # PDF viewer 是 Chrome plugin，無 DOM render-complete 信號可等，截圖前給渲染緩衝
            # （斷言全用 download 的 PDF bytes，不依賴此截圖；此 sleep 純為視覺證據完整）
            web.athena_base_page.sleep(3)
            web.athena_base_page.screenshot("Then 依查詢條件顯示報表")
