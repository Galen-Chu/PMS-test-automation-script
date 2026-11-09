import allure
import pytest
from pages.athena_base_page import AthenaBasePage
from pages.shift_detail_report_page import ShiftDetailReportPage
from pages.components.header_component import HeaderComponent
from tools.driver_helper import DriverHelper
from tools.test_data_helper import get_test_data
from tools import report_reader


@allure.feature("出納報表 - 交班明細表")
class TestShiftDetailReport:

    @allure.story("交班明細表 - 查詢顯示報表")
    @pytest.mark.xdist_group("test_shift_detail_report")
    @pytest.mark.dependency(name="test_query_shift_detail_report", scope="session")
    def test_query_shift_detail_report(self, logged_in_driver, report_staging):
        data = get_test_data("test_shift_detail_report", "query_shift_detail_report")

        pages = [ShiftDetailReportPage, HeaderComponent, AthenaBasePage]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        with allure.step("Given 使用者選取進入「出納報表_交班報表類_交班明細表」頁面"):
            web.header_component.expand_menu("出納").sleep(1)
            web.header_component.to_func_page("交班明細表").sleep(1)
            web.athena_base_page.screenshot(
                "Given 使用者選取進入「出納報表_交班報表類_交班明細表」頁面"
            )

        with allure.step("When 選擇廳別並點擊「藍色放大鏡」進行查詢"):
            web.shift_detail_report_page.select_hall(data["hall_option"]).sleep(1)
            batch_date = web.shift_detail_report_page.get_batch_date()
            web.shift_detail_report_page.query().sleep(1)
            web.athena_base_page.screenshot("When 選擇廳別並點擊「藍色放大鏡」進行查詢")

        with allure.step("Then 依查詢條件顯示報表"):
            pdf_url = web.shift_detail_report_page.get_report_pdf_url()
            pdf_path = report_reader.download(
                pdf_url, save_to=str(report_staging / "shift_detail_report.pdf")
            )
            # PDF 不主動 attach；失敗時由 conftest failure hook 掃 report/ 附上（成功不附，控容量）
            result = web.shift_detail_report_page.parse_report(pdf_path)

            # Tier 1-1 查詢回顯：報表頁尾反映送出的查詢參數
            web.athena_base_page.assert_data(
                "查詢回顯-廳別", result["echo"].get("廳別"), data["hall_code"]
            )
            web.athena_base_page.assert_data(
                "查詢回顯-查詢日期", result["echo"].get("查詢日期"), batch_date
            )

            # Tier 1-2 結構：15 欄表頭都在（「現」「金」在 PDF 跨兩 word，用單字「現」存在斷言）
            for header in (
                "系統別",
                "公帳號",
                "房號/單據編號",
                "發票號碼",
                "姓名",
                "入住日/入帳日",
                "退房日",
                "房租",
                "服務費",
                "客房其他",
                "預收款",
                "客房訂金",
                "現",
                "MASTER信用卡",
                "沖客房預收款",
            ):
                web.athena_base_page.assert_data(
                    f"結構-表頭「{header}」存在", header in result["text"], True
                )

            # Tier 1-3 彙總不變量：8 個數值欄明細加總 == 總計行（抓彙總 bug，與實際金額無關）
            web.athena_base_page.assert_data("彙總-總計行存在", result["total"] is not None, True)
            web.athena_base_page.assert_data("彙總-明細資料列 > 0", len(result["items"]) > 0, True)
            for col in ShiftDetailReportPage.NUMERIC_COLS:
                web.athena_base_page.assert_data(
                    f"彙總-{col} 明細加總 == 總計",
                    report_reader.sum_column(result["items"], col),
                    report_reader.to_num(result["total"].get(col, "")),
                )

            # Tier 1-4 格式：頁數 > 0
            web.athena_base_page.assert_data("格式-頁數 > 0", result["page_count"] > 0, True)
            # PDF viewer 是 Chrome plugin，無 DOM render-complete 信號可等，截圖前給渲染緩衝
            # （斷言全用 download 的 PDF bytes，不依賴此截圖；此 sleep 純為視覺證據完整）
            web.athena_base_page.sleep(3)
            web.athena_base_page.screenshot("Then 依查詢條件顯示報表")
