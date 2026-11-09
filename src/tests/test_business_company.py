import allure
import pytest
from pages.athena_base_page import AthenaBasePage
from pages.business_company_page import BusinessCompanyPage
from pages.co_list_page import CoListPage
from pages.components.company_panel_component import CompanyPanelComponent
from pages.components.header_component import HeaderComponent
from pages.components.tip_component import TipComponent
from pages.components.share_panel_component import SharePanelComponent
from pages.guest_account_page import GuestAccountPage
from tools.driver_helper import DriverHelper
from tools.test_data_helper import get_group_data, get_test_data
from tests.share_steps import ShareSteps

# EasyUI calendar 月份代碼（日期值來自 test_data，月份跟著解析不寫死）
MONTH_CODE = {
    "01": "Jan",
    "02": "Feb",
    "03": "Mar",
    "04": "Apr",
    "05": "May",
    "06": "Jun",
    "07": "Jul",
    "08": "Aug",
    "09": "Sep",
    "10": "Oct",
    "11": "Nov",
    "12": "Dec",
}


@allure.feature("業務作業 - 商務公司合約")
class TestBusinessCompany:

    @allure.story("商務公司 - 新增合約")
    @pytest.mark.xdist_group("test_business_company")
    @pytest.mark.dependency(name="test_add_contract", scope="session")
    def test_add_contract(self, logged_in_driver):
        data = get_group_data("test_business_company")
        company_cod = data["company_cod"]
        contract_no = data["contract_no"]
        start_date = data["start_date"]
        end_date = data["end_date"]

        pages = [
            BusinessCompanyPage,
            CompanyPanelComponent,
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            AthenaBasePage,
        ]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        with allure.step("Given 使用者進入「商務公司」頁面"):
            ShareSteps.open_contract_tab(web, company_cod)
            web.athena_base_page.screenshot("Given 使用者進入「商務公司」頁面")

        with allure.step("Given 復原：合約 grid 有殘留合約則刪除"):
            if web.business_company_page.has_contract_row():
                web.company_panel_component.click_target_contract()
                web.company_panel_component.click_remove_contract().sleep(1)
                web.tip_component.click_btn_by_text("確定").sleep(1)
                web.company_panel_component.click_save().sleep(2)
                web.tip_component.click_ok().sleep(1)
                # save 後維護視窗自動關閉，重開進合約頁籤
                web.business_company_page.click_target_company(company_cod).sleep(1)
                web.business_company_page.open_maintain_panel().sleep(2)
                web.share_panel_component.click_detail_tab("contract").sleep(1)
            web.athena_base_page.screenshot("Given 復原：合約 grid 有殘留合約則刪除")

        with allure.step("When 點擊下方「合約」頁簽"):
            web.athena_base_page.screenshot("When 點擊下方「合約」頁簽")

        with allure.step("And 點擊[橘色+]"):
            web.company_panel_component.click_add_contract().sleep(1)
            web.athena_base_page.screenshot("And 點擊[橘色+]")

        with allure.step("And 點擊[合約編號]欄位輸入"):
            web.company_panel_component.input_contract_no_value(contract_no)
            web.athena_base_page.screenshot("And 點擊[合約編號]欄位輸入")

        with allure.step("And 點擊[開始日期]欄位選擇"):
            web.company_panel_component.select_start_day(
                start_date.split("/")[-1], MONTH_CODE[start_date.split("/")[1]]
            )
            web.athena_base_page.screenshot("And 點擊[開始日期]欄位選擇")

        with allure.step("And 點擊[結束日期]欄位選擇"):
            web.company_panel_component.select_end_day(
                end_date.split("/")[-1], MONTH_CODE[end_date.split("/")[1]]
            )
            web.athena_base_page.screenshot("And 點擊[結束日期]欄位選擇")

        with allure.step("And 點擊[館別]欄位選擇"):
            hotel_cod = web.business_company_page.pick_hotel()
            web.athena_base_page.screenshot("And 點擊[館別]欄位選擇")

        with allure.step("And 點擊[房價代號]欄位選擇"):
            rate_cod_text = web.business_company_page.pick_contract_combobox("rate_cod")
            web.athena_base_page.screenshot("And 點擊[房價代號]欄位選擇")

        with allure.step("And 點擊右上角[橘色磁碟片]儲存"):
            web.company_panel_component.click_save().sleep(2)
            web.athena_base_page.screenshot("And 點擊右上角[橘色磁碟片]儲存")

        with allure.step("Then 顯示「儲存成功」提示"):
            tip_text = web.tip_component.get_tip_text()
            web.athena_base_page.assert_data("新增合約儲存提示", tip_text, "儲存成功")
            web.athena_base_page.screenshot("Then 顯示「儲存成功」提示")
            web.tip_component.click_ok().sleep(1)

        with allure.step("Postcondition 重開驗證合約頁籤五欄位"):
            web.business_company_page.click_target_company(company_cod).sleep(1)
            web.business_company_page.open_maintain_panel().sleep(2)
            web.share_panel_component.click_detail_tab("contract").sleep(1)
            web.athena_base_page.screenshot("Postcondition 重開驗證合約頁籤五欄位")
            web.athena_base_page.assert_data(
                "合約-合約編號",
                web.company_panel_component.get_td_input_value("contract_cod"),
                contract_no,
            )
            web.athena_base_page.assert_data(
                "合約-開始日期",
                web.company_panel_component.get_td_input_value("begin_dat"),
                start_date,
            )
            web.athena_base_page.assert_data(
                "合約-結束日期", web.company_panel_component.get_td_input_value("end_dat"), end_date
            )
            web.athena_base_page.assert_data(
                "合約-館別", web.company_panel_component.get_td_input_value("hotel_cod"), hotel_cod
            )
            web.athena_base_page.assert_data(
                "合約-房價代號",
                web.company_panel_component.get_td_input_value("rate_cod"),
                rate_cod_text,
            )
            web.share_panel_component.close_panel("商務公司維護")

    @allure.story("商務公司 - 修改合約")
    @pytest.mark.xdist_group("test_business_company")
    @pytest.mark.dependency(
        name="test_modify_contract", depends=["test_add_contract"], scope="session"
    )
    @pytest.mark.parametrize(
        "data_key", ["modify_rate_cod", "modify_remark1", "modify_source_typ", "modify_guest_typ"]
    )
    def test_modify_contract(self, logged_in_driver, data_key):
        data = get_test_data("test_business_company", data_key)
        field = data["field"]
        group = get_group_data("test_business_company")
        company_cod = group["company_cod"]
        contract_no = group["contract_no"]

        pages = [
            BusinessCompanyPage,
            CompanyPanelComponent,
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            AthenaBasePage,
        ]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        with allure.step("Given 使用者進入「商務公司」頁面"):
            ShareSteps.open_contract_tab(web, company_cod)
            web.athena_base_page.screenshot("Given 使用者進入「商務公司」頁面")

        with allure.step("When 點擊「合約」頁簽"):
            web.athena_base_page.screenshot("When 點擊「合約」頁簽")

        with allure.step("And 點擊合約資料進入 inline 編輯"):
            web.business_company_page.click_contract_cell_to_edit(contract_no).sleep(1)
            web.athena_base_page.screenshot("And 點擊合約資料進入 inline 編輯")

        with allure.step(f"And 選擇調整欄位[{field}]"):
            if field == "remark1":
                new_value = data["new_value"]
                web.business_company_page.type_remark1(new_value)
            else:
                # 排除當前值取第一個可用選項，保證修改前後有差異
                current = web.company_panel_component.get_td_input_value(field)
                new_value = web.business_company_page.pick_contract_combobox(field, exclude=current)
            web.athena_base_page.screenshot(f"And 選擇調整欄位[{field}]")

        with allure.step("And 點擊[橘色磁碟片]儲存"):
            web.company_panel_component.click_save().sleep(2)
            web.athena_base_page.screenshot("And 點擊[橘色磁碟片]儲存")

        with allure.step("Then 顯示「儲存成功」提示"):
            tip_text = web.tip_component.get_tip_text()
            web.athena_base_page.assert_data(f"修改{field}儲存提示", tip_text, "儲存成功")
            web.athena_base_page.screenshot("Then 顯示「儲存成功」提示")
            web.tip_component.click_ok().sleep(1)

        with allure.step("Postcondition 重開驗證修改欄位值保留"):
            web.business_company_page.click_target_company(company_cod).sleep(1)
            web.business_company_page.open_maintain_panel().sleep(2)
            web.share_panel_component.click_detail_tab("contract").sleep(1)
            web.athena_base_page.screenshot("Postcondition 重開驗證修改欄位值保留")
            # 重開後 row 為純顯示態，統一走 td/div 讀值（與新增驗證同路徑）
            actual = web.company_panel_component.get_td_input_value(field)
            web.athena_base_page.assert_data(f"合約-{field}修改保留", actual, new_value)
            web.share_panel_component.close_panel("商務公司維護")

    @allure.story("商務公司 - 刪除合約")
    @pytest.mark.xdist_group("test_business_company")
    @pytest.mark.dependency(
        name="test_remove_contract", depends=["test_modify_contract"], scope="session"
    )
    def test_remove_contract(self, logged_in_driver):
        data = get_group_data("test_business_company")
        company_cod = data["company_cod"]

        pages = [
            BusinessCompanyPage,
            CompanyPanelComponent,
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            AthenaBasePage,
        ]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        with allure.step("Given 使用者進入「商務公司」頁面"):
            ShareSteps.open_contract_tab(web, company_cod)
            web.athena_base_page.screenshot("Given 使用者進入「商務公司」頁面")

        with allure.step("When 點擊「合約」頁簽"):
            web.athena_base_page.screenshot("When 點擊「合約」頁簽")

        with allure.step("And 點擊合約資料列"):
            web.company_panel_component.click_target_contract()
            web.athena_base_page.screenshot("And 點擊合約資料列")

        with allure.step("And 點擊[橘色-]"):
            web.company_panel_component.click_remove_contract().sleep(1)
            web.athena_base_page.screenshot("And 點擊[橘色-]")

        with allure.step("Then 顯示「確定刪除此筆資料」並點擊[確定]"):
            tip_text = web.tip_component.get_tip_text()
            web.athena_base_page.assert_data("刪除合約確認提示", tip_text, "確定刪除此筆資料")
            web.athena_base_page.screenshot("Then 顯示「確定刪除此筆資料」並點擊[確定]")
            web.tip_component.click_btn_by_text("確定").sleep(1)

        with allure.step("Postcondition 儲存並驗證合約資料列已移除"):
            web.company_panel_component.click_save().sleep(2)
            web.tip_component.click_ok().sleep(1)
            web.business_company_page.click_target_company(company_cod).sleep(1)
            web.business_company_page.open_maintain_panel().sleep(2)
            web.share_panel_component.click_detail_tab("contract").sleep(1)
            web.athena_base_page.screenshot("Postcondition 儲存並驗證合約資料列已移除")
            web.athena_base_page.assert_data(
                "合約資料列移除", str(web.business_company_page.has_contract_row()), "False"
            )
            web.share_panel_component.close_panel("商務公司維護")


