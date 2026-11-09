import allure
import pytest
from pages.athena_base_page import AthenaBasePage
from pages.arrival_guest_report_page import ArrivalGuestReportPage
from pages.components.header_component import HeaderComponent
from tools.driver_helper import DriverHelper
from tools.test_data_helper import get_test_data
from tools import report_reader


@allure.feature("接待報表 - 到達旅客報表")
class TestArrivalGuestReport:

    @allure.story("到達旅客報表 - 查詢顯示報表（維度參數化）")
    @pytest.mark.xdist_group("test_arrival_guest_report")
    @pytest.mark.dependency(name="test_query_arrival_guest_report", scope="session")
    @pytest.mark.parametrize(
        "data_key",
        [
            "main_defaults",
            "sort_link_nos_detail",
            "sort_room_detail",
            "not_ci_off_detail",
            "print_rent_off_detail",
        ],
    )
    def test_query_arrival_guest_report(self, logged_in_driver, report_staging, data_key):
        data = get_test_data("test_arrival_guest_report", data_key)

        pages = [ArrivalGuestReportPage, HeaderComponent, AthenaBasePage]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        with allure.step("Given 使用者選取進入「接待報表_入住前服務類_到達旅客報表」頁面"):
            web.header_component.expand_menu("接待").sleep(1)
            web.header_component.to_func_page("到達旅客報表").sleep(1)
            web.athena_base_page.screenshot(
                "Given 使用者選取進入「接待報表_入住前服務類_到達旅客報表」頁面"
            )

        with allure.step("And 點擊[藍色倒三角形]擴充"):
            web.arrival_guest_report_page.expand_advanced().sleep(1)
            web.athena_base_page.screenshot("And 點擊[藍色倒三角形]擴充")

        with allure.step("And 選擇是否勾選[排除已入住資料]"):
            web.arrival_guest_report_page.set_is_not_ci(data["is_not_ci"]).sleep(0.5)
            web.athena_base_page.screenshot("And 選擇是否勾選[排除已入住資料]")

        with allure.step("And 選擇是否勾選[列印房租]"):
            web.arrival_guest_report_page.set_is_print_rent(data["is_print_rent"]).sleep(0.5)
            web.athena_base_page.screenshot("And 選擇是否勾選[列印房租]")

        with allure.step("And 依所選項目設定排序方式"):
            web.arrival_guest_report_page.select_sort_cod(data["sort_option"]).sleep(0.5)
            web.athena_base_page.screenshot("And 依所選項目設定排序方式")

        with allure.step("And 依所選項目設定報表格式"):
            web.arrival_guest_report_page.select_sql_mod(data["sql_option"]).sleep(0.5)
            web.athena_base_page.screenshot("And 依所選項目設定報表格式")

        with allure.step("And 點擊[藍色放大鏡]"):
            web.arrival_guest_report_page.query().sleep(1)
            web.athena_base_page.screenshot("And 點擊[藍色放大鏡]")

        with allure.step("Then 依查詢條件顯示報表"):
            pdf_url = web.arrival_guest_report_page.get_report_pdf_url()
            pdf_path = report_reader.download(
                pdf_url, save_to=str(report_staging / f"arrival_{data_key}.pdf")
            )
            result = web.arrival_guest_report_page.parse_report(pdf_path)

            # Tier 1-1 查詢回顯：頁尾 5 個維度反映送出的查詢參數
            web.athena_base_page.assert_data(
                "查詢回顯-入住日期", result["echo"].get("入住日期"), data["checkin_date"]
            )
            web.athena_base_page.assert_data(
                "查詢回顯-排序方式", result["echo"].get("排序方式"), data["sort_echo"]
            )
            web.athena_base_page.assert_data(
                "查詢回顯-報表格式", result["echo"].get("報表格式"), data["sql_echo"]
            )
            web.athena_base_page.assert_data(
                "查詢回顯-排除已入住資料",
                result["echo"].get("排除已入住資料"),
                "Y" if data["is_not_ci"] else "N",
            )
            web.athena_base_page.assert_data(
                "查詢回顯-列印房租",
                result["echo"].get("列印房租"),
                "Y" if data["is_print_rent"] else "N",
            )

            # Tier 1-2 結構：表頭主要欄位存在
            for header in ("訂房卡號", "房號", "住客姓名", "入住日期", "訂房來源"):
                web.athena_base_page.assert_data(
                    f"結構-表頭「{header}」存在", header in result["text"], True
                )

            # Tier 1-3 格式：頁數 > 0
            web.athena_base_page.assert_data("格式-頁數 > 0", result["page_count"] > 0, True)

            # Tier 1-4 列印房租開關：表頭第 2 行有無「房租」欄 == 送出的 is_print_rent
            web.athena_base_page.assert_data(
                "列印房租開關-表頭房租欄 == 送出值",
                result["header_has_rent"],
                data["is_print_rent"],
            )

            # Tier 1-5 排序驗證（Detail 格式抽對應欄升序；Group 格式合併顯示不做）
            if data["sql_echo"] == "detail":
                values = web.arrival_guest_report_page.sort_column_values(pdf_path, data["sort_by"])
                web.athena_base_page.assert_data(
                    f"排序-{data['sort_by']} 資料筆數 > 0", len(values) > 0, True
                )
                web.athena_base_page.assert_data(
                    f"排序-{data['sort_by']} 升序", values == sorted(values), True
                )

            # Tier 1-6 Group 統計小計彙總不變量（房型 × 客層加總 == 顯示合計）
            if data["sql_echo"] == "group":
                rows = result["summary_rows"]
                total = result["summary_total"]
                web.athena_base_page.assert_data("Group 統計-有資料列", len(rows) > 0, True)
                web.athena_base_page.assert_data("Group 統計-有合計列", total is not None, True)
                # 橫加：每列 散客+商務+團體 == 小計
                for row in rows:
                    row_sum = sum(
                        report_reader.to_num(row[col]) or 0
                        for col in ("guest_f", "guest_c", "guest_g")
                    )
                    web.athena_base_page.assert_data(
                        f"Group 統計-房型 {row['room_type']} 橫加 == 小計",
                        row_sum,
                        report_reader.to_num(row["subtotal"]),
                    )
                # 直加：各房型小計加總 == 合計列小計
                web.athena_base_page.assert_data(
                    "Group 統計-房型小計加總 == 合計",
                    report_reader.sum_column(rows, "subtotal"),
                    report_reader.to_num(total["subtotal"]),
                )

            # PDF viewer 是 Chrome plugin，無 DOM render-complete 信號可等，截圖前給渲染緩衝
            web.athena_base_page.sleep(3)
            web.athena_base_page.screenshot("Then 依查詢條件顯示報表")
