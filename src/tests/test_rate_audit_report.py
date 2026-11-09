import allure
import pytest
from pages.athena_base_page import AthenaBasePage
from pages.rate_audit_report_page import RateAuditReportPage
from pages.components.header_component import HeaderComponent
from tools.driver_helper import DriverHelper
from tools.test_data_helper import get_test_data
from tools import report_reader


@allure.feature("夜核報表 - 房價稽核表")
class TestRateAuditReport:

    @allure.story("房價稽核表 - 依類別查詢顯示報表（F/G/C 參數化）")
    @pytest.mark.xdist_group("test_rate_audit_report")
    @pytest.mark.dependency(name="test_query_rate_audit_report", scope="session")
    @pytest.mark.parametrize("data_key", ["guest_way_f", "guest_way_g", "guest_way_c"])
    def test_query_rate_audit_report(self, logged_in_driver, report_staging, data_key):
        data = get_test_data("test_rate_audit_report", data_key)

        pages = [RateAuditReportPage, HeaderComponent, AthenaBasePage]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        with allure.step("Given 使用者進入「房價稽核表」頁面"):
            web.header_component.expand_menu("夜核").sleep(1)
            web.header_component.to_func_page("房價稽核表").sleep(1)
            # 查詢日期預設 = PMS 營業日，動態讀取作為 echo 預期值（環境無關）
            expected_query_date = web.rate_audit_report_page.get_search_date()
            web.athena_base_page.screenshot("Given 使用者進入「房價稽核表」頁面")

        with allure.step("When 選擇[類別]"):
            web.rate_audit_report_page.select_guest_way(data["code"]).sleep(0.5)
            web.athena_base_page.screenshot("When 選擇[類別]")

        with allure.step("And 點擊[藍色放大鏡]進行查詢"):
            web.rate_audit_report_page.query().sleep(1)
            web.athena_base_page.screenshot("And 點擊[藍色放大鏡]進行查詢")

        with allure.step("Then 依查詢條件顯示報表"):
            pdf_url = web.rate_audit_report_page.get_report_pdf_url()
            pdf_path = report_reader.download(
                pdf_url, save_to=str(report_staging / f"rate_audit_{data_key}.pdf")
            )
            result = web.rate_audit_report_page.parse_report(pdf_path, data["code"])

            # Tier 1-1 查詢回顯：頁尾 3 個欄位反映送出的查詢參數
            web.athena_base_page.assert_data(
                "查詢回顯-查詢日期", result["echo"].get("查詢日期"), expected_query_date
            )
            web.athena_base_page.assert_data(
                "查詢回顯-金額為零不顯示", result["echo"].get("金額為零不顯示"), "Y"
            )
            web.athena_base_page.assert_data(
                "查詢回顯-排序方式", result["echo"].get("排序方式"), "依訂房卡"
            )

            # Tier 1-2 類別過濾不變量：非送出類別不混入（環境無關，三變體共通）
            # autotest 環境僅 F 散客訂房卡 C/I 資料，G/C 變體回空報表；不混入仍可驗
            for code, count in result["other_category_counts"].items():
                web.athena_base_page.assert_data(
                    f"類別過濾-非送出類別 {code} 不混入",
                    count,
                    0,
                )

            # Tier 1-3 結構：表頭主要欄位存在
            for field, present in result["header_fields_present"].items():
                web.athena_base_page.assert_data(f"結構-表頭「{field}」存在", present, True)

            # Tier 1-4 格式：頁數 > 0
            web.athena_base_page.assert_data("格式-頁數 > 0", result["page_count"] > 0, True)

            # PDF viewer 是 Chrome plugin，無 DOM render-complete 信號可等，截圖前給渲染緩衝
            web.athena_base_page.sleep(3)
            web.athena_base_page.screenshot("Then 依查詢條件顯示報表")
