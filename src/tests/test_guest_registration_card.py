import allure
import pytest
from pages.athena_base_page import AthenaBasePage
from pages.components.header_component import HeaderComponent
from pages.components.tip_component import TipComponent
from pages.guest_registration_card_page import GuestRegistrationCardPage
from tools.driver_helper import DriverHelper
from tools.test_data_helper import get_test_data
from tools import report_reader


@allure.feature("接待報表 - 旅客住宿登記卡")
class TestGuestRegistrationCard:

    @allure.story("旅客住宿登記卡 - 列印顯示報表預覽（單選/多選參數化）")
    @pytest.mark.xdist_group("test_guest_registration_card")
    @pytest.mark.dependency(name="test_print_registration_card", scope="session")
    @pytest.mark.parametrize("data_key", ["single_print", "multi_print"])
    # pylint: disable=too-many-locals
    def test_print_registration_card(self, logged_in_driver, report_staging, data_key):
        data = get_test_data("test_guest_registration_card", data_key)

        pages = [GuestRegistrationCardPage, HeaderComponent, AthenaBasePage]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        with allure.step("Given 使用者選取進入「接待報表_入住前服務類_旅客住宿登記卡」頁面"):
            web.header_component.expand_menu("接待").sleep(1)
            web.header_component.to_func_page("旅客住宿登記卡").sleep(1)
            web.athena_base_page.screenshot(
                "Given 使用者選取進入「接待報表_入住前服務類_旅客住宿登記卡」頁面"
            )

        with allure.step("And 點擊右側[放大鏡]搜尋"):
            web.guest_registration_card_page.search().sleep(2)
            web.athena_base_page.screenshot("And 點擊右側[放大鏡]搜尋")

        with allure.step("When 選取欲列印之資料列"):
            for ikey in data["ikeys"]:
                web.guest_registration_card_page.select_row_by_ikey(ikey)
            web.athena_base_page.screenshot("When 選取欲列印之資料列")

        with allure.step("And 點擊右側[列印]，出現格式下拉選單"):
            web.guest_registration_card_page.open_print_menu().sleep(0.5)
            web.athena_base_page.screenshot("And 點擊右側[列印]，出現格式下拉選單")

        with allure.step("And 點擊列印格式"):
            web.guest_registration_card_page.click_print_pdf().sleep(1)
            web.athena_base_page.screenshot("And 點擊列印格式")

        with allure.step("Then 顯示旅客住宿登記卡報表的預覽列印或儲存檔案"):
            page = web.guest_registration_card_page
            pdf_url = page.get_report_pdf_url()
            pdf_path = report_reader.download(
                pdf_url, save_to=str(report_staging / f"registration_card_{data_key}.pdf")
            )
            parsed = page.parse_report(pdf_path)

            # 格式：頁數 == 選取卡數（每卡一頁）
            web.athena_base_page.assert_data(
                "格式-頁數 == 選取卡數", parsed["page_count"], len(data["ikeys"])
            )

            # 結構：每張卡都有 ikey + 姓名 + 日期 + 房型 + 金額
            for card in parsed["cards"]:
                card_id = card.get("ikey", "?")
                for field in (
                    "guest_name",
                    "arrival",
                    "departure",
                    "room_type",
                    "room_rate",
                    "deposit",
                    "balance",
                ):
                    web.athena_base_page.assert_data(
                        f"結構-卡 {card_id} 欄位「{field}」有值", bool(card.get(field)), True
                    )

            # 內容：每張選取卡都出現在報表（存在驗證）
            cards_by_ikey = {card["ikey"]: card for card in parsed["cards"]}
            for ikey in data["ikeys"]:
                web.athena_base_page.assert_data(
                    f"內容-選取卡號 {ikey} 出現於報表", ikey in cards_by_ikey, True
                )

            # 主卡全欄位值驗證（第一張選取卡）：姓名/房型/日期/金額對 test_data
            main_ikey = data["main_card"]["ikey"]
            main = cards_by_ikey.get(main_ikey)
            web.athena_base_page.assert_data("主卡存在", main is not None, True)
            expected = data["main_card"]
            web.athena_base_page.assert_data(
                "主卡-住客姓名含關鍵字", expected["name_kw"] in main["guest_name"], True
            )
            web.athena_base_page.assert_data("主卡-入住日期", main["arrival"], expected["arrival"])
            web.athena_base_page.assert_data(
                "主卡-退房日期", main["departure"], expected["departure"]
            )
            web.athena_base_page.assert_data("主卡-房號", main["room"], expected["room"])
            web.athena_base_page.assert_data("主卡-房型", main["room_type"], expected["room_type"])
            web.athena_base_page.assert_data("主卡-住房人數", main["person"], expected["person"])
            web.athena_base_page.assert_data("主卡-房價", main["room_rate"], expected["room_rate"])
            web.athena_base_page.assert_data("主卡-訂金", main["deposit"], expected["deposit"])
            web.athena_base_page.assert_data("主卡-結餘", main["balance"], expected["balance"])

            # 不變量：結餘 == 房價 - 訂金（每張卡，與資料無關）
            for card in parsed["cards"]:
                invariant = card["room_rate_num"] - card["deposit_num"] == card["balance_num"]
                web.athena_base_page.assert_data(
                    f"不變量-卡 {card['ikey']} 結餘 == 房價-訂金", invariant, True
                )

            web.athena_base_page.sleep(3)
            web.athena_base_page.screenshot("Then 顯示旅客住宿登記卡報表的預覽列印或儲存檔案")

        with allure.step("Postcondition 關閉報表預覽視窗"):
            web.guest_registration_card_page.close_report_dialog().sleep(1)
            web.athena_base_page.screenshot("Postcondition 關閉報表預覽視窗")

    @allure.story("批次設定 - 執行批次設定時，未選擇資料須提醒使用者")
    @pytest.mark.xdist_group("test_guest_registration_card")
    @pytest.mark.dependency(name="test_batch_setting_no_selection_alert", scope="session")
    def test_batch_setting_no_selection_alert(self, logged_in_driver):
        pages = [GuestRegistrationCardPage, HeaderComponent, TipComponent, AthenaBasePage]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        with allure.step("Given 使用者進入「旅客住宿登記卡」頁面且未選擇資料"):
            web.header_component.expand_menu("接待").sleep(1)
            web.header_component.to_func_page("旅客住宿登記卡").sleep(1)
            web.guest_registration_card_page.search().sleep(2)
            web.athena_base_page.screenshot("Given 使用者進入「旅客住宿登記卡」頁面且未選擇資料")

        with allure.step("When 點擊[批次設定]按鈕"):
            web.guest_registration_card_page.open_batch_setting().sleep(1)
            web.athena_base_page.screenshot("When 點擊[批次設定]按鈕")

        with allure.step("Then 顯示「請先選擇需修改資料」訊息"):
            tip_text = web.tip_component.get_tip_text()
            web.athena_base_page.assert_data("未選提醒訊息", tip_text, "請選擇一筆資料")
            web.athena_base_page.screenshot("Then 顯示「請先選擇需修改資料」訊息")
            web.tip_component.click_ok().sleep(1)

    @allure.story("批次設定 - 批次設定成功（修改筆數 1筆/3筆參數化）")
    @pytest.mark.xdist_group("test_guest_registration_card")
    @pytest.mark.dependency(name="test_batch_setting_success", scope="session")
    @pytest.mark.parametrize("data_key", ["batch_setting_1", "batch_setting_3"])
    def test_batch_setting_success(self, logged_in_driver, data_key):
        data = get_test_data("test_guest_registration_card", data_key)
        ikeys = data["ikeys"]  # 本次修改筆數的卡列表
        is_print = data["is_print"]  # 本輪設定值（是/否）
        is_print_revert = data["is_print_revert"]  # 原值（復原目標）
        revert_code = data["revert_code"]  # 回復原值偵測用 code 前綴（Y : 是 / N : 否）

        web = DriverHelper.create_web_browser(
            [GuestRegistrationCardPage, HeaderComponent, TipComponent, AthenaBasePage],
            "pms",
            "reservation/PMS0110010",
        )
        page = web.guest_registration_card_page

        with allure.step("Given 使用者進入「旅客住宿登記卡」頁面"):
            web.header_component.expand_menu("接待").sleep(1)
            web.header_component.to_func_page("旅客住宿登記卡").sleep(1)
            page.search().sleep(2)
            web.athena_base_page.screenshot("Given 使用者進入「旅客住宿登記卡」頁面")

        with allure.step("Given 復原：若有卡列印房租非原值則批次設定回原值"):
            for ikey in ikeys:
                if not page.get_is_prtrent(ikey).startswith(revert_code):
                    page.apply_batch_setting(ikey, is_print_revert)
                    web.tip_component.click_ok().sleep(1)
                    page.search().sleep(2)
                    break
            web.athena_base_page.screenshot("Given 復原：若有卡列印房租非原值則批次設定回原值")

        with allure.step(f"When 選取欲設定的訂房卡號（{data['count_desc']}）"):
            for ikey in ikeys:
                page.select_row_by_ikey(ikey)
            web.athena_base_page.screenshot(f"When 選取欲設定的訂房卡號（{data['count_desc']}）")

        with allure.step("And 點擊左上方[批次設定]按鈕，進入「批次設定」視窗"):
            page.open_batch_setting().sleep(1)
            web.athena_base_page.screenshot("And 點擊左上方[批次設定]按鈕，進入「批次設定」視窗")

        with allure.step("And 點擊[列印房租]欄位，選擇設定值"):
            page.select_is_print(is_print).sleep(0.5)
            web.athena_base_page.screenshot("And 點擊[列印房租]欄位，選擇設定值")

        with allure.step("And 點擊[確定]"):
            page.confirm_batch_setting()
            web.athena_base_page.screenshot("And 點擊[確定]")

        with allure.step("Then 資料列的[列印房租]欄位顯示設定值"):
            web.tip_component.click_ok().sleep(1)
            page.search().sleep(2)
            for ikey in ikeys:
                actual = page.get_is_prtrent(ikey)
                web.athena_base_page.assert_data(
                    f"列印房租欄位（{ikey}）", actual, data["expected_echo"]
                )
            web.athena_base_page.screenshot("Then 資料列的[列印房租]欄位顯示設定值")

        with allure.step("Postcondition 批次設定列印房租回原值"):
            for ikey in ikeys:
                page.apply_batch_setting(ikey, is_print_revert)
                web.tip_component.click_ok().sleep(1)
                page.search().sleep(2)
                reverted = page.get_is_prtrent(ikey)
                web.athena_base_page.assert_data(
                    f"列印房租回復原值（{ikey}）", reverted, data["revert_echo"]
                )
            web.athena_base_page.screenshot("Postcondition 批次設定列印房租回原值")