@allure.feature("業務作業 - 商務公司簽帳")
class TestSignPay:
    """#601（Suite #49 商務公司）：簽帳設定鏈的端到端驗證。

    設定（3701 已實設可簽帳）+ 訂房卡/排房/入住為手動前置；測試驗證
    結帳時簽帳付款方式自動帶入。與合約三案分 group：操作主體在住客帳
    維護（co_list 基建），且 601 房資源與商務公司頁無衝突，不綁序列化。
    完整結帳流程（付款存入/發票）由 #496 客戶簽帳變體覆蓋，此處不結帳。"""

    @allure.story("結帳時，帶入簽帳付款方式，且結帳成功")
    @pytest.mark.xdist_group("test_sign_pay")
    def test_checkout_with_sign_pay(self, logged_in_driver):
        data = get_group_data("test_sign_pay")
        room = data["room"]
        company_cod = data["company_cod"]

        pages = [
            GuestAccountPage,
            CoListPage,
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            AthenaBasePage,
        ]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        with allure.step("Given 使用者進入「住客帳維護」頁面"):
            web.header_component.expand_menu("出納").sleep(1)
            web.header_component.to_func_page("住客帳維護").sleep(1)
            web.athena_base_page.screenshot("Given 使用者進入「住客帳維護」頁面")

        with allure.step("And 點擊[放大鏡]搜尋有訂房公司之住客"):
            web.guest_account_page.search_room(room).sleep(1)
            web.athena_base_page.screenshot("And 點擊[放大鏡]搜尋有訂房公司之住客")

        with allure.step("And 點擊有訂房公司之住客資料列"):
            web.guest_account_page.click_card_row(room).sleep(1)
            web.athena_base_page.screenshot("And 點擊有訂房公司之住客資料列")

        with allure.step("When 點擊[住客帳維護單筆]"):
            web.guest_account_page.click_guest_maintain().sleep(1)
            if web.guest_account_page.has_element(web.guest_account_page.locator.dialog_shift):
                ShareSteps.open_shift(web, "FO : 飯店櫃檯", "a", "autotest")
                web.guest_account_page.sleep(1)
            web.athena_base_page.screenshot("When 點擊[住客帳維護單筆]")

        with allure.step("Given 復原：帳務 K:關帳則開帳（前次中斷在關帳）"):
            if not web.co_list_page.is_account_open():
                web.co_list_page.click_toggle_account().sleep(1)
                web.athena_base_page.wait_visible(web.tip_component.locator.btn_alert_ok)
                web.tip_component.click_ok().sleep(1)
                web.athena_base_page.wait_visible(web.tip_component.locator.btn_alert_ok)
                web.tip_component.click_ok().sleep(1)
            web.athena_base_page.screenshot("Given 復原：帳務 K:關帳則開帳（前次中斷在關帳）")

        with allure.step("And 點擊[結帳]"):
            web.co_list_page.click_checkout_toolbar().sleep(1)
            web.athena_base_page.screenshot("And 點擊[結帳]")

        with allure.step("And 點擊[確認]關帳"):
            web.athena_base_page.wait_visible(web.tip_component.locator.btn_alert_ok)
            web.tip_component.click_ok().sleep(1)
            web.athena_base_page.wait_visible(web.tip_component.locator.btn_alert_ok)
            web.tip_component.click_ok().sleep(1)
            web.athena_base_page.screenshot("And 點擊[確認]關帳")

        with allure.step("Then 顯示「結帳」視窗"):
            web.athena_base_page.wait_visible(web.co_list_page.locator.dialog_checkout)
            web.athena_base_page.assert_data(
                "結帳視窗",
                str(web.athena_base_page.has_element(web.co_list_page.locator.dialog_checkout)),
                "True",
            )
            web.athena_base_page.screenshot("Then 顯示「結帳」視窗")

        with allure.step("And 顯示「請輸入付款方式」視窗"):
            web.athena_base_page.wait_visible(web.co_list_page.locator.dialog_payment)
            web.athena_base_page.assert_data(
                "請輸入付款方式視窗",
                str(web.athena_base_page.has_element(web.co_list_page.locator.dialog_payment)),
                "True",
            )
            web.athena_base_page.screenshot("And 顯示「請輸入付款方式」視窗")

        with allure.step("Then 付款方式自動帶入簽帳 41"):
            pay_way = web.co_list_page.get_pay_way_value()
            web.athena_base_page.assert_data("付款方式為簽帳 41", pay_way, "41:客戶簽帳(要開)")
            web.athena_base_page.screenshot("Then 付款方式自動帶入簽帳 41")

        with allure.step("And 簽帳公司自動帶入訂房公司"):
            # 公司名是環境資料，驗代號前綴（'代號:名稱' 格式）
            cust_cod = web.co_list_page.get_sign_cust_cod_value()
            web.athena_base_page.assert_data(
                "簽帳公司帶入", str(cust_cod.startswith(f"{company_cod}:")), "True"
            )
            web.athena_base_page.screenshot("And 簽帳公司自動帶入訂房公司")

        with allure.step("Postcondition 關閉視窗不結帳（簽帳結帳流程由 #496 覆蓋）"):
            web.co_list_page.close_sign_pay_dialogs(web.tip_component)
            web.athena_base_page.screenshot("Postcondition 關閉視窗不結帳")
