import allure
import pytest

from pages.base_page import BasePage
from pages.components.share_panel_component import SharePanelComponent
from pages.components.tip_component import TipComponent
from pages.components.header_component import HeaderComponent
from pages.components.spare_parts_component import SparePartsComponent
from pages.components.spare_parts_batch_component import SparePartsBatchComponent
from pages.components.todolist_edit_component import TodolistEditComponent
from pages.dialogs.reservation_card_dialog import ReservationCardDialog
from pages.reservation_page import ReservationPage
from pages.room_assignment_page import RoomAssignmentPage
from tests.share_steps import ShareSteps
from tools.driver_helper import DriverHelper


@allure.feature("訂房明細")
class TestReservationDetail:

    @allure.story("新增櫃台備品-自動入帳")
    @pytest.mark.xdist_group("add_spare_parts_with_expense")
    @pytest.mark.dependency(name="test_add_spare_parts_with_expense", scope="session")
    def test_add_spare_parts_with_expense(self, logged_in_driver):
        pages = [
            ReservationCardDialog,
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            BasePage,
            SparePartsComponent,
        ]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        with allure.step("Given 使用者進入「訂房明細」視窗"):
            ShareSteps.to_reservation_detail(
                web, "訂房", "訂房卡", "guestName", "Card Test", "doOpenDtDetailDialog"
            )
            web.base_page.screenshot("Given 使用者進入「訂房明細」視窗")

        with allure.step("When 點擊右上的[櫃台備品]，進入「櫃台備品」視窗"):
            web.reservation_card_dialog.click_detail_toolbar("spareParts").sleep(2)
            web.base_page.screenshot("When 點擊右上的[櫃台備品]，進入「櫃台備品」視窗")

        with allure.step("And 刪除舊櫃台備品"):
            while web.spare_parts_component.check_spare_parts_exist():
                web.spare_parts_component.click_remove_spare_parts()
                web.tip_component.click_ok()
            web.base_page.screenshot("And 刪除舊櫃台備品")

        with allure.step("And 新增櫃台備品並儲存"):
            web.spare_parts_component.click_add_spare_parts()
            web.spare_parts_component.create_spare_parts("充電器")
            web.base_page.click_toolbar_with_icon("save").sleep(2)
            web.base_page.screenshot("And 新增櫃台備品並儲存")

        with allure.step("Then 顯示'儲存成功'提示"):
            ShareSteps.verify_save_success_tip(web)
            web.share_panel_component.close_panel("櫃台備品")

        with allure.step("And 驗證櫃台備品資料"):
            web.reservation_card_dialog.click_detail_toolbar("spareParts").sleep(2)
            web.spare_parts_component.click_spare_parts_row()
            web.base_page.screenshot("And 驗證櫃台備品資料")
            info_list = [
                ("櫃台備品", "itemCode", "充電器"),
                ("開始日期", "rentalStartDate", "2024/01/05"),
                ("結束日期", "checkoutDate", "2024/01/08"),
                ("數量", "amount", "1"),
                ("自動入帳", "appraiseIns", "Y : 是"),
                ("入交辦", "todoInsert", "N : 否"),
                ("單價", "appraiseUnitAmount", "200"),
                ("單日小計", "appraiseItemAmount", "200"),
            ]
            for title, label, target in info_list:
                web.base_page.assert_data(
                    title, web.spare_parts_component.get_spare_parts_info(label), target
                )

            web.base_page.assert_data(
                "1/5使用數量",
                web.spare_parts_component.get_spare_parts_table_info_by_date("2024/01/05"),
                ["2024/01/05", "70", "1", "69"],
            )
            web.base_page.assert_data(
                "1/6使用數量",
                web.spare_parts_component.get_spare_parts_table_info_by_date("2024/01/06"),
                ["2024/01/06", "70", "1", "69"],
            )
            web.base_page.assert_data(
                "1/7使用數量",
                web.spare_parts_component.get_spare_parts_table_info_by_date("2024/01/07"),
                ["2024/01/07", "70", "1", "69"],
            )

            web.share_panel_component.close_panel("櫃台備品")
            web.base_page.close_panel()

    @allure.story("驗證新增後的資料-服務項目、費用明細")
    @pytest.mark.xdist_group("add_spare_parts_with_expense")
    @pytest.mark.dependency(
        name="test_verify_data_of_add_spare_parts",
        depends=["test_add_spare_parts_with_expense"],
        scope="session",
    )
    def test_verify_data_of_add_spare_parts(self, logged_in_driver):
        pages = [
            ReservationCardDialog,
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            BasePage,
        ]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        with allure.step("Given 使用者進入「訂房明細」視窗"):
            ShareSteps.to_reservation_detail(
                web, "訂房", "訂房卡", "guestName", "Card Test", "doOpenDtDetailDialog"
            )
            web.base_page.screenshot("Given 使用者進入「訂房明細」視窗")

        with allure.step("And 驗證服務項目資料"):
            web.reservation_card_dialog.click_tab("service").sleep(1)
            web.base_page.screenshot("And 驗證服務項目資料")
            info_list = [
                ("服務類別", "commandOption", "****: ALL"),
                ("服務項目", "itemNos", "備品租借費用"),
                ("單價", "unitAmount", "200"),
                ("數量規則", "itemQntRule", "BY_ROOM: 房間數"),
                ("數量", "itemQuantity", "1"),
                ("服務方式", "servWay", "A: 指定日期"),
                ("開始日期", "beginDate", "2024/01/05 週五"),
                ("結束日期", "endDate", "2024/01/07 週日"),
                ("來源", "fromSys", "AMENITY: 櫃台備品"),
            ]
            for title, label, target in info_list:
                web.base_page.assert_data(
                    title, web.reservation_card_dialog.get_tab_service_info(label), target
                )

        with allure.step("And 驗證費用明細資料"):
            web.reservation_card_dialog.click_tab("expenseDetail")
            web.base_page.screenshot("And 驗證費用明細資料")
            info_list = [
                ("入帳日", "useDate", "2024/01/07 週日"),
                ("消費項目", "itemSna", "備品租借費用"),
                ("單價", "unitAmount", "200"),
                ("數量", "itemQnt", "1"),
                ("小計", "itemAmount", "200"),
                ("服務日", "servDate", "2024/01/07 週日"),
            ]
            for title, label, target in info_list:
                web.base_page.assert_data(
                    title,
                    web.reservation_card_dialog.get_tab_expense_info_in_row("2024/01/07", label),
                    target,
                )

            web.base_page.assert_data(
                "1/5有備品費用",
                web.reservation_card_dialog.get_tab_expense_info_by_date("2024/01/05"),
                ["房租", "Service Charge", "備品租借費用"],
            )
            web.base_page.assert_data(
                "1/6有備品費用",
                web.reservation_card_dialog.get_tab_expense_info_by_date("2024/01/06"),
                ["房租", "Service Charge", "備品租借費用"],
            )
            web.base_page.assert_data(
                "1/7有備品費用",
                web.reservation_card_dialog.get_tab_expense_info_by_date("2024/01/07"),
                ["房租", "Service Charge", "備品租借費用"],
            )
            web.base_page.assert_data(
                "其他費用",
                web.reservation_card_dialog.get_expense_summary_info("otherFeeValue"),
                "600",
            )

    @allure.story("編輯櫃台備品-縮短結束日期")
    @pytest.mark.xdist_group("add_spare_parts_with_expense")
    @pytest.mark.dependency(
        name="test_shorten_spare_parts_end_date",
        depends=["test_verify_data_of_add_spare_parts"],
        scope="session",
    )
    def test_shorten_spare_parts_end_date(self, logged_in_driver):
        pages = [
            ReservationCardDialog,
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            BasePage,
            SparePartsComponent,
        ]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        with allure.step("Given 使用者進入「訂房明細」視窗"):
            ShareSteps.to_reservation_detail(
                web, "訂房", "訂房卡", "guestName", "Card Test", "doOpenDtDetailDialog"
            )
            web.base_page.screenshot("Given 使用者進入「訂房明細」視窗")

        with allure.step("And 點擊右上的[櫃台備品]，進入「櫃台備品」視窗"):
            web.reservation_card_dialog.click_detail_toolbar("spareParts").sleep(2)
            web.base_page.screenshot("And 點擊右上的[櫃台備品]，進入「櫃台備品」視窗")

        with allure.step("And 編輯櫃台備品結束日期"):
            web.spare_parts_component.click_spare_parts_row().sleep(1)
            web.spare_parts_component.edit_spare_parts_end_date("checkoutDate", "Jan", "7")
            web.base_page.click_toolbar_with_icon("save").sleep(2)
            web.base_page.screenshot("And 編輯櫃台備品結束日期")

        with allure.step("Then 顯示'儲存成功'提示"):
            ShareSteps.verify_save_success_tip(web)
            web.share_panel_component.close_panel("櫃台備品")

        with allure.step("And 驗證櫃台備品資料"):
            web.reservation_card_dialog.click_detail_toolbar("spareParts").sleep(2)
            web.spare_parts_component.click_spare_parts_row()
            web.base_page.screenshot("And 驗證櫃台備品資料")
            info_list = [
                ("櫃台備品", "itemCode", "充電器"),
                ("開始日期", "rentalStartDate", "2024/01/05"),
                ("結束日期", "checkoutDate", "2024/01/07"),
                ("數量", "amount", "1"),
                ("自動入帳", "appraiseIns", "Y : 是"),
                ("入交辦", "todoInsert", "N : 否"),
                ("單價", "appraiseUnitAmount", "200"),
                ("單日小計", "appraiseItemAmount", "200"),
            ]
            for title, label, target in info_list:
                web.base_page.assert_data(
                    title, web.spare_parts_component.get_spare_parts_info(label), target
                )

            web.base_page.assert_data(
                "1/5使用數量",
                web.spare_parts_component.get_spare_parts_table_info_by_date("2024/01/05"),
                ["2024/01/05", "70", "1", "69"],
            )
            web.base_page.assert_data(
                "1/6使用數量",
                web.spare_parts_component.get_spare_parts_table_info_by_date("2024/01/06"),
                ["2024/01/06", "70", "1", "69"],
            )

            web.share_panel_component.close_panel("櫃台備品")
            web.base_page.close_panel()

    @allure.story("驗證縮短後的資料-服務項目、費用明細")
    @pytest.mark.xdist_group("add_spare_parts_with_expense")
    @pytest.mark.dependency(
        name="test_verify_data_of_shorten_spare_parts",
        depends=["test_shorten_spare_parts_end_date"],
        scope="session",
    )
    def test_verify_data_of_shorten_spare_parts(self, logged_in_driver):
        pages = [
            ReservationCardDialog,
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            BasePage,
        ]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        with allure.step("Given 使用者進入「訂房明細」視窗"):
            ShareSteps.to_reservation_detail(
                web, "訂房", "訂房卡", "guestName", "Card Test", "doOpenDtDetailDialog"
            )
            web.base_page.screenshot("Given 使用者進入「訂房明細」視窗")

        with allure.step("Then 驗證服務項目資料"):
            web.reservation_card_dialog.click_tab("service").sleep(1)
            web.base_page.screenshot("Then 驗證服務項目資料")
            info_list = [
                ("服務類別", "commandOption", "****: ALL"),
                ("服務項目", "itemNos", "備品租借費用"),
                ("單價", "unitAmount", "200"),
                ("數量規則", "itemQntRule", "BY_ROOM: 房間數"),
                ("數量", "itemQuantity", "1"),
                ("服務方式", "servWay", "A: 指定日期"),
                ("開始日期", "beginDate", "2024/01/05 週五"),
                ("結束日期", "endDate", "2024/01/06 週六"),
                ("來源", "fromSys", "AMENITY: 櫃台備品"),
            ]
            for title, label, target in info_list:
                web.base_page.assert_data(
                    title, web.reservation_card_dialog.get_tab_service_info(label), target
                )

        with allure.step("And 驗證費用明細資料"):
            web.reservation_card_dialog.click_tab("expenseDetail")
            web.base_page.screenshot("And 驗證費用明細資料")
            info_list = [
                ("入帳日", "useDate", "2024/01/06 週六"),
                ("消費項目", "itemSna", "備品租借費用"),
                ("單價", "unitAmount", "200"),
                ("數量", "itemQnt", "1"),
                ("小計", "itemAmount", "200"),
                ("服務日", "servDate", "2024/01/06 週六"),
            ]
            for title, label, target in info_list:
                web.base_page.assert_data(
                    title,
                    web.reservation_card_dialog.get_tab_expense_info_in_row("2024/01/06", label),
                    target,
                )

            web.base_page.assert_data(
                "1/5有備品費用",
                web.reservation_card_dialog.get_tab_expense_info_by_date("2024/01/05"),
                ["房租", "Service Charge", "備品租借費用"],
            )
            web.base_page.assert_data(
                "1/6有備品費用",
                web.reservation_card_dialog.get_tab_expense_info_by_date("2024/01/06"),
                ["房租", "Service Charge", "備品租借費用"],
            )
            web.base_page.assert_data(
                "1/7沒有備品費用",
                web.reservation_card_dialog.get_tab_expense_info_by_date("2024/01/07"),
                ["房租", "Service Charge"],
            )
            web.base_page.assert_data(
                "其他費用",
                web.reservation_card_dialog.get_expense_summary_info("otherFeeValue"),
                "400",
            )

    @allure.story("編輯櫃台備品-延長結束日期")
    @pytest.mark.xdist_group("add_spare_parts_with_expense")
    @pytest.mark.dependency(
        name="test_extend_spare_parts_end_date",
        depends=["test_verify_data_of_shorten_spare_parts"],
        scope="session",
    )
    def test_extend_spare_parts_end_date(self, logged_in_driver):
        pages = [
            ReservationCardDialog,
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            BasePage,
            SparePartsComponent,
        ]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        with allure.step("Given 使用者進入「訂房明細」視窗"):
            ShareSteps.to_reservation_detail(
                web, "訂房", "訂房卡", "guestName", "Card Test", "doOpenDtDetailDialog"
            )
            web.base_page.screenshot("Given 使用者進入「訂房明細」視窗")

        with allure.step("And 點擊右上的[櫃台備品]，進入「櫃台備品」視窗"):
            web.reservation_card_dialog.click_detail_toolbar("spareParts").sleep(2)
            web.base_page.screenshot("And 點擊右上的[櫃台備品]，進入「櫃台備品」視窗")

        with allure.step("And 編輯櫃台備品結束日期"):
            web.spare_parts_component.click_spare_parts_row().sleep(1)
            web.spare_parts_component.edit_spare_parts_end_date("checkoutDate", "Jan", "8")
            web.base_page.click_toolbar_with_icon("save").sleep(1)
            web.base_page.screenshot("And 編輯櫃台備品結束日期")

        with allure.step("Then 顯示'儲存成功'提示"):
            ShareSteps.verify_save_success_tip(web)
            web.share_panel_component.close_panel("櫃台備品")

        with allure.step("And 驗證櫃台備品資料"):
            web.reservation_card_dialog.click_detail_toolbar("spareParts").sleep(2)
            web.spare_parts_component.click_spare_parts_row()
            web.base_page.screenshot("And 驗證櫃台備品資料")
            info_list = [
                ("櫃台備品", "itemCode", "充電器"),
                ("開始日期", "rentalStartDate", "2024/01/05"),
                ("結束日期", "checkoutDate", "2024/01/08"),
                ("數量", "amount", "1"),
                ("自動入帳", "appraiseIns", "Y : 是"),
                ("入交辦", "todoInsert", "N : 否"),
                ("單價", "appraiseUnitAmount", "200"),
                ("單日小計", "appraiseItemAmount", "200"),
            ]
            for title, label, target in info_list:
                web.base_page.assert_data(
                    title, web.spare_parts_component.get_spare_parts_info(label), target
                )

            web.base_page.assert_data(
                "1/5使用數量",
                web.spare_parts_component.get_spare_parts_table_info_by_date("2024/01/05"),
                ["2024/01/05", "70", "1", "69"],
            )
            web.base_page.assert_data(
                "1/6使用數量",
                web.spare_parts_component.get_spare_parts_table_info_by_date("2024/01/06"),
                ["2024/01/06", "70", "1", "69"],
            )
            web.base_page.assert_data(
                "1/7使用數量",
                web.spare_parts_component.get_spare_parts_table_info_by_date("2024/01/07"),
                ["2024/01/07", "70", "1", "69"],
            )

            web.share_panel_component.close_panel("櫃台備品")
            web.base_page.close_panel()

    @allure.story("驗證延長後的資料-服務項目、費用明細")
    @pytest.mark.xdist_group("add_spare_parts_with_expense")
    @pytest.mark.dependency(
        name="test_verify_data_of_extend_spare_parts",
        depends=["test_extend_spare_parts_end_date"],
        scope="session",
    )
    def test_verify_data_of_extend_spare_parts(self, logged_in_driver):
        pages = [
            ReservationCardDialog,
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            BasePage,
        ]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        with allure.step("Given 使用者進入「訂房明細」視窗"):
            ShareSteps.to_reservation_detail(
                web, "訂房", "訂房卡", "guestName", "Card Test", "doOpenDtDetailDialog"
            )
            web.base_page.screenshot("Given 使用者進入「訂房明細」視窗")

        with allure.step("Then 驗證服務項目資料"):
            web.reservation_card_dialog.click_tab("service").sleep(1)
            web.base_page.screenshot("Then 驗證服務項目資料")
            info_list = [
                ("服務類別", "commandOption", "****: ALL"),
                ("服務項目", "itemNos", "備品租借費用"),
                ("單價", "unitAmount", "200"),
                ("數量規則", "itemQntRule", "BY_ROOM: 房間數"),
                ("數量", "itemQuantity", "1"),
                ("服務方式", "servWay", "A: 指定日期"),
                ("開始日期", "beginDate", "2024/01/05 週五"),
                ("結束日期", "endDate", "2024/01/07 週日"),
                ("來源", "fromSys", "AMENITY: 櫃台備品"),
            ]
            for title, label, target in info_list:
                web.base_page.assert_data(
                    title, web.reservation_card_dialog.get_tab_service_info(label), target
                )

        with allure.step("And 驗證費用明細資料"):
            web.reservation_card_dialog.click_tab("expenseDetail")
            web.base_page.screenshot("And 驗證費用明細資料")
            info_list = [
                ("入帳日", "useDate", "2024/01/07 週日"),
                ("消費項目", "itemSna", "備品租借費用"),
                ("單價", "unitAmount", "200"),
                ("數量", "itemQnt", "1"),
                ("小計", "itemAmount", "200"),
                ("服務日", "servDate", "2024/01/07 週日"),
            ]
            for title, label, target in info_list:
                web.base_page.assert_data(
                    title,
                    web.reservation_card_dialog.get_tab_expense_info_in_row("2024/01/07", label),
                    target,
                )

            web.base_page.assert_data(
                "1/5有備品費用",
                web.reservation_card_dialog.get_tab_expense_info_by_date("2024/01/05"),
                ["房租", "Service Charge", "備品租借費用"],
            )
            web.base_page.assert_data(
                "1/6有備品費用",
                web.reservation_card_dialog.get_tab_expense_info_by_date("2024/01/06"),
                ["房租", "Service Charge", "備品租借費用"],
            )
            web.base_page.assert_data(
                "1/7有備品費用",
                web.reservation_card_dialog.get_tab_expense_info_by_date("2024/01/07"),
                ["房租", "Service Charge", "備品租借費用"],
            )
            web.base_page.assert_data(
                "其他費用",
                web.reservation_card_dialog.get_expense_summary_info("otherFeeValue"),
                "600",
            )

    @allure.story("編輯櫃台備品-修改數量")
    @pytest.mark.xdist_group("add_spare_parts_with_expense")
    @pytest.mark.dependency(
        name="test_edit_spare_parts_amount",
        depends=["test_verify_data_of_extend_spare_parts"],
        scope="session",
    )
    def test_edit_spare_parts_amount(self, logged_in_driver):
        pages = [
            ReservationCardDialog,
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            BasePage,
            SparePartsComponent,
        ]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        with allure.step("Given 使用者進入「訂房明細」視窗"):
            ShareSteps.to_reservation_detail(
                web, "訂房", "訂房卡", "guestName", "Card Test", "doOpenDtDetailDialog"
            )
            web.base_page.screenshot("Given 使用者進入「訂房明細」視窗")

        with allure.step("And 點擊右上的[櫃台備品]，進入「櫃台備品」視窗"):
            web.reservation_card_dialog.click_detail_toolbar("spareParts").sleep(2)
            web.base_page.screenshot("And 點擊右上的[櫃台備品]，進入「櫃台備品」視窗")

        with allure.step("And 編輯櫃台備品數量"):
            web.spare_parts_component.click_spare_parts_row().sleep(1)
            web.spare_parts_component.edit_spare_parts_amount("amount", 80)
            web.base_page.click_toolbar_with_icon("save").sleep(1)
            amount_alert = web.tip_component.get_tip_text()
            web.tip_component.click_ok()
            web.spare_parts_component.edit_spare_parts_amount("amount", 2)
            web.base_page.click_toolbar_with_icon("save").sleep(1)
            web.base_page.screenshot("And 編輯櫃台備品數量")

        with allure.step("Then 顯示'儲存成功'提示"):
            ShareSteps.verify_save_success_tip(web)
            web.share_panel_component.close_panel("櫃台備品")

        with allure.step("And 驗證櫃台備品資料"):
            web.reservation_card_dialog.click_detail_toolbar("spareParts").sleep(2)
            web.spare_parts_component.click_spare_parts_row()
            web.base_page.screenshot("And 驗證櫃台備品資料")
            info_list = [
                ("櫃台備品", "itemCode", "充電器"),
                ("開始日期", "rentalStartDate", "2024/01/05"),
                ("結束日期", "checkoutDate", "2024/01/08"),
                ("數量", "amount", "2"),
                ("自動入帳", "appraiseIns", "Y : 是"),
                ("入交辦", "todoInsert", "N : 否"),
                ("單價", "appraiseUnitAmount", "200"),
                ("單日小計", "appraiseItemAmount", "400"),
            ]
            for title, label, target in info_list:
                web.base_page.assert_data(
                    title, web.spare_parts_component.get_spare_parts_info(label), target
                )

            web.base_page.assert_data(
                "1/5使用數量",
                web.spare_parts_component.get_spare_parts_table_info_by_date("2024/01/05"),
                ["2024/01/05", "70", "2", "68"],
            )
            web.base_page.assert_data(
                "1/6使用數量",
                web.spare_parts_component.get_spare_parts_table_info_by_date("2024/01/06"),
                ["2024/01/06", "70", "2", "68"],
            )
            web.base_page.assert_data(
                "1/7使用數量",
                web.spare_parts_component.get_spare_parts_table_info_by_date("2024/01/07"),
                ["2024/01/07", "70", "2", "68"],
            )
            web.base_page.assert_data(
                "數量超過提示",
                amount_alert,
                "異動後 充電器 於 2024/01/05 庫存數不足 "
                "異動後 充電器 於 2024/01/06 庫存數不足 "
                "異動後 充電器 於 2024/01/07 庫存數不足",
            )

            web.share_panel_component.close_panel("櫃台備品")
            web.base_page.close_panel()

    @allure.story("驗證修改數量後的資料-服務項目、費用明細")
    @pytest.mark.xdist_group("add_spare_parts_with_expense")
    @pytest.mark.dependency(
        name="test_verify_data_of_edit_spare_parts_amount",
        depends=["test_edit_spare_parts_amount"],
        scope="session",
    )
    def test_verify_data_of_edit_spare_parts_amount(self, logged_in_driver):
        pages = [
            ReservationCardDialog,
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            BasePage,
        ]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        with allure.step("Given 使用者進入「訂房明細」視窗"):
            ShareSteps.to_reservation_detail(
                web, "訂房", "訂房卡", "guestName", "Card Test", "doOpenDtDetailDialog"
            )
            web.base_page.screenshot("Given 使用者進入「訂房明細」視窗")

        with allure.step("Then 驗證服務項目資料"):
            web.reservation_card_dialog.click_tab("service").sleep(1)
            web.base_page.screenshot("Then 驗證服務項目資料")
            info_list = [
                ("服務類別", "commandOption", "****: ALL"),
                ("服務項目", "itemNos", "備品租借費用"),
                ("單價", "unitAmount", "200"),
                ("數量規則", "itemQntRule", "BY_ROOM: 房間數"),
                ("數量", "itemQuantity", "2"),
                ("服務方式", "servWay", "A: 指定日期"),
                ("開始日期", "beginDate", "2024/01/05 週五"),
                ("結束日期", "endDate", "2024/01/07 週日"),
                ("來源", "fromSys", "AMENITY: 櫃台備品"),
            ]
            for title, label, target in info_list:
                web.base_page.assert_data(
                    title, web.reservation_card_dialog.get_tab_service_info(label), target
                )

        with allure.step("And 驗證費用明細資料"):
            web.reservation_card_dialog.click_tab("expenseDetail")
            web.base_page.screenshot("And 驗證費用明細資料")
            info_list = [
                ("入帳日", "useDate", "2024/01/07 週日"),
                ("消費項目", "itemSna", "備品租借費用"),
                ("單價", "unitAmount", "200"),
                ("數量", "itemQnt", "2"),
                ("小計", "itemAmount", "400"),
                ("服務日", "servDate", "2024/01/07 週日"),
            ]
            for title, label, target in info_list:
                web.base_page.assert_data(
                    title,
                    web.reservation_card_dialog.get_tab_expense_info_in_row("2024/01/07", label),
                    target,
                )

            web.base_page.assert_data(
                "1/5有備品費用",
                web.reservation_card_dialog.get_tab_expense_info_by_date("2024/01/05"),
                ["房租", "Service Charge", "備品租借費用"],
            )
            web.base_page.assert_data(
                "1/6有備品費用",
                web.reservation_card_dialog.get_tab_expense_info_by_date("2024/01/06"),
                ["房租", "Service Charge", "備品租借費用"],
            )
            web.base_page.assert_data(
                "1/7有備品費用",
                web.reservation_card_dialog.get_tab_expense_info_by_date("2024/01/07"),
                ["房租", "Service Charge", "備品租借費用"],
            )
            web.base_page.assert_data(
                "其他費用",
                web.reservation_card_dialog.get_expense_summary_info("otherFeeValue"),
                "1200",
            )

    @allure.story("刪除櫃台備品-自動入帳")
    @pytest.mark.xdist_group("add_spare_parts_with_expense")
    @pytest.mark.dependency(
        name="test_delete_spare_parts_with_expense",
        depends=["test_verify_data_of_edit_spare_parts_amount"],
        scope="session",
    )
    def test_delete_spare_parts_with_expense(self, logged_in_driver):
        pages = [
            ReservationCardDialog,
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            BasePage,
            SparePartsComponent,
        ]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        with allure.step("Given 使用者進入「訂房明細」視窗"):
            ShareSteps.to_reservation_detail(
                web, "訂房", "訂房卡", "guestName", "Card Test", "doOpenDtDetailDialog"
            )
            web.base_page.screenshot("Given 使用者進入「訂房明細」視窗")

        with allure.step("And 點擊右上的[櫃台備品]，進入「櫃台備品」視窗"):
            web.reservation_card_dialog.click_detail_toolbar("spareParts").sleep(2)
            web.base_page.screenshot("And 點擊右上的[櫃台備品]，進入「櫃台備品」視窗")

        with allure.step("And 點擊左側表格中的[紅色減號]，顯示'確定刪除此筆資料'訊息"):
            web.spare_parts_component.click_remove_spare_parts()
            del_message = web.tip_component.get_tip_text()
            web.base_page.screenshot("And 點擊左側表格中的[紅色減號]，顯示'確定刪除此筆資料'訊息")

        with allure.step("And 點擊[確定]，訊息視窗消失"):
            web.tip_component.click_ok()
            web.base_page.screenshot("And 點擊[確定]，訊息視窗消失")

        with allure.step("And 點擊[橘色磁碟片]進行儲存"):
            ShareSteps.click_btn_save(web)

        with allure.step("Then 顯示'儲存成功'提示"):
            ShareSteps.verify_save_success_tip(web)
            web.share_panel_component.close_panel("櫃台備品")
            web.reservation_card_dialog.click_detail_toolbar("save").sleep(1)
            web.tip_component.click_ok()

        with allure.step("And 驗證櫃台備品資料已被刪除"):
            web.reservation_card_dialog.click_detail_toolbar("spareParts").sleep(2)
            web.base_page.screenshot("And 驗證櫃台備品資料已被刪除")
            web.base_page.assert_data(
                "櫃台備品資料已被刪除", web.spare_parts_component.check_spare_parts_exist(), False
            )
            web.base_page.assert_data("刪除訊息正確", del_message, "確定刪除此筆資料")
            web.share_panel_component.close_panel("櫃台備品")

        with allure.step("And 驗證服務項目沒有資料"):
            web.reservation_card_dialog.click_tab("service").sleep(1)
            web.base_page.screenshot("And 驗證服務項目沒有資料")
            web.base_page.assert_data(
                "服務項目資料已被刪除",
                web.reservation_card_dialog.get_tab_empty_msg("service"),
                "無任何資料",
            )

        with allure.step("And 驗證費用明細沒有資料"):
            web.reservation_card_dialog.click_tab("expenseDetail")
            web.base_page.screenshot("And 驗證費用明細沒有資料")
            web.base_page.assert_data(
                "1/5沒有備品費用",
                web.reservation_card_dialog.get_tab_expense_info_by_date("2024/01/05"),
                ["房租", "Service Charge"],
            )
            web.base_page.assert_data(
                "1/6沒有備品費用",
                web.reservation_card_dialog.get_tab_expense_info_by_date("2024/01/06"),
                ["房租", "Service Charge"],
            )
            web.base_page.assert_data(
                "1/7沒有備品費用",
                web.reservation_card_dialog.get_tab_expense_info_by_date("2024/01/07"),
                ["房租", "Service Charge"],
            )
            web.base_page.assert_data(
                "其他費用",
                web.reservation_card_dialog.get_expense_summary_info("otherFeeValue"),
                "0",
            )

    @allure.story("新增櫃台備品-入交辦")
    @pytest.mark.xdist_group("add_spare_parts_with_todo")
    @pytest.mark.dependency(name="test_add_spare_parts_with_todo", scope="session")
    def test_add_spare_parts_with_todo(self, logged_in_driver):
        pages = [
            ReservationCardDialog,
            ReservationPage,
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            BasePage,
            SparePartsComponent,
            TodolistEditComponent,
        ]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        with allure.step("Given 使用者進入「訂房明細」視窗"):
            ShareSteps.create_or_enter_reservation_detail(
                web,
                "guestName",
                "Card Todo",
                "doOpenDtDetailDialog",
                "Card",
                "Todo",
                "現場訂房含早",
                4,
            )
            web.base_page.screenshot("Given 使用者進入「訂房明細」視窗")

        with allure.step("And 點擊右上的[櫃台備品]，進入「櫃台備品」視窗"):
            web.reservation_card_dialog.click_detail_toolbar("spareParts").sleep(2)
            web.base_page.screenshot("And 點擊右上的[櫃台備品]，進入「櫃台備品」視窗")

        with allure.step("And 刪除舊櫃台備品"):
            while web.spare_parts_component.check_spare_parts_exist():
                web.spare_parts_component.click_remove_spare_parts()
                web.tip_component.click_ok().sleep(1)
            web.base_page.screenshot("And 刪除舊櫃台備品")

        with allure.step("And 新增櫃台備品並儲存"):
            web.spare_parts_component.click_add_spare_parts()
            web.spare_parts_component.create_spare_parts("除濕機")
            web.base_page.click_toolbar_with_icon("save").sleep(1)
            web.base_page.screenshot("And 新增櫃台備品並儲存")

        with allure.step("Then 顯示'儲存成功'提示"):
            ShareSteps.verify_save_success_tip(web)
            web.share_panel_component.close_panel("櫃台備品")

        with allure.step("And 驗證櫃台備品資料"):
            web.reservation_card_dialog.click_detail_toolbar("spareParts").sleep(2)
            web.spare_parts_component.click_spare_parts_row()
            web.base_page.screenshot("And 驗證櫃台備品資料")
            info_list = [
                ("櫃台備品", "itemCode", "除濕機"),
                ("開始日期", "rentalStartDate", "2024/01/05"),
                ("結束日期", "checkoutDate", "2024/01/06"),
                ("數量", "amount", "1"),
                ("自動入帳", "appraiseIns", "N : 否"),
                ("入交辦", "todoInsert", "Y : 是"),
                ("處理部門", "todoDeptCode", "西餐廳"),
                ("單價", "appraiseUnitAmount", "0"),
                ("單日小計", "appraiseItemAmount", "0"),
            ]
            for title, label, target in info_list:
                web.base_page.assert_data(
                    title, web.spare_parts_component.get_spare_parts_info(label), target
                )

            web.base_page.assert_data(
                "1/5使用數量",
                web.spare_parts_component.get_spare_parts_table_info_by_date("2024/01/05"),
                ["2024/01/05", "10", "1", "9"],
            )
            web.share_panel_component.close_panel("櫃台備品").sleep(1)

        with allure.step("And 驗證交辦事項"):
            web.reservation_card_dialog.click_tab("guest")
            web.reservation_card_dialog.click_tab_toolbar("guest", "編輯")
            web.reservation_card_dialog.click_tab_guest_function("todoListButton").sleep(1)
            web.base_page.screenshot("And 驗證交辦事項")
            info_list = [
                ("處理狀態", "proc_sta", "N"),
                ("開始日期", "begin_dat", "2024/01/05"),
                ("結束日期", "end_dat", "2024/01/05"),
                ("處理部門", "dept_sna", "西餐廳"),
                ("交辦內容", "todo_rmk", "除濕機 QTY:1"),
            ]
            for title, label, target in info_list:
                web.base_page.assert_data(
                    title, web.todolist_edit_component.get_todolist_info(label), target
                )

    @allure.story("刪除櫃台備品-入交辦")
    @pytest.mark.xdist_group("add_spare_parts_with_todo")
    @pytest.mark.dependency(
        name="test_delete_spare_parts_with_todo",
        depends=["test_add_spare_parts_with_todo"],
        scope="session",
    )
    def test_delete_spare_parts_with_todo(self, logged_in_driver):
        pages = [
            ReservationCardDialog,
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            BasePage,
            SparePartsComponent,
            TodolistEditComponent,
        ]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        with allure.step("Given 使用者進入「訂房明細」視窗"):
            ShareSteps.create_or_enter_reservation_detail(
                web, "quickSearch", "Card Todo", "doOpenDtDetailDialog"
            )
            web.base_page.screenshot("Given 使用者進入「訂房明細」視窗")

        with allure.step("And 點擊右上的[櫃台備品]，進入「櫃台備品」視窗"):
            web.reservation_card_dialog.click_detail_toolbar("spareParts").sleep(2)
            web.base_page.screenshot("And 點擊右上的[櫃台備品]，進入「櫃台備品」視窗")

        with allure.step("And 點擊左側表格中的[紅色減號]，顯示'確定刪除此筆資料'訊息"):
            web.spare_parts_component.click_remove_spare_parts()
            del_message = web.tip_component.get_tip_text()
            web.base_page.screenshot("And 點擊左側表格中的[紅色減號]，顯示'確定刪除此筆資料'訊息")

        with allure.step("And 點擊[確定]，訊息視窗消失"):
            web.tip_component.click_ok()
            web.base_page.screenshot("And 點擊[確定]，訊息視窗消失")

        with allure.step("And 點擊[橘色磁碟片]進行儲存"):
            ShareSteps.click_btn_save(web)

        with allure.step("Then 顯示'儲存成功'提示"):
            ShareSteps.verify_save_success_tip(web)
            web.share_panel_component.close_panel("櫃台備品")

        with allure.step("And 驗證櫃台備品資料已被刪除"):
            web.reservation_card_dialog.click_detail_toolbar("spareParts").sleep(2)
            web.base_page.screenshot("And 驗證櫃台備品資料已被刪除")
            web.base_page.assert_data(
                "櫃台備品資料已被刪除", web.spare_parts_component.check_spare_parts_exist(), False
            )
            web.base_page.assert_data("刪除訊息正確", del_message, "確定刪除此筆資料")
            web.share_panel_component.close_panel("櫃台備品").sleep(1)

        with allure.step("And 驗證交辦事項不受影響"):
            web.reservation_card_dialog.click_tab("guest").sleep(2)
            web.reservation_card_dialog.click_tab_toolbar("guest", "編輯").sleep(2)
            web.reservation_card_dialog.click_tab_guest_function("todoListButton").sleep(2)
            web.base_page.screenshot("And 驗證交辦事項不受影響")
            info_list = [
                ("處理狀態", "proc_sta", "N"),
                ("開始日期", "begin_dat", "2024/01/05"),
                ("結束日期", "end_dat", "2024/01/05"),
                ("處理部門", "dept_sna", "西餐廳"),
                ("交辦內容", "todo_rmk", "除濕機 QTY:1"),
            ]
            for title, label, target in info_list:
                web.base_page.assert_data(
                    title, web.todolist_edit_component.get_todolist_info(label), target
                )

    @allure.story("備品批次新增櫃台備品-入交辦")
    @pytest.mark.xdist_group("add_spare_parts_with_todo")
    @pytest.mark.dependency(
        name="test_batch_spare_add_with_todo",
        depends=["test_delete_spare_parts_with_todo"],
        scope="session",
    )
    def test_batch_spare_add_with_todo(self, logged_in_driver):
        pages = [
            ReservationCardDialog,
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            BasePage,
            SparePartsBatchComponent,
        ]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        with allure.step("Given 使用者進入「備品批次」視窗"):
            ShareSteps.create_or_enter_reservation_detail(
                web, "guestName", "Card Todo", "doOpenBatchSpareInsert"
            )
            web.base_page.screenshot("Given 使用者進入「備品批次」視窗")

        with allure.step("And 點擊[+]新增一筆櫃台備品"):
            web.reservation_card_dialog.click_btn_add()
            web.reservation_card_dialog.click_btn_add()
            web.spare_parts_batch_component.create_batch_spare("Baby Cot")
            info_list = [
                ("櫃台備品", "itemCode", "BC: Baby Cot"),
                ("開始日期", "rentalStartDate", "2024/01/05"),
                ("結束日期", "rentalEndDate", "2024/01/06"),
                ("自動入帳", "appraiseIns", "否"),
                ("數量", "amount", "1"),
                ("單價", "appraiseUnitAmount", "0"),
                ("單日小計", "appraiseItemAmount", "0"),
                ("入交辦", "todoInsert", "是"),
                ("處理部門", "todoDeptCode", "西餐廳"),
            ]
            real_values = [
                web.spare_parts_batch_component.get_batch_spare_info(key) for _, key, _ in info_list
            ]
            web.base_page.screenshot("And 點擊[+]新增一筆櫃台備品")

        with allure.step("And 勾選一筆住客資料"):
            web.spare_parts_batch_component.click_checkbox_in_guest()
            web.base_page.screenshot("And 勾選一筆住客資料")

        with allure.step("And 點擊[橘色磁碟片]進行儲存"):
            ShareSteps.click_btn_save(
                web,
                save_method=lambda: web.spare_parts_batch_component.click_save_batch_spare().sleep(
                    1
                ),
            )

        with allure.step("Then 顯示'儲存成功'提示"):
            ShareSteps.verify_save_success_tip(web)

        with allure.step("And 驗證備品批次帶入資訊正確"):
            web.base_page.screenshot("And 驗證備品批次帶入資訊正確")
            for i, (title, label, expected) in enumerate(info_list):
                web.base_page.assert_data(title, real_values[i], expected)

        with allure.step("And 驗證備品資訊正確"):
            web.reservation_card_dialog.click_spare_parts_info_toolbar("spareInfo").sleep(1)
            web.base_page.screenshot("And 驗證備品資訊正確")
            info_list = [
                ("狀態", "viewStatus", "Arrival"),
                ("住客姓名", "guestName", "Card Todo"),
                ("櫃台備品", "itemName", "Baby Cot"),
                ("開始日期", "amenityBeginDate", "2024/01/05"),
                ("結束日期", "amenityCheckoutDate", "2024/01/06"),
                ("數量", "itemQuantity", "1"),
                ("入住日期", "checkInDate", "2024/01/05"),
                ("退房日期", "checkOutDate", "2024/01/06"),
            ]
            for title, label, target in info_list:
                web.base_page.assert_data(
                    title, web.reservation_card_dialog.get_info_in_spare_parts_info(label), target
                )

    @allure.story("驗證備品批次新增的資料-入交辦")
    @pytest.mark.xdist_group("add_spare_parts_with_todo")
    @pytest.mark.dependency(
        name="test_verify_data_of_batch_spare_add_with_todo",
        depends=["test_batch_spare_add_with_todo"],
        scope="session",
    )
    def test_verify_data_of_batch_spare_add_with_todo(self, logged_in_driver):
        pages = [
            ReservationCardDialog,
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            BasePage,
            SparePartsComponent,
            TodolistEditComponent,
        ]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        with allure.step("Given 使用者進入「訂房明細」視窗"):
            ShareSteps.create_or_enter_reservation_detail(
                web, "guestName", "Card Todo", "doOpenDtDetailDialog"
            )
            web.base_page.screenshot("Given 使用者進入「訂房明細」視窗")

        with allure.step("And 點擊右上的[櫃台備品]，進入「櫃台備品」視窗"):
            web.reservation_card_dialog.click_detail_toolbar("spareParts").sleep(2)
            web.base_page.screenshot("And 點擊右上的[櫃台備品]，進入「櫃台備品」視窗")

        with allure.step("And 驗證櫃台備品資料"):
            web.spare_parts_component.click_spare_parts_row()
            web.base_page.screenshot("And 驗證櫃台備品資料")
            info_list = [
                ("櫃台備品", "itemCode", "Baby Cot"),
                ("開始日期", "rentalStartDate", "2024/01/05"),
                ("結束日期", "checkoutDate", "2024/01/06"),
                ("數量", "amount", "1"),
                ("自動入帳", "appraiseIns", "N : 否"),
                ("入交辦", "todoInsert", "Y : 是"),
                ("單價", "appraiseUnitAmount", "0"),
                ("單日小計", "appraiseItemAmount", "0"),
                ("處理部門", "todoDeptCode", "西餐廳"),
            ]
            for title, label, target in info_list:
                web.base_page.assert_data(
                    title, web.spare_parts_component.get_spare_parts_info(label), target
                )
            web.share_panel_component.close_panel("櫃台備品").sleep(1)

        with allure.step("And 驗證交辦事項正確"):
            web.reservation_card_dialog.click_tab("guest").sleep(2)
            web.reservation_card_dialog.click_tab_toolbar("guest", "編輯").sleep(2)
            web.reservation_card_dialog.click_tab_guest_function("todoListButton").sleep(2)
            web.base_page.screenshot("And 驗證交辦事項正確")
            info_list = [
                ("處理狀態", "proc_sta", "N"),
                ("開始日期", "begin_dat", "2024/01/05"),
                ("結束日期", "end_dat", "2024/01/05"),
                ("處理部門", "dept_sna", "西餐廳"),
                ("交辦內容", "todo_rmk", "Baby Cot QTY:1"),
            ]
            for title, label, target in info_list:
                web.base_page.assert_data(
                    title, web.todolist_edit_component.get_todolist_info(label), target
                )

    @allure.story("查詢櫃台備品")
    @pytest.mark.xdist_group("other_sparts_part_test")
    @pytest.mark.parametrize(
        "search_type, selected_count", [("單選", 1), ("複選", 3), ("全選", "all")]
    )
    def test_search_spare_parts(self, logged_in_driver, search_type, selected_count):
        pages = [
            ReservationCardDialog,
            HeaderComponent,
            TipComponent,
            ReservationPage,
            BasePage,
            SparePartsComponent,
        ]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        with allure.step("Given 使用者進入「訂房明細」視窗"):
            ShareSteps.create_or_enter_reservation_detail(
                web, "guestName", "Card Search Spare Parts", "doOpenDtDetailDialog"
            )
            web.base_page.screenshot("Given 使用者進入「訂房明細」視窗")

        with allure.step("And 點擊右上的[櫃台備品]，進入「櫃台備品」視窗"):
            web.reservation_card_dialog.click_detail_toolbar("spareParts").sleep(2)
            web.base_page.screenshot("And 點擊右上的[櫃台備品]，進入「櫃台備品」視窗")

        with allure.step("And 點擊左上的[庫存查詢]，進入「備品庫存查詢」視窗"):
            web.spare_parts_component.click_spare_parts_toolbar("庫存查詢")
            web.base_page.screenshot("And 點擊左上的[庫存查詢]，進入「備品庫存查詢」視窗")

        with allure.step("And 點擊選擇欲查詢之內容<日期、備品篩選（可複選）>，並點擊頁面空白處"):
            web.reservation_card_dialog.click_spare_parts_filter().sleep(1)
            web.reservation_card_dialog.click_spare_parts_checkbox(target_num=selected_count)
            selected_spare_parts = web.reservation_card_dialog.get_spare_parts_selected(
                target_num=selected_count
            )
            web.reservation_card_dialog.click_spare_parts_filter().sleep(1)
            web.base_page.screenshot(
                "And 點擊選擇欲查詢之內容<日期、備品篩選（可複選）>，並點擊頁面空白處"
            )

        with allure.step(f"Then 依查詢條件顯示符合之篩選內容-{search_type}"):
            web.base_page.screenshot("Then 依查詢條件顯示符合之篩選內容")
            web.base_page.assert_data(
                "查詢結果",
                web.reservation_card_dialog.get_spare_parts_search_result(),
                selected_spare_parts,
            )

    @allure.story("新增排房備註")
    @pytest.mark.xdist_group("add_assign_note")
    @pytest.mark.dependency(name="test_add_room_assign_note", scope="session")
    def test_add_room_assign_note(self, logged_in_driver):
        pages = [
            ReservationCardDialog,
            HeaderComponent,
            TipComponent,
            ReservationPage,
            RoomAssignmentPage,
            BasePage,
        ]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        with allure.step("Given 使用者進入「訂房明細」視窗"):
            ShareSteps.create_or_enter_reservation_detail(
                web,
                "guestName",
                "Card Room Assign note",
                "doOpenDtDetailDialog",
                "Card",
                "Room Assign note",
                "現場訂房含早",
                3,
            )
            web.base_page.screenshot("Given 使用者進入「訂房明細」視窗")

        with allure.step("And 從左側表格中選擇一筆資料點擊[黑色鉛筆]"):
            web.reservation_card_dialog.click_edit_assign_notes()
            web.base_page.screenshot("And 從左側表格中選擇一筆資料點擊[黑色鉛筆]")

        with allure.step("And 點擊左側表格右方的[綠色加號]，進入「房間特色選單」視窗"):
            web.reservation_card_dialog.click_add_assign_notes().sleep(1)
            web.base_page.screenshot("And 點擊左側表格右方的[綠色加號]，進入「房間特色選單」視窗")

        with allure.step("And 點擊下方表格中的項目或自行輸入備註內容"):
            web.reservation_card_dialog.unselect_room_features()
            web.reservation_card_dialog.click_room_features(["面對馬路", "嬰兒床1"])
            web.base_page.screenshot("And 點擊下方表格中的項目或自行輸入備註內容")

        with allure.step("And 點擊「確認」，離開該視窗"):
            web.base_page.click_toolbar_item_2("確認").sleep(1)
            web.base_page.screenshot("And 點擊「確認」，離開該視窗")

        with allure.step("And 點擊左方的[黑色磁碟片]或頁面空白處，並點擊[橘色磁碟片]儲存"):
            web.reservation_card_dialog.click_save_assign_notes()
            web.reservation_card_dialog.click_detail_toolbar("save").sleep(1)
            web.tip_component.click_ok()
            web.base_page.close_panel()
            web.base_page.screenshot(
                "And 點擊左方的[黑色磁碟片]或頁面空白處，並點擊[橘色磁碟片]儲存"
            )

        with allure.step("Then 驗證排房備註資料"):
            web.reservation_card_dialog.click_card_toolbar("doOpenDtDetailDialog").sleep(1)
            web.base_page.screenshot("And 驗證排房備註資料")
            web.base_page.assert_data(
                "排房備住", web.reservation_card_dialog.get_assign_notes(), "面對馬路,嬰兒床1"
            )
            web.base_page.close_panel()

            web.reservation_card_dialog.click_card_toolbar("doOpenRoomAssignDialog").sleep(1)
            web.base_page.click_toolbar_item("彙總").sleep(1)
            web.base_page.assert_data(
                "排房備註icon", web.room_assignment_page.has_assign_rmk(), True
            )

    @allure.story("修改排房備註")
    @pytest.mark.xdist_group("add_assign_note")
    @pytest.mark.dependency(
        name="test_edit_room_assign_note", depends=["test_add_room_assign_note"], scope="session"
    )
    def test_edit_room_assign_note(self, logged_in_driver):
        pages = [ReservationCardDialog, HeaderComponent, TipComponent, RoomAssignmentPage, BasePage]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        with allure.step("Given 使用者進入「訂房明細」視窗"):
            ShareSteps.to_reservation_detail(
                web, "訂房", "訂房卡", "guestName", "Card Room Assign note", "doOpenDtDetailDialog"
            )
            web.base_page.screenshot("Given 使用者進入「訂房明細」視窗")

        with allure.step("And 從左側表格中選擇一筆資料點擊[黑色鉛筆]"):
            web.reservation_card_dialog.click_edit_assign_notes()
            web.base_page.screenshot("And 從左側表格中選擇一筆資料點擊[黑色鉛筆]")

        with allure.step("And 點擊左側表格右方的[綠色加號]，進入「房間特色選單」視窗"):
            web.reservation_card_dialog.click_add_assign_notes().sleep(1)
            web.base_page.screenshot("And 點擊左側表格右方的[綠色加號]，進入「房間特色選單」視窗")

        with allure.step("And 點擊下方表格中的項目或自行輸入備註內容"):
            web.reservation_card_dialog.unselect_room_features()
            web.reservation_card_dialog.click_room_features(["不要角落", "落地窗"])
            web.base_page.screenshot("And 點擊下方表格中的項目或自行輸入備註內容")

        with allure.step("And 點擊「確認」，離開該視窗"):
            web.base_page.click_toolbar_item_2("確認").sleep(1)
            web.base_page.screenshot("And 點擊「確認」，離開該視窗")

        with allure.step("And 點擊左方的[黑色磁碟片]或頁面空白處"):
            web.reservation_card_dialog.click_save_assign_notes()
            web.base_page.screenshot("And 點擊左方的[黑色磁碟片]或頁面空白處")

        with allure.step("And 點擊[橘色磁碟片]進行儲存"):
            ShareSteps.click_btn_save(
                web,
                save_method=lambda: web.reservation_card_dialog.click_detail_toolbar("save").sleep(
                    1
                ),
            )

        with allure.step("Then 顯示'儲存成功'提示"):
            ShareSteps.verify_save_success_tip(web)
            web.base_page.close_panel()

        with allure.step("And 驗證排房備註資料"):
            web.reservation_card_dialog.click_card_toolbar("doOpenDtDetailDialog").sleep(1)
            web.base_page.screenshot("And 驗證排房備註資料")
            web.base_page.assert_data(
                "排房備住", web.reservation_card_dialog.get_assign_notes(), "不要角落,落地窗"
            )
            web.base_page.close_panel()

        with allure.step("And 驗證排房作業的圖示"):
            web.reservation_card_dialog.click_card_toolbar("doOpenRoomAssignDialog").sleep(1)
            web.base_page.click_toolbar_item("彙總").sleep(1)
            web.base_page.screenshot("And 驗證排房作業的圖示")
            web.base_page.assert_data(
                "排房備註icon", web.room_assignment_page.has_assign_rmk(), True
            )

    @allure.story("團體名單調整住客")
    def test_group_list_edit_guest(self, logged_in_driver):
        pages = [
            ReservationCardDialog,
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            RoomAssignmentPage,
            BasePage,
        ]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        with allure.step("Given 使用者進入「訂房明細」視窗"):
            ShareSteps.to_reservation_detail(
                web, "訂房", "訂房卡", "guestName", "Card Group List", "doOpenDtDetailDialog"
            )
            web.base_page.screenshot("Given 使用者進入「訂房明細」視窗")

        with allure.step("And 點擊右上的[團體名單]，進入「團體名單」視窗"):
            web.reservation_card_dialog.click_detail_toolbar("groupList").sleep(2)
            web.base_page.screenshot("And 點擊右上的[團體名單]，進入「團體名單」視窗")

        with allure.step("And 點擊左側表格中欲調整的訂房明細，並點擊兩表格中間的[>]，將人員移出"):
            label = ["roomNos", "useCod", "ci_dat", "co_dat", "customers"]
            first_guest_info = {
                key: web.reservation_card_dialog.get_group_list_row_info(1, key) for key in label
            }
            second_guest_info = {
                key: web.reservation_card_dialog.get_group_list_row_info(2, key) for key in label
            }
            web.reservation_card_dialog.click_group_list_row("1")
            web.reservation_card_dialog.click_move_guest("right")
            web.reservation_card_dialog.click_group_list_row("2")
            web.reservation_card_dialog.click_move_guest("right")
            web.base_page.screenshot(
                "And 點擊左側表格中欲調整的訂房明細，並點擊兩表格中間的[>]，將人員移出"
            )

        with allure.step(
            "And 點擊左側表格中另一個訂房明細及右側表格中的人員名單，並點擊兩表格中間的[<]，匯入人員名單"
        ):
            web.reservation_card_dialog.click_group_list_guest()
            web.reservation_card_dialog.click_group_list_row("2")
            web.reservation_card_dialog.click_move_guest("left")
            web.reservation_card_dialog.click_group_list_guest()
            web.reservation_card_dialog.click_group_list_row("1")
            web.reservation_card_dialog.click_move_guest("left")
            web.base_page.screenshot(
                "And 點擊左側表格中另一個訂房明細及右側表格中的人員名單，並點擊兩表格中間的[<]，匯入人員名單"
            )

        with allure.step("And 點擊[橘色磁碟片]進行儲存"):
            web.reservation_card_dialog.click_toolbar_with_icon("save").sleep(1)
            web.base_page.screenshot("And 點擊[橘色磁碟片]進行儲存")

        with allure.step("Then 顯示'儲存成功'提示"):
            ShareSteps.verify_save_success_tip(web)
            web.share_panel_component.close_panel("團體名單")

        with allure.step("And 「團體管理」視窗中，顯示調整過的資訊"):
            web.reservation_card_dialog.click_detail_toolbar("groupList").sleep(2)
            web.base_page.screenshot("And 「團體管理」視窗中，顯示調整過的資訊")
            first_info_list = [
                ("房號", "roomNos", first_guest_info["roomNos"]),
                ("房型", "useCod", first_guest_info["useCod"]),
                ("入住日期", "ci_dat", first_guest_info["ci_dat"]),
                ("退房日期", "co_dat", first_guest_info["co_dat"]),
                ("住客姓名", "customers", second_guest_info["customers"]),
            ]
            for title, label, target in first_info_list:
                web.base_page.assert_data(
                    title, web.reservation_card_dialog.get_group_list_row_info(1, label), target
                )

            second_info_list = [
                ("房號", "roomNos", second_guest_info["roomNos"]),
                ("房型", "useCod", second_guest_info["useCod"]),
                ("入住日期", "ci_dat", second_guest_info["ci_dat"]),
                ("退房日期", "co_dat", second_guest_info["co_dat"]),
                ("住客姓名", "customers", first_guest_info["customers"]),
            ]
            for title, label, target in second_info_list:
                web.base_page.assert_data(
                    title, web.reservation_card_dialog.get_group_list_row_info(2, label), target
                )
