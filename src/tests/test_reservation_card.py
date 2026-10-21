import allure
import names
import pytest

from pages.base_page import BasePage
from pages.components.header_component import HeaderComponent
from pages.components.share_panel_component import SharePanelComponent
from pages.components.tip_component import TipComponent
from pages.dialogs.reservation_card_dialog import ReservationCardDialog
from pages.reservation_page import ReservationPage
from pages.room_assignment_page import RoomAssignmentPage
from tests.share_steps import ShareSteps
from tools.driver_helper import DriverHelper
from tools.random_helper import RandomHelper


@allure.feature("訂房卡單筆")
class TestReservationCard:

    @allure.story("建立訂房卡 - 新增住客為已存在住客歷史，要跳提示")
    @pytest.mark.parametrize(
        "guest_history_field", ["姓+名", "姓名", "證件號碼", "手機", "電子郵件"]
    )
    def test_create_reservation_card_with_existing_guest_history(
        self, logged_in_driver, guest_history_field
    ):
        pages = [BasePage, HeaderComponent, TipComponent, ReservationPage, ReservationCardDialog]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        with allure.step("Given 開啟訂房卡頁面"):
            web.header_component.expand_menu("訂房").sleep(1)
            web.header_component.to_func_page("訂房卡").sleep(2)
            web.reservation_page.screenshot("Given 開啟訂房卡頁面")

        with allure.step("When 使用者開啟一筆「訂房卡」"):
            web.reservation_card_dialog.click_btn_add().sleep(1)
            web.reservation_page.screenshot("When 使用者開啟一筆「訂房卡」")

        with allure.step("And 點擊姓名欄位旁邊[...]"):
            web.reservation_page.click_edit_guest().sleep(3)
            web.reservation_page.screenshot("And 點擊姓名欄位旁邊[...]")

        with allure.step(f"And 輸入住客歷史的{guest_history_field}"):
            first_name = "Sunny"
            last_name = "Yang"
            id_number = "A123456789"
            phone = "0922551305"
            email = "baiquan.wang@gmail.com"

            # 根據不同的參數輸入對應的欄位
            if guest_history_field == "姓+名":
                web.base_page.set_value_by_data_field_id("first_nam", first_name)
                web.base_page.set_value_by_data_field_id("last_nam", last_name)
                web.base_page.click(web.reservation_page.locator.btn_save_guest)
            elif guest_history_field == "姓名":
                web.base_page.set_value_by_data_field_id("alt_nam", first_name + " " + last_name)
                web.base_page.click(web.reservation_page.locator.btn_save_guest)
            elif guest_history_field == "證件號碼":
                web.base_page.set_value_by_data_field_id("cust_idx.id_cod", id_number)
                web.base_page.click(web.reservation_page.locator.btn_save_guest)
            elif guest_history_field == "手機":
                web.base_page.set_value_by_data_field_id("cust_idx.mobile_nos", phone)
                web.base_page.click(web.reservation_page.locator.btn_save_guest)
            elif guest_history_field == "電子郵件":
                web.reservation_page.set_email(email)
                web.base_page.click(web.reservation_page.locator.btn_save_guest)

            web.reservation_page.screenshot(f"And 輸入住客歷史的{guest_history_field}")

        with allure.step("Then 跳出「住客歷史資料確認」視窗"):
            web.reservation_page.screenshot("Then 跳出「住客歷史資料確認」視窗")
            web.base_page.assert_data(
                "顯示住客歷史資料確認視窗",
                web.reservation_page.has_guest_data_confirm_dialog(),
                True,
            )

    @allure.story("編輯訂房卡 - 新增單筆訂金成功(不用發票)")
    @pytest.mark.parametrize("invoice_type", ["X : 已開", "N : 後開"])
    @pytest.mark.xdist_group("reservation_card_add_deposit")
    @pytest.mark.dependency(name="test_add_deposit_to_reservation_card_no_invoice", scope="session")
    def test_add_deposit_to_reservation_card_no_invoice(self, logged_in_driver, invoice_type):
        pages = [
            BasePage,
            HeaderComponent,
            SharePanelComponent,
            TipComponent,
            ReservationPage,
            ReservationCardDialog,
        ]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        with allure.step("Given 使用者進入「訂房明細」視窗"):
            web.header_component.expand_menu("訂房").sleep(1)
            web.header_component.to_func_page("訂房卡").sleep(1)
            web.reservation_card_dialog.search_reservation_card(
                "quickSearch", "Card Deposit Add"
            ).sleep(1)
            web.reservation_card_dialog.click_edit_reservation_card().sleep(3)
            web.base_page.screenshot("Given 使用者進入「訂房明細」視窗")

        with allure.step("When 點擊住客頁籤「已付訂金」欄位下方的[...]按鈕"):
            deposit_amo = web.reservation_page.get_deposit_amo()
            web.reservation_card_dialog.click_deposit_setting().sleep(2)
            web.base_page.screenshot("When 點擊住客頁籤「已付訂金」欄位下方的[...]按鈕")

        with allure.step("And 填寫開班作業必填欄位"):
            ShareSteps.open_shift(web, "FO : 飯店櫃檯", "a", "autotest")
            web.base_page.screenshot("And 填寫開班作業必填欄位")

        with allure.step("And 點擊[+]新增按鈕"):
            if deposit_amo != "":
                web.reservation_card_dialog.clear_deposit_nos()
            web.base_page.click_by_data_field("addButton").sleep(2)
            web.base_page.screenshot("And 點擊[+]新增按鈕")

        with allure.step(f"And 選擇欲變更發票開立方式為「{invoice_type}」"):
            web.reservation_card_dialog.select_invoice_method("發票開立方式", invoice_type).sleep(1)
            web.base_page.screenshot(f"And 選擇欲變更發票開立方式為「{invoice_type}」")

        with allure.step("And 輸入付款方式及金額"):
            web.reservation_card_dialog.select_payment_method("10:現  金").sleep(1)
            web.reservation_card_dialog.input_payment_amount("1000").sleep(1)
            web.base_page.screenshot("And 輸入付款方式及金額")

        with allure.step("Then 點擊[磁碟片]儲存"):
            web.base_page.click_toolbar_with_icon("save").sleep(1)
            web.base_page.screenshot("Then 點擊[磁碟片]儲存")

        with allure.step("And 顯示「儲存成功」訊息"):
            ShareSteps.verify_save_success_tip(web)
            web.base_page.screenshot("And 顯示「儲存成功」訊息")

        with allure.step("Then 點擊[磁碟片]儲存訂金明細"):
            web.base_page.click_by_data_field("saveButton").sleep(2)
            web.base_page.screenshot("Then 點擊[磁碟片]儲存訂金明細")

        with allure.step("And 顯示「儲存成功」訊息"):
            ShareSteps.verify_save_success_tip(web)

        with allure.step("Then 已付訂金欄位顯示金額"):
            deposit_nos = web.base_page.get_dropdown_input_value("depositNos")
            web.base_page.close_panel().sleep(2)
            panel_title = web.reservation_page.get_dialog_ikey()
            dialog_ikey = panel_title.split(":")[1].strip()
            deposit_amo = web.reservation_page.get_deposit_amo()
            web.base_page.screenshot("Then 已付訂金欄位顯示金額")
            web.base_page.assert_data("訂金編號", deposit_amo, "1000")

            web.base_page.close_panel()

        with allure.step("And 訂金帳戶維護有正確資料"):
            web.header_component.expand_menu("出納").sleep(1)
            web.header_component.to_func_page("訂金帳戶維護").sleep(1)
            web.base_page.set_value_by_label("訂金編號", deposit_nos)
            web.base_page.search()
            web.base_page.screenshot("And 訂金帳戶維護有正確資料")

            web.base_page.assert_data(
                "訂金編號", web.base_page.get_field_text("deposit_mn_deposit_nos"), deposit_nos
            )
            web.base_page.assert_data(
                "訂金狀態", web.base_page.get_field_text("deposit_mn_deposit_sta"), "N : 使用中"
            )
            web.base_page.assert_data(
                "姓名", web.base_page.get_field_text("deposit_mn_alt_nam"), "Card Deposit Add"
            )
            web.base_page.assert_data(
                "餘額", web.base_page.get_field_text("deposit_mn_banlance_amt"), "1,000"
            )
            web.base_page.assert_data(
                "發票開立方式", web.base_page.get_field_text("deposit_mn_uniinv_sta"), invoice_type
            )
            web.base_page.assert_data(
                "單號", web.base_page.get_field_text("deposit_mn_link_nos"), dialog_ikey
            )

    @allure.story("編輯訂房卡 - 新增單筆訂金成功(有發票)")
    @pytest.mark.xdist_group("reservation_card_add_deposit")
    @pytest.mark.dependency(
        name="test_add_deposit_to_reservation_card_has_invoice",
        depends=["test_add_deposit_to_reservation_card_no_invoice"],
        scope="session",
    )
    def test_add_deposit_to_reservation_card_has_invoice(self, logged_in_driver):
        pages = [
            BasePage,
            HeaderComponent,
            SharePanelComponent,
            TipComponent,
            ReservationPage,
            ReservationCardDialog,
        ]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        with allure.step("Given 使用者進入「訂房明細」視窗"):
            web.header_component.expand_menu("訂房").sleep(1)
            web.header_component.to_func_page("訂房卡").sleep(1)
            web.reservation_card_dialog.search_reservation_card(
                "quickSearch", "Card Deposit Add"
            ).sleep(1)
            web.reservation_card_dialog.click_edit_reservation_card().sleep(2)
            web.base_page.screenshot("Given 使用者進入「訂房明細」視窗")

        with allure.step("When 點擊住客頁籤「已付訂金」欄位下方的[...]按鈕"):
            deposit_amo = web.reservation_page.get_deposit_amo()
            web.reservation_card_dialog.click_deposit_setting().sleep(2)
            web.base_page.screenshot("When 點擊住客頁籤「已付訂金」欄位下方的[...]按鈕")

        with allure.step("And 填寫開班作業必填欄位"):
            ShareSteps.open_shift(web, "FO : 飯店櫃檯", "a", "autotest")
            web.base_page.screenshot("And 填寫開班作業必填欄位")

        with allure.step("And 點擊[+]新增按鈕"):
            web.reservation_card_dialog.clear_deposit_nos()
            web.base_page.click_by_data_field("addButton").sleep(2)
            web.base_page.screenshot("And 點擊[+]新增按鈕")

        with allure.step("And 選擇欲變更發票開立方式為「Y : 先開」"):
            web.reservation_card_dialog.select_invoice_method("發票開立方式", "Y : 先開").sleep(1)
            web.base_page.screenshot("And 選擇欲變更發票開立方式為「Y : 先開」")

        with allure.step("And 輸入付款方式及金額"):
            web.reservation_card_dialog.select_payment_method("10:現  金").sleep(1)
            web.reservation_card_dialog.input_payment_amount("1000").sleep(1)
            web.base_page.screenshot("And 輸入付款方式及金額")

        with allure.step("And 點擊[磁碟片]儲存，並顯示發票載具視窗"):
            web.base_page.click_toolbar_with_icon("save").sleep(1)
            web.base_page.screenshot("And 點擊[磁碟片]儲存，並顯示發票載具視窗")
            web.share_panel_component.click_panel_footer_btn("發票載具", "確定").sleep(2)

        with allure.step("Then 顯示「儲存成功」訊息"):
            ShareSteps.verify_save_success_tip(web)
            web.tip_component.click_ok().sleep(1)

        with allure.step("And 點擊[磁碟片]儲存訂金明細"):
            web.base_page.click_by_data_field("saveButton").sleep(2)
            web.base_page.screenshot("And 點擊[磁碟片]儲存訂金明細")

        with allure.step("Then 顯示「儲存成功」訊息"):
            ShareSteps.verify_save_success_tip(web)

        with allure.step("And 已付訂金欄位顯示金額"):
            deposit_nos = web.base_page.get_dropdown_input_value("depositNos")
            web.base_page.close_panel().sleep(2)
            panel_title = web.reservation_page.get_dialog_ikey()
            dialog_ikey = panel_title.split(":")[1].strip()
            deposit_amo = web.reservation_page.get_deposit_amo()
            web.base_page.screenshot("And 已付訂金欄位顯示金額")
            web.base_page.assert_data("訂金金額", deposit_amo, "1000")
            web.base_page.close_panel()

        with allure.step("And 訂金帳戶維護有正確資料"):
            web.header_component.expand_menu("出納").sleep(1)
            web.header_component.to_func_page("訂金帳戶維護").sleep(1)
            web.base_page.set_value_by_label("訂金編號", deposit_nos)
            web.base_page.search()
            web.base_page.screenshot("And 訂金帳戶維護有正確資料")

            web.base_page.assert_data(
                "訂金編號", web.base_page.get_field_text("deposit_mn_deposit_nos"), deposit_nos
            )
            web.base_page.assert_data(
                "訂金狀態", web.base_page.get_field_text("deposit_mn_deposit_sta"), "N : 使用中"
            )
            web.base_page.assert_data(
                "姓名", web.base_page.get_field_text("deposit_mn_alt_nam"), "Card Deposit Add"
            )
            web.base_page.assert_data(
                "餘額", web.base_page.get_field_text("deposit_mn_banlance_amt"), "1,000"
            )
            web.base_page.assert_data(
                "發票開立方式", web.base_page.get_field_text("deposit_mn_uniinv_sta"), "Y : 先開"
            )
            web.base_page.assert_data(
                "單號", web.base_page.get_field_text("deposit_mn_link_nos"), dialog_ikey
            )

    @allure.story("編輯訂房卡 - 代入已存在訂金")
    @pytest.mark.xdist_group("reservation_card_add_deposit")
    @pytest.mark.dependency(
        name="test_load_existing_deposit_to_reservation_card",
        depends=["test_add_deposit_to_reservation_card_has_invoice"],
        scope="session",
    )
    def test_load_existing_deposit_to_reservation_card(self, logged_in_driver):
        pages = [
            BasePage,
            HeaderComponent,
            TipComponent,
            ReservationPage,
            ReservationCardDialog,
            SharePanelComponent,
        ]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        with allure.step("Given 使用者進入「訂房明細」視窗"):
            web.header_component.expand_menu("訂房").sleep(1)
            web.header_component.to_func_page("訂房卡").sleep(1)
            web.reservation_card_dialog.search_reservation_card(
                "quickSearch", "Card Deposit Add"
            ).sleep(1)
            web.reservation_card_dialog.click_edit_reservation_card().sleep(2)
            web.base_page.screenshot("Given 使用者進入「訂房明細」視窗")

        with allure.step("When 點擊住客頁籤「已付訂金」欄位下方的[...]按鈕"):
            web.reservation_card_dialog.click_deposit_setting().sleep(2)
            web.base_page.screenshot("When 點擊住客頁籤「已付訂金」欄位下方的[...]按鈕")

        with allure.step("And 填寫開班作業必填欄位"):
            ShareSteps.open_shift(web, "FO : 飯店櫃檯", "a", "autotest")
            web.base_page.screenshot("And 填寫開班作業必填欄位")

        with allure.step("And 點擊[訂金編號]下拉選單，選擇一筆已存在的訂金"):
            web.reservation_card_dialog.select_deposit_no("0000002203").sleep(1)
            web.base_page.screenshot("And 點擊[訂金編號]下拉選單，選擇一筆已存在的訂金")

        with allure.step("Then 點擊[磁碟片]儲存按鈕"):
            web.base_page.click_by_data_field("saveButton").sleep(2)
            web.base_page.screenshot("Then 點擊[磁碟片]儲存按鈕")

        with allure.step("And 顯示「儲存成功」訊息"):
            ShareSteps.verify_save_success_tip(web)

        with allure.step("And 按[X]關閉訂金明細視窗"):
            web.base_page.close_panel().sleep(2)
            web.base_page.screenshot("And 按[X]關閉訂金明細視窗")

        with allure.step("Then 已付訂金欄位顯示訂金金額"):
            deposit_amo = web.reservation_page.get_deposit_amo()
            web.base_page.screenshot("Then 已付訂金欄位顯示訂金金額")
            web.base_page.assert_data("已付訂金金額", deposit_amo, "10000")

    @allure.story("編輯訂房卡 - 新增關聯單號綁訂")
    @pytest.mark.xdist_group("test_edit_reservation_card")
    @pytest.mark.dependency(name="test_edit_reservation_card_add_link_nos", scope="session")
    def test_edit_reservation_card_add_link_nos(self, logged_in_driver):
        pages = [
            BasePage,
            HeaderComponent,
            SharePanelComponent,
            TipComponent,
            ReservationPage,
            ReservationCardDialog,
        ]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        with allure.step("Given 使用者進入「訂房卡」頁面"):
            web.header_component.expand_menu("訂房").sleep(1)
            web.header_component.to_func_page("訂房卡").sleep(1)
            web.base_page.screenshot("Given 使用者進入「訂房卡」頁面")

        with allure.step("When 開啟一筆訂房卡"):
            web.reservation_card_dialog.search_reservation_card("quickSearch", "test 123").sleep(1)
            web.reservation_card_dialog.click_edit_reservation_card().sleep(2)
            web.base_page.screenshot("When 開啟一筆訂房卡")

        with allure.step("And 點擊[關聯單號]按鈕"):
            web.reservation_card_dialog.click_link_nos_button().sleep(1)
            web.base_page.screenshot("And 點擊[關聯單號]按鈕")

        with allure.step("And 點擊[+]按鈕開啟新增關聯單號視窗"):
            if web.reservation_card_dialog.get_link_nos_in_dialog():
                web.reservation_card_dialog.click_link_nos_remove()
                web.base_page.click_toolbar_with_icon("save").sleep(1)
                web.tip_component.click_ok()
            web.reservation_card_dialog.click_link_nos_add_button().sleep(1)
            web.base_page.screenshot("And 點擊[+]按鈕開啟新增關聯單號視窗")

        with allure.step("And 搜尋要關聯的訂房卡資訊"):
            web.reservation_card_dialog.search_link_nos("00008235").sleep(1)
            web.base_page.screenshot("And 搜尋要關聯的訂房卡資訊")

        with allure.step("And 勾選要關聯的訂房卡資訊"):
            web.reservation_card_dialog.check_link_nos().sleep(1)
            web.base_page.screenshot("And 勾選要關聯的訂房卡資訊")

        with allure.step("And 點擊[確定]按鈕"):
            web.share_panel_component.click_panel_footer_btn("新增關聯單號", "確定").sleep(1)
            web.base_page.screenshot("And 點擊[確定]按鈕")

        with allure.step("Then 點擊[儲存]按鈕"):
            web.base_page.click_toolbar_with_icon("save").sleep(1)
            web.base_page.screenshot("Then 點擊[儲存]按鈕")

        with allure.step("And 顯示「儲存成功」訊息"):
            ShareSteps.verify_save_success_tip(web)
            web.share_panel_component.close_panel("關聯單號")
            link_nos = web.reservation_card_dialog.get_link_nos()
            web.base_page.close_panel()

        with allure.step("And 驗證關聯單號綁定成功"):
            web.reservation_card_dialog.click_edit_reservation_card().sleep(2)
            web.base_page.assert_data("關聯單號", link_nos, "00008234")
            web.base_page.screenshot("And 驗證關聯單號綁定成功")

    @allure.story("編輯訂房卡 - 排房成功")
    @pytest.mark.xdist_group("test_edit_reservation_card")
    @pytest.mark.dependency(
        name="test_edit_assign_room",
        depends=["test_edit_reservation_card_add_link_nos"],
        scope="session",
    )
    def test_edit_assign_room(self, logged_in_driver):
        pages = [
            BasePage,
            HeaderComponent,
            TipComponent,
            ReservationPage,
            ReservationCardDialog,
            RoomAssignmentPage,
            SharePanelComponent,
        ]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110040")

        with allure.step("Given 使用者進入「訂房卡」頁面"):
            web.header_component.expand_menu("訂房").sleep(1)
            web.header_component.to_func_page("訂房卡").sleep(1)
            web.base_page.screenshot("Given 使用者進入「訂房卡」頁面")

        with allure.step("And 使用者開啟一筆「訂房卡」"):
            web.reservation_card_dialog.search_reservation_card("quickSearch", "test 123").sleep(1)
            web.reservation_card_dialog.click_edit_reservation_card().sleep(2)
            web.base_page.screenshot("And 使用者開啟一筆「訂房卡」")

        with allure.step("When 點擊[排房]"):
            web.reservation_card_dialog.click_detail_toolbar("doOpenRoomAssignDialog").sleep(2)
            web.base_page.screenshot("When 點擊[排房]")

        with allure.step("And 切換明細頁籤，並點擊[房號]"):
            web.base_page.click_toolbar_item("彙總").sleep(1)
            if web.room_assignment_page.get_text_in_detail_tab("room_nos"):
                web.room_assignment_page.click_room_sta_checkbox()
                web.tip_component.click_ok().sleep(2)
            web.room_assignment_page.select_room_no("211")
            web.base_page.screenshot("And 切換明細頁籤，並點擊[房號]")

        with allure.step("And 點擊[X]關閉排房視窗"):
            web.share_panel_component.close_panel("排房")
            web.base_page.screenshot("And 點擊[X]關閉排房視窗")

        with allure.step("And 點擊[磁碟片]儲存"):
            web.reservation_page.save_card().sleep(1)
            web.base_page.screenshot("And 點擊[磁碟片]儲存")

        with allure.step("Then 顯示'儲存成功'訊息"):
            ShareSteps.verify_save_success_tip(web)
            web.base_page.close_panel()

        with allure.step("And 重新開啟訂房卡顯示正確資訊"):
            web.reservation_card_dialog.click_edit_reservation_card().sleep(2)
            web.reservation_card_dialog.click_tab("Detail")
            web.base_page.screenshot("And 重新開啟訂房卡顯示正確資訊")

            web.base_page.assert_data(
                "房號", web.reservation_card_dialog.get_text_in_tab("roomNos"), "211"
            )

    @allure.story("建立訂房卡 - 公帳號")
    def test_create_reservation_card_with_folio(self, logged_in_driver):
        pages = [BasePage, HeaderComponent, TipComponent, ReservationPage, ReservationCardDialog]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        with allure.step("Given 開啟訂房卡頁面"):
            web.header_component.expand_menu("訂房").sleep(1)
            web.header_component.to_func_page("訂房卡").sleep(2)
            web.base_page.screenshot("Given 開啟訂房卡頁面")

        with allure.step("When 使用者開啟一筆「訂房卡」"):
            web.reservation_card_dialog.click_btn_add().sleep(1)
            web.base_page.screenshot("When 使用者開啟一筆「訂房卡」")

        with allure.step("And 勾選[使用公帳號]"):
            web.reservation_card_dialog.check_use_folio().sleep(1)
            web.base_page.screenshot("And 勾選[使用公帳號]")

        with allure.step("And 選擇[公帳號]"):
            web.base_page.click_by_data_field("masterNos")
            web.reservation_card_dialog.select_folio().sleep(1)
            folio = web.base_page.get_dropdown_input_value("masterNos")
            web.base_page.screenshot("And 選擇[公帳號]")

        with allure.step("And 填寫訂房卡必填欄位"):
            web.reservation_page.click_edit_guest().sleep(3)
            first_name = names.get_first_name()
            last_name = names.get_last_name()
            web.reservation_page.create_guest(
                first_name, last_name, "Miss.", RandomHelper.generate_phone_mobile()
            )
            web.tip_component.click_ok().sleep(1)
            web.reservation_card_dialog.click_edit_rate_cod()
            web.reservation_card_dialog.set_rate_code("現場訂房含早", "4").sleep(1)
            web.reservation_page.save_card()
            web.base_page.screenshot("And 填寫訂房卡必填欄位")

        with allure.step("Then 顯示「儲存成功」訊息"):
            ShareSteps.verify_save_success_tip(web)

        with allure.step("And 驗證公帳號正確"):
            panel_title = web.reservation_page.get_dialog_ikey()
            web.reservation_page.close_panel_by_title(panel_title).sleep(2)
            dialog_ikey = panel_title.split(":")[1].strip()

            web.reservation_card_dialog.search_reservation_card("ikey", dialog_ikey)
            web.base_page.assert_data(
                "公帳號", web.reservation_card_dialog.get_row_text("masterNos").split(":")[0], folio
            )
            web.base_page.screenshot("And 驗證公帳號正確")
