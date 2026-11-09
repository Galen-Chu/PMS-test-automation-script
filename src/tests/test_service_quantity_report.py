import allure
import pytest
from pages.athena_base_page import AthenaBasePage
from pages.service_quantity_report_page import ServiceQuantityReportPage
from pages.components.header_component import HeaderComponent
from tools.driver_helper import DriverHelper
from tools.test_data_helper import get_test_data, resolve_date
from tools import report_reader


@allure.feature("接待報表 - 服務數量報表")
class TestServiceQuantityReport:

    @allure.story("服務數量報表 - 查詢顯示報表（維度參數化）")
    @pytest.mark.xdist_group("test_service_quantity_report")
    @pytest.mark.dependency(name="test_query_service_quantity_report", scope="session")
    @pytest.mark.parametrize(
        "data_key",
        [
            "detail_by_date",
            "detail_by_room",
            "detail_by_ikey",
            "detail_by_item",
            "summary_by_date",
            "detail_all",
        ],
    )
    def test_query_service_quantity_report(self, logged_in_driver, report_staging, data_key):
        data = get_test_data("test_service_quantity_report", data_key)
        # service_date 非 checkin_date/checkout_date，resolve_date 不會自動 resolve，手動轉
        service_date = resolve_date(data["service_date"])

        pages = [ServiceQuantityReportPage, HeaderComponent, AthenaBasePage]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        with allure.step("Given 使用者選取進入「接待報表_入住前服務類_服務數量報表」頁面"):
            web.header_component.expand_menu("接待").sleep(1)
            web.header_component.to_func_page("服務數量報表").sleep(1)
            web.athena_base_page.screenshot(
                "Given 使用者選取進入「接待報表_入住前服務類_服務數量報表」頁面"
            )

        with allure.step("And 選擇查詢日期"):
            web.service_quantity_report_page.set_query_dat(service_date).sleep(0.5)
            web.athena_base_page.screenshot("And 選擇查詢日期")

        with allure.step("And 依所選項目設定排序方式"):
            web.service_quantity_report_page.select_sort_by(data["sort_option"]).sleep(0.5)
            web.athena_base_page.screenshot("And 依所選項目設定排序方式")

        with allure.step("And 依所選項目設定報表格式"):
            web.service_quantity_report_page.select_report_typ(data["report_option"]).sleep(0.5)
            web.athena_base_page.screenshot("And 依所選項目設定報表格式")

        with allure.step("And 依所選項目設定查詢範圍"):
            web.service_quantity_report_page.set_query_range(data["range_label"]).sleep(0.5)
            web.athena_base_page.screenshot("And 依所選項目設定查詢範圍")

        with allure.step("And 點擊[藍色放大鏡]"):
            web.service_quantity_report_page.query().sleep(1)
            web.athena_base_page.screenshot("And 點擊[藍色放大鏡]")

        with allure.step("Then 依查詢條件顯示報表"):
            pdf_url = web.service_quantity_report_page.get_report_pdf_url()
            pdf_path = report_reader.download(
                pdf_url, save_to=str(report_staging / f"service_{data_key}.pdf")
            )
            result = web.service_quantity_report_page.parse_report(pdf_path)

            # Tier 1-1 查詢回顯：頁尾 4 個維度反映送出的查詢參數
            web.athena_base_page.assert_data(
                "查詢回顯-查詢日期", result["echo"].get("查詢日期"), service_date
            )
            web.athena_base_page.assert_data(
                "查詢回顯-報表格式", result["echo"].get("報表格式"), data["report_echo"]
            )
            web.athena_base_page.assert_data(
                "查詢回顯-排序方式", result["echo"].get("排序方式"), data["sort_echo"]
            )
            web.athena_base_page.assert_data(
                "查詢回顯-查詢範圍", result["echo"].get("查詢範圍"), data["range_echo"]
            )

            # Tier 1-2 結構：表頭主要欄位存在
            if data["report_echo"] == "DETAIL":
                for header in (
                    "訂房卡號",
                    "房號",
                    "住客姓名",
                    "服務項目",
                    "數量",
                    "入住日期",
                    "退房日期",
                ):
                    web.athena_base_page.assert_data(
                        f"結構-表頭「{header}」存在", header in result["text"], True
                    )
            else:  # SUMMARY
                for header in ("服務項目", "小計", "房號", "數量", "總計"):
                    web.athena_base_page.assert_data(
                        f"結構-表頭「{header}」存在", header in result["text"], True
                    )

            # Tier 1-3 格式：頁數 > 0
            web.athena_base_page.assert_data("格式-頁數 > 0", result["page_count"] > 0, True)

            # Tier 1-4 排序驗證（DETAIL + 可排序的 sort_by：room/ikey）
            # BY_DATE/BY_ITEM 不驗排序：自測環境單一服務日/單一服務項目，值全相同無法以升序斷言
            if data["report_echo"] == "DETAIL" and data.get("sort_by"):
                values = web.service_quantity_report_page.sort_column_values(
                    pdf_path, data["sort_by"]
                )
                web.athena_base_page.assert_data(
                    f"排序-{data['sort_by']} 資料筆數 > 0", len(values) > 0, True
                )
                web.athena_base_page.assert_data(
                    f"排序-{data['sort_by']} 升序", values == sorted(values), True
                )

            # Tier 1-5 SUMMARY 各服務項目一致性（B 不變量）：每個 item 小計 == 該 item 明細數量加總
            # 小計值分組（同值 = 同 item 多排重印），不靠 item 名稱邊界。撞值風險見 page method docstring
            if data["report_echo"] == "SUMMARY":
                items = result["summary_items"]
                web.athena_base_page.assert_data(
                    "SUMMARY 一致性-有 item 分組", len(items) > 0, True
                )
                for item in items:
                    web.athena_base_page.assert_data(
                        f"SUMMARY 一致性-小計 {item['subtotal']} == 明細加總 {item['detail_sum']}",
                        item["match"],
                        True,
                    )

            # PDF viewer 是 Chrome plugin，無 DOM render-complete 信號可等，截圖前給渲染緩衝
            web.athena_base_page.sleep(3)
            web.athena_base_page.screenshot("Then 依查詢條件顯示報表")
