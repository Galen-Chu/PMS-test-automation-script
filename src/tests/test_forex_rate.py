import allure
import pytest
from pages.athena_base_page import AthenaBasePage
from pages.components.header_component import HeaderComponent
from pages.components.share_panel_component import SharePanelComponent
from pages.components.tip_component import TipComponent
from pages.forex_rate_page import ForexRatePage
from tests.share_steps import ShareSteps
from tools.driver_helper import DriverHelper
from tools.test_data_helper import get_test_data, resolve_date


@allure.feature("外幣匯率異動")
class TestForexRate:

    @allure.story("外幣匯率異動 - 新增外幣匯率")
    @pytest.mark.xdist_group("test_forex_rate")
    @pytest.mark.dependency(name="test_add_forex_rate", scope="session")
    def test_add_forex_rate(self, logged_in_driver):
        data = get_test_data("test_forex_rate", "add_forex_rate")
        currency = data["currency"]
        buy_rate = data["buy_rate"]
        service_amt = data["service_amt"]

        pages = [ForexRatePage, HeaderComponent, TipComponent, SharePanelComponent, AthenaBasePage]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        with allure.step("Given 使用者進入「外幣匯率異動」頁面"):
            web.header_component.expand_menu("出納").sleep(1)
            web.header_component.to_func_page("外幣匯率異動").sleep(1)
            # 未開班觸發開班 dialog 攔截（首次/跨日 session 可能未開班）
            if web.athena_base_page.has_element(web.forex_rate_page.locator.dialog_shift):
                ShareSteps.open_shift(web, "FO : 飯店櫃檯", "a", "autotest")
                web.athena_base_page.sleep(1)
            # 頁面初始空資料，doSearch 才載入既有匯率
            web.athena_base_page.search().sleep(1)
            web.athena_base_page.screenshot("Given 使用者進入「外幣匯率異動」頁面")

        with allure.step("Given 復原：若有同幣別殘留 row 則刪除"):
            if web.forex_rate_page.has_currency_row(currency):
                web.forex_rate_page.remove_currency_row(currency)
                web.athena_base_page.click_toolbar_with_icon("save").sleep(1)
                web.tip_component.click_ok().sleep(1)
            web.athena_base_page.screenshot("Given 復原：若有同幣別殘留 row 則刪除")

        with allure.step("When 點擊[橘色加號]"):
            web.athena_base_page.click_toolbar_with_icon("add").sleep(1)
            web.athena_base_page.screenshot("When 點擊[橘色加號]")

        with allure.step("And 點擊[匯入幣別代號]欄位選擇<匯入幣別代號>"):
            web.forex_rate_page.select_currency(currency).sleep(0.5)
            web.athena_base_page.screenshot("And 點擊[匯入幣別代號]欄位選擇<匯入幣別代號>")

        with allure.step("And 點擊[匯率]欄位輸入<匯率>"):
            web.forex_rate_page.input_buy_rate(buy_rate)
            web.athena_base_page.screenshot("And 點擊[匯率]欄位輸入<匯率>")

        with allure.step("And 點擊[手續費金額]輸入<手續費金額>"):
            web.forex_rate_page.input_service_amt(service_amt)
            web.athena_base_page.screenshot("And 點擊[手續費金額]輸入<手續費金額>")

        with allure.step("And 點擊[橘色磁碟片]進行儲存"):
            web.athena_base_page.click_toolbar_with_icon("save").sleep(1)
            web.athena_base_page.screenshot("And 點擊[橘色磁碟片]進行儲存")

        with allure.step("Then 顯示「儲存成功」提示"):
            tip_text = web.tip_component.get_tip_text()
            web.athena_base_page.assert_data("儲存成功提示", "儲存成功" in tip_text, True)
            web.athena_base_page.screenshot("Then 顯示「儲存成功」提示")
            web.tip_component.click_ok().sleep(1)

        with allure.step("Then 「外幣匯率異動」頁面新增一筆資料列"):
            web.athena_base_page.search().sleep(1)
            row_fmoney = web.forex_rate_page.get_row_field(currency, "fmoneyCode")
            row_tmoney = web.forex_rate_page.get_row_field(currency, "tmoneyCode")
            row_buy_rate = web.forex_rate_page.get_row_field(currency, "buyRate")
            row_service = web.forex_rate_page.get_row_field(currency, "serviceAmt")
            row_batch_date = web.forex_rate_page.get_row_field(currency, "batchDate")
            web.athena_base_page.assert_data("新增資料列匯入幣別", currency in row_fmoney, True)
            web.athena_base_page.assert_data("新增資料列匯出幣別預設TWD", "TWD" in row_tmoney, True)
            web.athena_base_page.assert_data("新增資料列匯率", float(row_buy_rate), float(buy_rate))
            web.athena_base_page.assert_data(
                "新增資料列手續費", float(row_service), float(service_amt)
            )
            web.athena_base_page.assert_data(
                "新增資料列生效日期", row_batch_date, resolve_date("+0")
            )
            web.athena_base_page.screenshot("Then 「外幣匯率異動」頁面新增一筆資料列")

        with allure.step("Postcondition 刪除新增資料列（還原列表）"):
            web.forex_rate_page.remove_currency_row(currency)
            web.athena_base_page.click_toolbar_with_icon("save").sleep(1)
            web.tip_component.click_ok().sleep(1)
            web.athena_base_page.screenshot("Postcondition 刪除新增資料列（還原列表）")
