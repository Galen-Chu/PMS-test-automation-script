import allure
import pytest
from pages.athena_base_page import AthenaBasePage
from pages.components.header_component import HeaderComponent
from pages.components.tip_component import TipComponent
from pages.dialogs.pay_folio_dialog import PayFolioDialog
from pages.dialogs.reservation_card_dialog import ReservationCardDialog
from tools.driver_helper import DriverHelper
from tools.test_data_helper import get_group_data


@allure.feature("訂房作業 - 線上繳款單")
class TestPayFolio:

    @allure.story("訂房卡開啟[線上繳款單] - 新增單筆")
    @pytest.mark.xdist_group("test_pay_folio")
    def test_add_pay_folio(self, logged_in_driver):
        data = get_group_data("test_pay_folio")
        card_name = data["card_name"]
        pay_amount = data["pay_amount"]

        pages = [
            ReservationCardDialog,
            PayFolioDialog,
            HeaderComponent,
            TipComponent,
            AthenaBasePage,
        ]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        with allure.step("Given 使用者進入「訂房卡」頁面並搜尋目標卡"):
            web.header_component.expand_menu("訂房").sleep(1)
            web.header_component.to_func_page("訂房卡").sleep(1)
            web.reservation_card_dialog.search_reservation_card("guestName", card_name).sleep(1)
            web.athena_base_page.screenshot("Given 使用者進入「訂房卡」頁面並搜尋目標卡")

        with allure.step("And 開啟訂房卡編輯視窗"):
            web.reservation_card_dialog.click_edit_reservation_card().sleep(2)
            web.athena_base_page.screenshot("And 開啟訂房卡編輯視窗")

        with allure.step("When 點擊[線上繳款單]"):
            web.pay_folio_dialog.open_pay_folio_dialog().sleep(1)
            web.athena_base_page.screenshot("When 點擊[線上繳款單]")

        with allure.step("Given 復原：存在未取消帳單（N/F 筆）則選取刪除"):
            # 一卡一有效筆：殘留有效筆會擋 addButton（「存在未取消帳單」）
            if web.pay_folio_dialog.has_active_folio():
                web.pay_folio_dialog.select_first_active_folio().sleep(1)
                web.pay_folio_dialog.click_cancel().sleep(1)
            web.athena_base_page.screenshot("Given 復原：存在未取消帳單（N/F 筆）則選取刪除")

        with allure.step("And 選取已刪除(D)筆並點擊[新增]"):
            # D 筆不擋新增；addButton 需先選 D 筆才 enabled（雙層啟用邏輯）
            web.pay_folio_dialog.select_deleted_folio().sleep(1)
            web.pay_folio_dialog.click_add().sleep(1)
            web.athena_base_page.screenshot("And 選取已刪除(D)筆並點擊[新增]")

        with allure.step("Then 畫面新增一筆明細自動新增一筆"):
            web.athena_base_page.assert_data(
                "新增後明細筆數", str(web.pay_folio_dialog.get_grid_count("seqNos")), "1"
            )
            web.athena_base_page.screenshot("Then 畫面新增一筆明細自動新增一筆")

        with allure.step("And 主檔自動帶入應收訂金/狀態/繳款人"):
            field_pay_amount = web.pay_folio_dialog.get_field_value("payAmount")
            folio_status = web.pay_folio_dialog.get_field_value("folioStatus")
            alt_name = web.pay_folio_dialog.get_field_value("altName")
            web.athena_base_page.assert_data("主檔-應收訂金", field_pay_amount, pay_amount)
            web.athena_base_page.assert_data("主檔-狀態(新增)", folio_status, "正常")
            web.athena_base_page.assert_data("主檔-繳款人", alt_name, card_name)
            web.athena_base_page.screenshot("And 主檔自動帶入應收訂金/狀態/繳款人")

        with allure.step("And 點擊[儲存]"):
            web.pay_folio_dialog.click_save().sleep(2)
            web.athena_base_page.screenshot("And 點擊[儲存]")

        with allure.step("Then 生成繳款單號且狀態轉為上傳失敗"):
            folio_nos = web.pay_folio_dialog.get_saved_folio_nos()
            web.athena_base_page.assert_data("繳款單號已生成", str(folio_nos != ""), "True")
            web.athena_base_page.assert_data(
                "主檔-狀態(存檔)", web.pay_folio_dialog.get_field_value("folioStatus"), "上傳失敗"
            )
            web.athena_base_page.screenshot("Then 生成繳款單號且狀態轉為上傳失敗")

        with allure.step("Postcondition 重開視窗驗證存檔資料"):
            web.pay_folio_dialog.close_dialog().sleep(1)
            web.pay_folio_dialog.open_pay_folio_dialog().sleep(1)
            # D 筆（歷次 cancel）不從 grid 消失，筆數隨輪數累積——以本筆單號選取驗存在
            web.pay_folio_dialog.select_folio_by_nos(folio_nos).sleep(1)
            web.athena_base_page.assert_data(
                "重開-應收訂金", web.pay_folio_dialog.get_field_value("payAmount"), pay_amount
            )
            web.athena_base_page.assert_data(
                "重開-繳款人", web.pay_folio_dialog.get_field_value("altName"), card_name
            )
            web.athena_base_page.assert_data(
                "重開-明細筆數", str(web.pay_folio_dialog.get_grid_count("seqNos")), "1"
            )
            web.athena_base_page.screenshot("Postcondition 重開視窗驗證存檔資料")

        with allure.step("Postcondition 選取本筆取消刪除（還原可重跑）"):
            web.pay_folio_dialog.click_cancel().sleep(1)
            web.athena_base_page.assert_data(
                "還原-狀態(刪除)", web.pay_folio_dialog.get_field_value("folioStatus"), "刪除"
            )
            web.pay_folio_dialog.close_dialog().sleep(1)
            web.athena_base_page.screenshot("Postcondition 選取本筆取消刪除（還原可重跑）")
