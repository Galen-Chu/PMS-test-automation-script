import random

import allure
import pytest
from pages.athena_base_page import AthenaBasePage
from pages.components.header_component import HeaderComponent
from pages.components.share_panel_component import SharePanelComponent
from pages.components.tip_component import TipComponent
from pages.forex_exchange_page import ForexExchangePage
from tests.share_steps import ShareSteps
from tools.driver_helper import DriverHelper
from tools.test_data_helper import get_test_data


@allure.feature("外幣匯兌維護")
class TestForexExchange:

    @allure.story("外幣匯兌維護 - 新增一筆外幣匯兌")
    @pytest.mark.xdist_group("test_forex_exchange")
    @pytest.mark.dependency(name="test_add_forex", scope="session")
    @pytest.mark.parametrize("data_key", ["forex_non_cny", "forex_cny"])
    def test_add_forex(self, logged_in_driver, data_key):
        # pylint: disable=too-many-locals  # data 拆變數 + 編輯 Panel 11 欄驗證
        data = get_test_data("test_forex_exchange", data_key)
        full_name = data["full_name"]
        room_no = data["room_no"]
        id_code = f"A{random.randint(100000000, 999999999)}"
        birthday_day = data["birthday_day"]
        currency = data["currency"]
        foreign_amount = data["foreign_amount"]
        service_amount = data["service_amount"]
        ikey = data["ikey"]

        pages = [
            ForexExchangePage,
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            AthenaBasePage,
        ]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        with allure.step("Given 使用者進入「外幣匯兌維護」頁面"):
            web.header_component.expand_menu("出納").sleep(1)
            web.header_component.to_func_page("外幣匯兌維護").sleep(1)
            # 未開班觸發開班 dialog 攔截（首次/跨日 session 可能未開班）
            if web.athena_base_page.has_element(web.forex_exchange_page.locator.dialog_shift):
                ShareSteps.open_shift(web, "FO : 飯店櫃檯", "a", "autotest")
                web.athena_base_page.sleep(1)
            web.athena_base_page.screenshot("Given 使用者進入「外幣匯兌維護」頁面")

        with allure.step("When 點擊[橘色加號]"):
            web.athena_base_page.click_toolbar_with_icon("add").sleep(1)
            web.athena_base_page.screenshot("When 點擊[橘色加號]")

        with allure.step("And 點擊[姓名]欄位輸入<姓名>並選擇<房號>住客"):
            web.forex_exchange_page.search_and_select_guest(full_name, room_no).sleep(1)
            web.athena_base_page.screenshot("And 點擊[姓名]欄位輸入<姓名>並選擇<房號>住客")

        with allure.step("And 點擊[證件號碼]欄位輸入<證件號碼>"):
            web.forex_exchange_page.input_id_code(id_code)
            web.athena_base_page.screenshot("And 點擊[證件號碼]欄位輸入<證件號碼>")

        with allure.step("And 點擊[生日]欄位選擇<生日>"):
            web.forex_exchange_page.select_birthday(birthday_day)
            web.athena_base_page.screenshot("And 點擊[生日]欄位選擇<生日>")

        with allure.step("And 點擊[幣別]欄位選擇<幣別>"):
            web.forex_exchange_page.select_currency(currency).sleep(0.5)
            web.athena_base_page.screenshot("And 點擊[幣別]欄位選擇<幣別>")

        with allure.step("And 點擊[外幣金額]欄位輸入<外幣金額>"):
            web.forex_exchange_page.input_amount(foreign_amount, service_amount)
            web.athena_base_page.screenshot("And 點擊[外幣金額]欄位輸入<外幣金額>")

        with allure.step("And 點擊[橘色磁碟片]進行儲存"):
            web.athena_base_page.click_toolbar_with_icon("save").sleep(1)
            web.athena_base_page.screenshot("And 點擊[橘色磁碟片]進行儲存")

        with allure.step("Then 顯示「新增成功 是否列印水單？」提示"):
            tip_text = web.tip_component.get_tip_text()
            web.athena_base_page.assert_data("新增成功提示", "新增成功" in tip_text, True)
            web.athena_base_page.screenshot("Then 顯示「新增成功 是否列印水單？」提示")
            # 取消不列印（避免觸發列印 dialog）
            web.athena_base_page.click(web.forex_exchange_page.locator.btn_alert_cancel)
            web.athena_base_page.sleep(1)
            # 關新增 Panel（save 後 Panel + window-mask 殘留，關 Panel 清 mask 才能搜尋列表）
            web.athena_base_page.click(web.forex_exchange_page.locator.btn_close_panel)
            web.athena_base_page.sleep(1)

        with allure.step("Then 「外幣匯兌維護」頁面新增一筆資料列"):
            web.forex_exchange_page.search_by_idcode(id_code).sleep(1)
            row_currency = web.forex_exchange_page.get_latest_row_field(ikey, "fmoneyCode")
            row_amount = web.forex_exchange_page.get_latest_row_field(ikey, "fmoneyAmt")
            web.athena_base_page.assert_data("新增資料列幣別", currency in row_currency, True)
            web.athena_base_page.assert_data("新增資料列外幣金額", row_amount, str(foreign_amount))
            web.athena_base_page.screenshot("Then 「外幣匯兌維護」頁面新增一筆資料列")

        with allure.step("And 重新打開該筆水單的編輯 Panel"):
            web.forex_exchange_page.open_edit_panel_for_latest(ikey).sleep(1)
            web.athena_base_page.screenshot("And 重新打開該筆水單的編輯 Panel")

        with allure.step("Then 編輯 Panel 欄位值與新增輸入一致"):
            fields = web.forex_exchange_page.get_edit_panel_fields()
            web.athena_base_page.assert_data("編輯Panel姓名", fields["full_name"], full_name)
            web.athena_base_page.assert_data("編輯Panel房號", fields["room_number"], room_no)
            web.athena_base_page.assert_data("編輯Panel國籍", fields["country_code"], "TWN")
            web.athena_base_page.assert_data(
                "編輯Panel證件號碼遮罩前綴", fields["id_code"].startswith(id_code[:3]), True
            )
            web.athena_base_page.assert_data(
                "編輯Panel生日含日", ("/" + str(birthday_day)) in fields["birthday"], True
            )
            web.athena_base_page.assert_data(
                "編輯Panel幣別", currency in fields["fmoney_code"], True
            )
            web.athena_base_page.assert_data(
                "編輯Panel外幣金額", fields["fmoney_amt"], str(foreign_amount)
            )
            web.athena_base_page.assert_data(
                "編輯Panel手續費", fields["service_amt"], str(service_amount)
            )
            web.athena_base_page.assert_data(
                "編輯Panel匯率有效", float(fields["buy_rate"].replace(",", "")) > 0, True
            )
            web.athena_base_page.assert_data(
                "編輯Panel兌換總額有效", float(fields["total_amt"].replace(",", "")) > 0, True
            )
            expected_tmoney = round(
                float(fields["total_amt"].replace(",", ""))
                - float(fields["service_amt"].replace(",", "")),
                2,
            )
            web.athena_base_page.assert_data(
                "編輯Panel兌換淨額守恆",
                round(float(fields["tmoney_amt"].replace(",", "")), 2),
                expected_tmoney,
            )
            web.athena_base_page.screenshot("Then 編輯 Panel 欄位值與新增輸入一致")
            # 關編輯 Panel 清殘留 mask
            web.athena_base_page.click(web.forex_exchange_page.locator.btn_close_panel)
            web.athena_base_page.sleep(1)
