from datetime import datetime
import allure
import pytest
import names

from pages.base_page import BasePage
from pages.components.share_panel_component import SharePanelComponent
from pages.components.tip_component import TipComponent
from pages.components.header_component import HeaderComponent
from pages.components.service_item_component import ServiceItemComponent
from pages.components.transport_services_component import TransportServicesComponent
from pages.dialogs.reservation_card_dialog import ReservationCardDialog
from pages.reservation_page import ReservationPage
from tests.share_steps import ShareSteps

# pylint: disable=unused-import
from tests.dynamic_steps.service_item_step import (
    FirstDayServiceItemStep,
    DailyServiceItemStep,
    LastDayServiceItemStep,
    EveryFewDaysServiceItemStep,
    OnePlusEveryFewDaysServiceItemStep,
    WeeklyServiceItemStep,
    SpecifiedDateServiceItemStep,
)

# pylint: enable=unused-import
from tools.driver_helper import DriverHelper


@allure.feature("住客明細-服務")
class TestGuestServices:

    @allure.story("新增接送服務-接(自動入帳)")
    @pytest.mark.xdist_group("test_transport_service")
    @pytest.mark.dependency(name="test_add_transport_service_with_expense", scope="session")
    def test_add_transport_service_with_expense(self, cache):
        pages = [
            ReservationCardDialog,
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            ReservationPage,
            BasePage,
            TransportServicesComponent,
        ]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")

        with allure.step(
            "Given 使用者從「訂房」進入「訂房卡」頁面並進入「訂房明細」，然後點擊住客的黑色鉛筆"
        ):
            first_name = names.get_first_name()
            last_name = names.get_last_name()
            cache.set("full_name_transport", f"{first_name} {last_name}")
            ShareSteps.create_or_enter_reservation_detail(
                web,
                "guestName",
                f"{first_name} {last_name}",
                "doOpenDtDetailDialog",
                first_name,
                last_name,
                "現場訂房含早",
                3,
            )
            web.reservation_card_dialog.click_tab_toolbar("guest", "編輯")
            web.base_page.screenshot("Given 使用者進入「訂房明細」視窗，然後點擊住客的黑色鉛筆")

        with allure.step("And 點擊「接送」欄位的[綠色加號]，進入「接送服務編輯」視窗"):
            web.reservation_card_dialog.click_tab_guest_function("transferButton").sleep(2)

            initial_values = {
                "type": web.transport_services_component.get_transport_combobox_text("接/送"),
                "date": web.transport_services_component.get_transport_field_value("日期"),
                "company": web.transport_services_component.get_transport_field_direct_value(
                    "公司"
                ),
                "contact": web.transport_services_component.get_transport_field_direct_value(
                    "連絡人"
                ),
                "phone": web.transport_services_component.get_transport_field_direct_value("電話"),
                "guest": web.transport_services_component.get_transport_field_direct_value(
                    "指定住客"
                ),
                "guest_status": web.transport_services_component.get_transport_field_direct_value(
                    "住客帳狀態"
                ),
                "card_no": web.transport_services_component.get_transport_field_direct_value(
                    "訂房卡號"
                ),
                "checkin_date": web.transport_services_component.get_transport_field_value(
                    "入住日期"
                ),
                "checkout_date": web.transport_services_component.get_transport_field_value(
                    "退房日期"
                ),
            }

            web.base_page.screenshot("And 點擊「接送」欄位的[綠色加號]，進入「接送服務編輯」視窗")

        with allure.step("And 點擊下拉選單選擇或輸入必填欄位"):
            web.transport_services_component.set_transport_service("100").sleep(1)
            input_time = web.transport_services_component.get_transport_field_value("時間")
            web.base_page.screenshot("And 點擊下拉選單選擇或輸入必填欄位")

        with allure.step("And 點擊右上的[橘色磁碟片]儲存"):
            ShareSteps.click_btn_save(web)

        with allure.step("Then 顯示'儲存成功'訊息"):
            ShareSteps.verify_save_success_tip(web)
            web.share_panel_component.close_panel("接送服務編輯").sleep(1)
            web.reservation_card_dialog.click_detail_toolbar("save").sleep(1)
            web.tip_component.click_ok()
            web.base_page.close_panel()

        with allure.step("And 驗證接送服務表單欄位值正確"):
            web.reservation_card_dialog.click_card_toolbar("doOpenDtDetailDialog").sleep(1)
            web.reservation_card_dialog.click_tab_toolbar("guest", "編輯")
            web.reservation_card_dialog.click_tab_guest_function("transferButton").sleep(1)
            web.transport_services_component.click_transport_grid_last_row().sleep(1)
            web.base_page.screenshot("And 驗證接送服務表單欄位值正確")
            field_validations = [
                ("接/送", "combobox", "接/送", initial_values["type"]),
                ("日期", "field", "日期", initial_values["date"]),
                ("時間", "field", "時間", input_time),
                ("公司", "direct", "公司", initial_values["company"]),
                ("連絡人", "direct", "連絡人", initial_values["contact"]),
                ("電話", "direct", "電話", initial_values["phone"]),
                ("費用", "spinbutton", "費用", "100"),
                ("大人", "spinbutton", "大人", "2"),
                ("小孩", "spinbutton", "小孩", "0"),
                ("指定住客", "direct", "指定住客", initial_values["guest"]),
                ("住客帳狀態", "direct", "住客帳狀態", initial_values["guest_status"]),
                ("訂房卡號", "direct", "訂房卡號", initial_values["card_no"]),
                ("入住日期", "field", "入住日期", initial_values["checkin_date"]),
                ("退房日期", "field", "退房日期", initial_values["checkout_date"]),
                ("新增日期", "field", "新增日期", datetime.now().strftime("%Y/%m/%d")),
                ("新增者", "direct", "新增者", "autotest"),
                ("修改日期", "field", "修改日期", datetime.now().strftime("%Y/%m/%d")),
                ("修改者", "direct", "修改者", "autotest"),
            ]
            for title, method, field, expected in field_validations:
                if method == "field":
                    web.base_page.assert_data(
                        title,
                        web.transport_services_component.get_transport_field_value(field),
                        expected,
                    )
                elif method == "direct":
                    web.base_page.assert_data(
                        title,
                        web.transport_services_component.get_transport_field_direct_value(field),
                        expected,
                    )
                elif method == "spinbutton":
                    web.base_page.assert_data(
                        title,
                        web.transport_services_component.get_transport_spinbutton_value(field),
                        expected,
                    )
                elif method == "combobox":
                    web.base_page.assert_data(
                        title,
                        web.transport_services_component.get_transport_combobox_text(field),
                        expected,
                    )

        with allure.step("And 驗證接送服務表格資料正確"):
            web.base_page.screenshot("And 驗證接送服務表格資料正確")
            for title, col, expected in [
                ("接/送", "1", initial_values["type"]),
                ("日期", "2", initial_values["date"]),
                ("時間", "4", input_time),
            ]:
                web.base_page.assert_data(
                    title,
                    web.transport_services_component.get_transport_grid_cell_text(col),
                    expected,
                )

    @allure.story("驗證接送服務(接)資料-服務項目、費用明細")
    @pytest.mark.xdist_group("test_transport_service")
    @pytest.mark.dependency(
        name="test_verify_transport_service_expense",
        depends=["test_add_transport_service_with_expense"],
        scope="session",
    )
    def test_verify_transport_service_expense(self, cache):
        pages = [
            ReservationCardDialog,
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            ReservationPage,
            BasePage,
            TransportServicesComponent,
        ]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")
        full_name = cache.get("full_name_transport", "")

        with allure.step("Given 使用者從「訂房」進入「訂房卡」頁面並進入「訂房明細」視窗"):
            ShareSteps.create_or_enter_reservation_detail(
                web, "guestName", full_name, "doOpenDtDetailDialog"
            )
            web.base_page.screenshot("Given 使用者進入「訂房明細」視窗")

        with allure.step("When 驗證服務項目資料"):
            web.reservation_card_dialog.click_tab("service").sleep(1)
            web.base_page.screenshot("When 驗證服務項目資料")
            info_list = [
                ("服務類別", "commandOption", "****: ALL"),
                ("服務項目", "itemNos", "交通接駁(接)"),
                ("單價", "unitAmount", "100"),
                ("數量規則", "itemQntRule", "BY_ROOM: 房間數"),
                ("數量", "itemQuantity", "1"),
                ("服務方式", "servWay", "A: 指定日期"),
                ("開始日期", "beginDate", "2024/01/05 週五"),
                ("結束日期", "endDate", "2024/01/05 週五"),
                ("來源", "fromSys", "PICK_UP: 交通接駁"),
            ]
            for title, label, target in info_list:
                web.base_page.assert_data(
                    title, web.reservation_card_dialog.get_tab_service_info(label), target
                )

        with allure.step("Then 驗證費用明細資料"):
            web.reservation_card_dialog.click_tab("expenseDetail")
            web.base_page.screenshot("Then 驗證費用明細資料")
            info_list = [
                ("入帳日", "useDate", "2024/01/05 週五"),
                ("消費項目", "itemSna", "交通接駁(接)"),
                ("單價", "unitAmount", "100"),
                ("數量", "itemQnt", "1"),
                ("小計", "itemAmount", "100"),
                ("服務日", "servDate", "2024/01/05 週五"),
            ]
            for title, label, target in info_list:
                web.base_page.assert_data(
                    title,
                    web.reservation_card_dialog.get_tab_expense_info_in_row("2024/01/05", label),
                    target,
                )

    @allure.story("新增接送服務-送(自動入帳)")
    @pytest.mark.xdist_group("test_transport_service")
    @pytest.mark.dependency(
        name="test_add_transport_service_send_with_expense",
        depends=["test_verify_transport_service_expense"],
        scope="session",
    )
    def test_add_transport_service_send_with_expense(self, cache):
        pages = [
            ReservationCardDialog,
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            ReservationPage,
            BasePage,
            TransportServicesComponent,
        ]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")
        full_name = cache.get("full_name_transport", "")

        with allure.step(
            "Given 使用者從「訂房」進入「訂房卡」頁面並進入「訂房明細」視窗，然後點擊住客的黑色鉛筆"
        ):
            ShareSteps.create_or_enter_reservation_detail(
                web, "guestName", full_name, "doOpenDtDetailDialog"
            )
            web.reservation_card_dialog.click_tab_toolbar("guest", "編輯")
            web.base_page.screenshot("Given 使用者進入「訂房明細」視窗，然後點擊住客的黑色鉛筆")

        with allure.step("And 點擊「接送」欄位的[綠色加號]，進入「接送服務編輯」視窗"):
            web.reservation_card_dialog.click_tab_guest_function("transferButton").sleep(1)
            web.base_page.click_toolbar_with_icon("add").sleep(1)
            web.base_page.screenshot("And 點擊「接送」欄位的[綠色加號]，進入「接送服務編輯」視窗")

        with allure.step("And 點擊下拉選單選擇或輸入必填欄位"):
            web.transport_services_component.set_transport_service(
                "100", transport_type="L : 送"
            ).sleep(1)
            input_time = web.transport_services_component.get_transport_field_value("時間")
            initial_values = {
                "type": web.transport_services_component.get_transport_combobox_text("接/送"),
                "date": web.transport_services_component.get_transport_field_value("日期"),
                "company": web.transport_services_component.get_transport_field_direct_value(
                    "公司"
                ),
                "contact": web.transport_services_component.get_transport_field_direct_value(
                    "連絡人"
                ),
                "phone": web.transport_services_component.get_transport_field_direct_value("電話"),
                "guest": web.transport_services_component.get_transport_field_direct_value(
                    "指定住客"
                ),
                "guest_status": web.transport_services_component.get_transport_field_direct_value(
                    "住客帳狀態"
                ),
                "card_no": web.transport_services_component.get_transport_field_direct_value(
                    "訂房卡號"
                ),
                "checkin_date": web.transport_services_component.get_transport_field_value(
                    "入住日期"
                ),
                "checkout_date": web.transport_services_component.get_transport_field_value(
                    "退房日期"
                ),
            }
            web.base_page.screenshot("And 點擊下拉選單選擇或輸入必填欄位")

        with allure.step("And 點擊右上的[橘色磁碟片]儲存"):
            ShareSteps.click_btn_save(web)

        with allure.step("Then 顯示'儲存成功'訊息"):
            ShareSteps.verify_save_success_tip(web)
            web.share_panel_component.close_panel("接送服務編輯").sleep(1)
            web.reservation_card_dialog.click_detail_toolbar("save").sleep(1)
            web.tip_component.click_ok()
            web.base_page.close_panel()

        with allure.step("And 驗證接送服務表單欄位值正確"):
            web.reservation_card_dialog.click_card_toolbar("doOpenDtDetailDialog").sleep(1)
            web.reservation_card_dialog.click_tab_toolbar("guest", "編輯")
            web.reservation_card_dialog.click_tab_guest_function("transferButton").sleep(1)
            web.transport_services_component.click_transport_grid_last_row().sleep(2)
            web.base_page.screenshot("And 驗證接送服務表單欄位值正確")
            field_validations = [
                ("接/送", "combobox", "接/送", "L : 送"),
                ("日期", "field", "日期", initial_values["date"]),
                ("時間", "field", "時間", input_time),
                ("公司", "direct", "公司", initial_values["company"]),
                ("連絡人", "direct", "連絡人", initial_values["contact"]),
                ("電話", "direct", "電話", initial_values["phone"]),
                ("費用", "spinbutton", "費用", "100"),
                ("大人", "spinbutton", "大人", "2"),
                ("小孩", "spinbutton", "小孩", "0"),
                ("指定住客", "direct", "指定住客", initial_values["guest"]),
                ("住客帳狀態", "direct", "住客帳狀態", initial_values["guest_status"]),
                ("訂房卡號", "direct", "訂房卡號", initial_values["card_no"]),
                ("入住日期", "field", "入住日期", initial_values["checkin_date"]),
                ("退房日期", "field", "退房日期", initial_values["checkout_date"]),
                ("新增日期", "field", "新增日期", datetime.now().strftime("%Y/%m/%d")),
                ("新增者", "direct", "新增者", "autotest"),
                ("修改日期", "field", "修改日期", datetime.now().strftime("%Y/%m/%d")),
                ("修改者", "direct", "修改者", "autotest"),
            ]
            for title, method, field, expected in field_validations:
                if method == "field":
                    web.base_page.assert_data(
                        title,
                        web.transport_services_component.get_transport_field_value(field),
                        expected,
                    )
                elif method == "direct":
                    web.base_page.assert_data(
                        title,
                        web.transport_services_component.get_transport_field_direct_value(field),
                        expected,
                    )
                elif method == "spinbutton":
                    web.base_page.assert_data(
                        title,
                        web.transport_services_component.get_transport_spinbutton_value(field),
                        expected,
                    )
                elif method == "combobox":
                    web.base_page.assert_data(
                        title,
                        web.transport_services_component.get_transport_combobox_text(field),
                        expected,
                    )

        with allure.step("And 驗證接送服務表格資料正確"):
            web.base_page.screenshot("And 驗證接送服務表格資料正確")
            for title, col, expected in [
                ("接/送", "1", "L : 送"),
                ("日期", "2", initial_values["date"]),
                ("時間", "4", input_time),
            ]:
                web.base_page.assert_data(
                    title,
                    web.transport_services_component.get_transport_grid_cell_text(col),
                    expected,
                )

    @allure.story("驗證接送服務(送)資料-服務項目、費用明細")
    @pytest.mark.xdist_group("test_transport_service")
    @pytest.mark.dependency(
        name="test_verify_transport_service_send_expense",
        depends=["test_add_transport_service_send_with_expense"],
        scope="session",
    )
    def test_verify_transport_service_send_expense(self, cache):
        pages = [
            ReservationCardDialog,
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            ReservationPage,
            BasePage,
            TransportServicesComponent,
        ]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")
        full_name = cache.get("full_name_transport", "")

        with allure.step("Given 使用者從「訂房」進入「訂房卡」頁面並進入「訂房明細」視窗"):
            ShareSteps.create_or_enter_reservation_detail(
                web, "guestName", full_name, "doOpenDtDetailDialog"
            )
            web.base_page.screenshot("Given 使用者進入「訂房明細」視窗")

        with allure.step("When 驗證服務項目資料"):
            web.reservation_card_dialog.click_tab("service").sleep(1)
            web.base_page.screenshot("When 驗證服務項目資料")
            info_list = [
                ("服務類別", "commandOption", "****: ALL"),
                ("服務項目", "itemNos", "交通接駁(送)"),
                ("單價", "unitAmount", "100"),
                ("數量規則", "itemQntRule", "BY_ROOM: 房間數"),
                ("數量", "itemQuantity", "1"),
                ("服務方式", "servWay", "A: 指定日期"),
                ("開始日期", "beginDate", "2024/01/05 週五"),
                ("結束日期", "endDate", "2024/01/05 週五"),
                ("來源", "fromSys", "PICK_UP: 交通接駁"),
            ]
            for title, label, target in info_list:
                web.base_page.assert_data(
                    title, web.reservation_card_dialog.get_tab_service_info(label), target
                )

        with allure.step("Then 驗證費用明細資料"):
            web.reservation_card_dialog.click_tab("expenseDetail")
            web.base_page.screenshot("Then 驗證費用明細資料")
            info_list = [
                ("入帳日", "useDate", "2024/01/05 週五"),
                ("消費項目", "itemSna", "交通接駁(送)"),
                ("單價", "unitAmount", "100"),
                ("數量", "itemQnt", "1"),
                ("小計", "itemAmount", "100"),
                ("服務日", "servDate", "2024/01/06 週六"),
            ]
            for title, label, target in info_list:
                web.base_page.assert_data(
                    title,
                    web.reservation_card_dialog.get_tab_expense_info_in_row("2024/01/05", label),
                    target,
                )

    @allure.story("新增接送服務-接(無入帳)")
    @pytest.mark.xdist_group("test_transport_service_no_charge")
    @pytest.mark.dependency(name="test_add_transport_service_without_charge", scope="session")
    def test_add_transport_service_without_charge(self, cache):
        pages = [
            ReservationCardDialog,
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            ReservationPage,
            BasePage,
            TransportServicesComponent,
        ]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")

        with allure.step(
            "Given 使用者從「訂房」進入「訂房卡」頁面並進入「訂房明細」，然後點擊住客的黑色鉛筆"
        ):
            first_name = names.get_first_name()
            last_name = names.get_last_name()
            cache.set("full_name_transport_no_charge", f"{first_name} {last_name}")
            ShareSteps.create_or_enter_reservation_detail(
                web,
                "guestName",
                f"{first_name} {last_name}",
                "doOpenDtDetailDialog",
                first_name,
                last_name,
                "現場訂房含早",
                3,
            )
            web.reservation_card_dialog.click_tab_toolbar("guest", "編輯")
            web.base_page.screenshot("Given 使用者進入「訂房明細」視窗，然後點擊住客的黑色鉛筆")

        with allure.step("And 點擊「接送」欄位的[綠色加號]，進入「接送服務編輯」視窗"):
            web.reservation_card_dialog.click_tab_guest_function("transferButton").sleep(1)
            web.base_page.click_toolbar_with_icon("add").sleep(1)
            web.base_page.screenshot("And 點擊「接送」欄位的[綠色加號]，進入「接送服務編輯」視窗")

        with allure.step("And 點擊下拉選單選擇或輸入必填欄位"):
            web.transport_services_component.set_transport_service().sleep(1)
            initial_values = {
                "type": web.transport_services_component.get_transport_combobox_text("接/送"),
                "date": web.transport_services_component.get_transport_field_value("日期"),
                "company": web.transport_services_component.get_transport_field_direct_value(
                    "公司"
                ),
                "contact": web.transport_services_component.get_transport_field_direct_value(
                    "連絡人"
                ),
                "phone": web.transport_services_component.get_transport_field_direct_value("電話"),
                "guest": web.transport_services_component.get_transport_field_direct_value(
                    "指定住客"
                ),
                "guest_status": web.transport_services_component.get_transport_field_direct_value(
                    "住客帳狀態"
                ),
                "card_no": web.transport_services_component.get_transport_field_direct_value(
                    "訂房卡號"
                ),
                "checkin_date": web.transport_services_component.get_transport_field_value(
                    "入住日期"
                ),
                "checkout_date": web.transport_services_component.get_transport_field_value(
                    "退房日期"
                ),
                "input_time": web.transport_services_component.get_transport_field_value("時間"),
            }
            web.base_page.screenshot("And 點擊下拉選單選擇或輸入必填欄位")

        with allure.step("And 點擊右上的[橘色磁碟片]儲存"):
            ShareSteps.click_btn_save(web)

        with allure.step("Then 顯示'儲存成功'訊息"):
            ShareSteps.verify_save_success_tip(web)
            web.share_panel_component.close_panel("接送服務編輯")
            web.reservation_card_dialog.click_detail_toolbar("save").sleep(1)
            web.tip_component.click_ok()

        with allure.step("And 驗證接送服務表單欄位值正確"):
            web.reservation_card_dialog.click_tab_toolbar("guest", "編輯")
            web.reservation_card_dialog.click_tab_guest_function("transferButton").sleep(1)
            web.transport_services_component.click_transport_grid_last_row().sleep(2)
            web.base_page.screenshot("And 驗證接送服務表單欄位值正確")
            field_validations = [
                ("接/送", "combobox", "接/送", initial_values["type"]),
                ("日期", "field", "日期", initial_values["date"]),
                ("時間", "field", "時間", initial_values["input_time"]),
                ("公司", "direct", "公司", initial_values["company"]),
                ("連絡人", "direct", "連絡人", initial_values["contact"]),
                ("電話", "direct", "電話", initial_values["phone"]),
                ("費用", "spinbutton", "費用", "0"),
                ("大人", "spinbutton", "大人", "2"),
                ("小孩", "spinbutton", "小孩", "0"),
                ("指定住客", "direct", "指定住客", initial_values["guest"]),
                ("住客帳狀態", "direct", "住客帳狀態", initial_values["guest_status"]),
                ("訂房卡號", "direct", "訂房卡號", initial_values["card_no"]),
                ("入住日期", "field", "入住日期", initial_values["checkin_date"]),
                ("退房日期", "field", "退房日期", initial_values["checkout_date"]),
                ("新增日期", "field", "新增日期", datetime.now().strftime("%Y/%m/%d")),
                ("新增者", "direct", "新增者", "autotest"),
                ("修改日期", "field", "修改日期", datetime.now().strftime("%Y/%m/%d")),
                ("修改者", "direct", "修改者", "autotest"),
            ]
            for title, method, field, expected in field_validations:
                if method == "field":
                    web.base_page.assert_data(
                        title,
                        web.transport_services_component.get_transport_field_value(field),
                        expected,
                    )
                elif method == "direct":
                    web.base_page.assert_data(
                        title,
                        web.transport_services_component.get_transport_field_direct_value(field),
                        expected,
                    )
                elif method == "spinbutton":
                    web.base_page.assert_data(
                        title,
                        web.transport_services_component.get_transport_spinbutton_value(field),
                        expected,
                    )
                elif method == "combobox":
                    web.base_page.assert_data(
                        title,
                        web.transport_services_component.get_transport_combobox_text(field),
                        expected,
                    )

        with allure.step("And 驗證接送服務表格資料正確"):
            web.base_page.screenshot("And 驗證接送服務表格資料正確")
            for title, col, expected in [
                ("接/送", "1", initial_values["type"]),
                ("日期", "2", initial_values["date"]),
                ("時間", "4", initial_values["input_time"]),
            ]:
                web.base_page.assert_data(
                    title,
                    web.transport_services_component.get_transport_grid_cell_text(col),
                    expected,
                )

    @allure.story("新增接送服務-送(無入帳)")
    @pytest.mark.xdist_group("test_transport_service_no_charge")
    @pytest.mark.dependency(
        name="test_add_transport_service_send_without_charge",
        depends=["test_add_transport_service_without_charge"],
        scope="session",
    )
    def test_add_transport_service_send_without_charge(self, cache):
        pages = [
            ReservationCardDialog,
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            ReservationPage,
            BasePage,
            TransportServicesComponent,
        ]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")
        full_name = cache.get("full_name_transport_no_charge", "")

        with allure.step(
            "Given 使用者從「訂房」進入「訂房卡」頁面並進入「訂房明細」視窗，然後點擊住客的黑色鉛筆"
        ):
            ShareSteps.create_or_enter_reservation_detail(
                web, "guestName", full_name, "doOpenDtDetailDialog"
            )
            web.reservation_card_dialog.click_tab_toolbar("guest", "編輯")
            web.base_page.screenshot("Given 使用者進入「訂房明細」視窗，然後點擊住客的黑色鉛筆")

        with allure.step("And 點擊「接送」欄位的[綠色加號]，進入「接送服務編輯」視窗"):
            web.reservation_card_dialog.click_tab_guest_function("transferButton").sleep(1)
            web.base_page.click_toolbar_with_icon("add").sleep(1)
            web.base_page.screenshot("And 點擊「接送」欄位的[綠色加號]，進入「接送服務編輯」視窗")

        with allure.step("And 點擊下拉選單選擇或輸入必填欄位"):
            web.transport_services_component.set_transport_service(
                fee=None, transport_type="L : 送"
            ).sleep(1)
            initial_values = {
                "type": web.transport_services_component.get_transport_combobox_text("接/送"),
                "date": web.transport_services_component.get_transport_field_value("日期"),
                "company": web.transport_services_component.get_transport_field_direct_value(
                    "公司"
                ),
                "contact": web.transport_services_component.get_transport_field_direct_value(
                    "連絡人"
                ),
                "phone": web.transport_services_component.get_transport_field_direct_value("電話"),
                "guest": web.transport_services_component.get_transport_field_direct_value(
                    "指定住客"
                ),
                "guest_status": web.transport_services_component.get_transport_field_direct_value(
                    "住客帳狀態"
                ),
                "card_no": web.transport_services_component.get_transport_field_direct_value(
                    "訂房卡號"
                ),
                "checkin_date": web.transport_services_component.get_transport_field_value(
                    "入住日期"
                ),
                "checkout_date": web.transport_services_component.get_transport_field_value(
                    "退房日期"
                ),
                "input_time": web.transport_services_component.get_transport_field_value("時間"),
            }
            web.base_page.screenshot("And 點擊下拉選單選擇或輸入必填欄位")

        with allure.step("And 點擊右上的[橘色磁碟片]儲存"):
            ShareSteps.click_btn_save(web)

        with allure.step("Then 顯示'儲存成功'訊息"):
            ShareSteps.verify_save_success_tip(web)
            web.share_panel_component.close_panel("接送服務編輯")
            web.reservation_card_dialog.click_detail_toolbar("save").sleep(1)
            web.tip_component.click_ok()

        with allure.step("And 驗證接送服務表單欄位值正確"):
            web.reservation_card_dialog.click_tab_toolbar("guest", "編輯")
            web.reservation_card_dialog.click_tab_guest_function("transferButton").sleep(1)
            web.transport_services_component.click_transport_grid_last_row().sleep(2)
            web.base_page.screenshot("And 驗證接送服務表單欄位值正確")
            field_validations = [
                ("接/送", "combobox", "接/送", initial_values["type"]),
                ("日期", "field", "日期", initial_values["date"]),
                ("時間", "field", "時間", initial_values["input_time"]),
                ("公司", "direct", "公司", initial_values["company"]),
                ("連絡人", "direct", "連絡人", initial_values["contact"]),
                ("電話", "direct", "電話", initial_values["phone"]),
                ("費用", "spinbutton", "費用", "0"),
                ("大人", "spinbutton", "大人", "2"),
                ("小孩", "spinbutton", "小孩", "0"),
                ("指定住客", "direct", "指定住客", initial_values["guest"]),
                ("住客帳狀態", "direct", "住客帳狀態", initial_values["guest_status"]),
                ("訂房卡號", "direct", "訂房卡號", initial_values["card_no"]),
                ("入住日期", "field", "入住日期", initial_values["checkin_date"]),
                ("退房日期", "field", "退房日期", initial_values["checkout_date"]),
                ("新增日期", "field", "新增日期", datetime.now().strftime("%Y/%m/%d")),
                ("新增者", "direct", "新增者", "autotest"),
                ("修改日期", "field", "修改日期", datetime.now().strftime("%Y/%m/%d")),
                ("修改者", "direct", "修改者", "autotest"),
            ]
            for title, method, field, expected in field_validations:
                if method == "field":
                    web.base_page.assert_data(
                        title,
                        web.transport_services_component.get_transport_field_value(field),
                        expected,
                    )
                elif method == "direct":
                    web.base_page.assert_data(
                        title,
                        web.transport_services_component.get_transport_field_direct_value(field),
                        expected,
                    )
                elif method == "spinbutton":
                    web.base_page.assert_data(
                        title,
                        web.transport_services_component.get_transport_spinbutton_value(field),
                        expected,
                    )
                elif method == "combobox":
                    web.base_page.assert_data(
                        title,
                        web.transport_services_component.get_transport_combobox_text(field),
                        expected,
                    )

        with allure.step("And 驗證接送服務表格資料正確"):
            web.base_page.screenshot("And 驗證接送服務表格資料正確")
            for title, col, expected in [
                ("接/送", "1", initial_values["type"]),
                ("日期", "2", initial_values["date"]),
                ("時間", "4", initial_values["input_time"]),
            ]:
                web.base_page.assert_data(
                    title,
                    web.transport_services_component.get_transport_grid_cell_text(col),
                    expected,
                )

    @allure.story("批次新增接送服務")
    @pytest.mark.xdist_group("test_transport_service")
    @pytest.mark.dependency(name="test_batch_add_transport_service", scope="session")
    def test_batch_add_transport_service(self, cache):
        pages = [
            ReservationCardDialog,
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            ReservationPage,
            BasePage,
            TransportServicesComponent,
        ]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")

        with allure.step("Given 使用者從「訂房」進入「訂房卡」頁面並進入「訂房明細」"):
            first_name = names.get_first_name()
            last_name = names.get_last_name()
            cache.set("full_name_batch_transport", f"{first_name} {last_name}")
            ShareSteps.create_or_enter_reservation_detail(
                web,
                "guestName",
                f"{first_name} {last_name}",
                "doOpenDtDetailDialog",
                first_name,
                last_name,
                "現場訂房含早",
                4,
            )
            web.reservation_card_dialog.click_tab_toolbar("guest", "編輯")
            web.base_page.screenshot("Given 使用者進入「訂房明細」視窗，然後點擊住客的黑色鉛筆")

        with allure.step("And 點擊「接送」欄位的[勾勾]，進入「接送服務編輯」視窗"):
            web.reservation_card_dialog.click_tab_guest_function("transferButton").sleep(1)

        with allure.step("And 新增一筆接送服務作為批次新增基礎"):
            web.transport_services_component.set_transport_service().sleep(1)

            initial_values = {
                "type": web.transport_services_component.get_transport_combobox_text("接/送"),
                "company": web.transport_services_component.get_transport_field_direct_value(
                    "公司"
                ),
                "contact": web.transport_services_component.get_transport_field_direct_value(
                    "連絡人"
                ),
                "phone": web.transport_services_component.get_transport_field_direct_value("電話"),
                "guest": web.transport_services_component.get_transport_field_direct_value(
                    "指定住客"
                ),
                "guest_status": web.transport_services_component.get_transport_field_direct_value(
                    "住客帳狀態"
                ),
                "card_no": web.transport_services_component.get_transport_field_direct_value(
                    "訂房卡號"
                ),
                "checkin_date": web.transport_services_component.get_transport_field_value(
                    "入住日期"
                ),
                "checkout_date": web.transport_services_component.get_transport_field_value(
                    "退房日期"
                ),
                "input_time": web.transport_services_component.get_transport_field_value("時間"),
            }
            cache.set("batch_transport_data", initial_values)

            web.base_page.click_toolbar_with_icon("save").sleep(1)
            web.tip_component.click_ok()
            web.base_page.screenshot("And 點擊右側表格中想要批次新增的項目")

        with allure.step("And 點擊左上的[批次新增]，進入「批次新增」視窗"):
            web.transport_services_component.click_transport_batch_add().sleep(1)
            web.transport_services_component.click_save_transport_batch().sleep(1)
            web.base_page.screenshot("And 點擊左上的[批次新增]，進入「批次新增」視窗")

        with allure.step("Then 顯示'儲存成功'訊息"):
            ShareSteps.verify_save_success_tip(web)
            web.share_panel_component.close_panel("批次新增").sleep(1)
            web.share_panel_component.close_panel("接送服務編輯")
            web.reservation_card_dialog.click_detail_toolbar("save").sleep(1)
            web.tip_component.click_ok()

        with allure.step("And 驗證右方表格顯示批次新增的接送服務筆數"):
            web.reservation_card_dialog.click_tab_toolbar("guest", "編輯")
            web.reservation_card_dialog.click_tab_guest_function("transferButton").sleep(1)
            web.base_page.screenshot("And 驗證右方表格顯示批次新增的接送服務筆數")

            transport_rows = web.transport_services_component.get_transport_row_count()
            web.base_page.assert_data("接送服務表格行數", transport_rows, 2)

    @allure.story("驗證批次新增接送服務資料")
    @pytest.mark.xdist_group("test_transport_service")
    @pytest.mark.dependency(
        name="test_verify_batch_add_transport_service_data",
        depends=["test_batch_add_transport_service"],
        scope="session",
    )
    def test_verify_batch_add_transport_service_data(self, cache):
        pages = [
            ReservationCardDialog,
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            ReservationPage,
            BasePage,
            TransportServicesComponent,
        ]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")
        full_name = cache.get("full_name_batch_transport", "")
        transport_data = cache.get("batch_transport_data", "")

        with allure.step("Given 使用者從「訂房」進入「訂房卡」頁面並進入「訂房明細」視窗"):
            ShareSteps.create_or_enter_reservation_detail(
                web, "guestName", full_name, "doOpenDtDetailDialog"
            )
            web.reservation_card_dialog.click_tab_toolbar("guest", "編輯")
            web.base_page.screenshot("Given 使用者進入「訂房明細」視窗")

        with allure.step("When 點擊「接送」欄位的[勾勾]，進入「接送服務編輯」視窗"):
            web.reservation_card_dialog.click_tab_guest_function("transferButton").sleep(1)
            web.base_page.screenshot("When 點擊「接送」欄位的[勾勾]，進入「接送服務編輯」視窗")

        with allure.step("And 驗證接送服務表單欄位值正確"):
            web.transport_services_component.click_transport_grid_last_row().sleep(5)
            web.base_page.screenshot("And 驗證接送服務表單欄位值正確")

            field_validations = [
                ("接/送", "combobox", "接/送", transport_data["type"]),
                ("日期", "field", "日期", "2024/01/06"),
                ("時間", "field", "時間", transport_data["input_time"]),
                ("公司", "direct", "公司", transport_data["company"]),
                ("連絡人", "direct", "連絡人", transport_data["contact"]),
                ("電話", "direct", "電話", transport_data["phone"]),
                ("費用", "spinbutton", "費用", "0"),
                ("大人", "spinbutton", "大人", "2"),
                ("小孩", "spinbutton", "小孩", "0"),
                ("指定住客", "direct", "指定住客", transport_data["guest"]),
                ("住客帳狀態", "direct", "住客帳狀態", transport_data["guest_status"]),
                ("訂房卡號", "direct", "訂房卡號", transport_data["card_no"]),
                ("入住日期", "field", "入住日期", transport_data["checkin_date"]),
                ("退房日期", "field", "退房日期", transport_data["checkout_date"]),
                ("新增日期", "field", "新增日期", datetime.now().strftime("%Y/%m/%d")),
                ("新增者", "direct", "新增者", "autotest"),
                ("修改日期", "field", "修改日期", datetime.now().strftime("%Y/%m/%d")),
                ("修改者", "direct", "修改者", "autotest"),
            ]

            for title, method, field, expected in field_validations:
                if method == "field":
                    web.base_page.assert_data(
                        title,
                        web.transport_services_component.get_transport_field_value(field),
                        expected,
                    )
                elif method == "direct":
                    web.base_page.assert_data(
                        title,
                        web.transport_services_component.get_transport_field_direct_value(field),
                        expected,
                    )
                elif method == "spinbutton":
                    web.base_page.assert_data(
                        title,
                        web.transport_services_component.get_transport_spinbutton_value(field),
                        expected,
                    )
                elif method == "combobox":
                    web.base_page.assert_data(
                        title,
                        web.transport_services_component.get_transport_combobox_text(field),
                        expected,
                    )

        with allure.step("And 驗證接送服務表格資料正確"):
            web.base_page.screenshot("And 驗證接送服務表格資料正確")
            transport_rows = web.transport_services_component.get_transport_row_count()
            date = ["2024/01/05", "2024/01/06"]

            for row_index in range(1, transport_rows + 1):
                web.base_page.assert_data(
                    f"第{row_index}筆-接/送",
                    web.transport_services_component.get_transport_grid_cell_text_by_row(
                        row_index, "1"
                    ),
                    transport_data["type"],
                )
                web.base_page.assert_data(
                    f"第{row_index}筆-日期",
                    web.transport_services_component.get_transport_grid_cell_text_by_row(
                        row_index, "2"
                    ),
                    date[row_index - 1],
                )
                web.base_page.assert_data(
                    f"第{row_index}筆-時間",
                    web.transport_services_component.get_transport_grid_cell_text_by_row(
                        row_index, "4"
                    ),
                    transport_data["input_time"],
                )

    @allure.story("住客明細-新增服務項目(可改金額)")
    @pytest.mark.parametrize(
        "service_way",
        [
            "SpecifiedDate",
            "FirstDay",
            "Daily",
            "LastDay",
            "OnePlusEveryFewDays",
            "EveryFewDays",
            "Weekly",
        ],
    )
    @pytest.mark.xdist_group("test_service_item")
    @pytest.mark.dependency(name="test_add_service_item_editable_price", scope="session")
    def test_add_service_item_editable_price(self, service_way):
        pages = [
            ReservationCardDialog,
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            ServiceItemComponent,
            ReservationPage,
            BasePage,
        ]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")
        service_item_step = globals()[f"{service_way}ServiceItemStep"](web)

        with allure.step("Given 使用者進入「訂房明細」視窗"):
            ShareSteps.create_or_enter_reservation_detail(
                web,
                "quickSearch",
                "Card Service",
                "doOpenDtDetailDialog",
                "Card",
                "Service",
                "現場訂房含早",
                1,
            )
            web.base_page.screenshot("Given 使用者進入「訂房明細」視窗")

        with allure.step("When 點擊「服務項目」頁籤並新增服務項目"):
            web.reservation_card_dialog.click_tab("service").sleep(1)
            service_item_step.clear_service_item()
            web.reservation_card_dialog.click_tab_add_btn("service").sleep(1)
            web.base_page.screenshot("When 點擊「服務項目」頁籤並新增服務項目")

        with allure.step("And 輸入服務項目資訊"):
            service_item_step.input_service_item_info("SPA", "2,000")
            web.base_page.screenshot("And 輸入服務項目資訊")

        with allure.step("And 點擊右上的[橘色磁碟片]儲存"):
            web.base_page.click_toolbar_with_icon("save")
            web.reservation_card_dialog.click_detail_toolbar("save").sleep(1)
            web.tip_component.click_ok()
            web.base_page.screenshot("And 點擊右上的[橘色磁碟片]儲存")

        with allure.step("Then 驗證服務項目資料"):
            web.base_page.close_panel()
            web.reservation_card_dialog.click_card_toolbar("doOpenDtDetailDialog").sleep(1)
            web.reservation_card_dialog.click_tab("service").sleep(1)
            web.base_page.screenshot("Then 驗證服務項目資料")
            service_item_step.valid_tab_service_info("SPA", "2,000")

        with allure.step("And 驗證費用明細資料"):
            web.reservation_card_dialog.click_tab("expenseDetail")
            web.base_page.screenshot("And 驗證費用明細資料")
            service_item_step.valid_tab_expense_detail_info("SPA", "2,000")

    @allure.story("住客明細-新增服務項目(不可改金額)")
    @pytest.mark.parametrize(
        "service_way",
        [
            "SpecifiedDate",
            "FirstDay",
            "Daily",
            "LastDay",
            "OnePlusEveryFewDays",
            "EveryFewDays",
            "Weekly",
        ],
    )
    @pytest.mark.xdist_group("test_service_item")
    @pytest.mark.dependency(
        name="test_add_service_item_non_editable_price",
        depends=["test_add_service_item_editable_price"],
        scope="session",
    )
    def test_add_service_item_non_editable_price(self, service_way):
        pages = [
            ReservationCardDialog,
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            ServiceItemComponent,
            ReservationPage,
            BasePage,
        ]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")
        service_item_step = globals()[f"{service_way}ServiceItemStep"](web)

        with allure.step("Given 使用者進入「訂房明細」視窗"):
            ShareSteps.create_or_enter_reservation_detail(
                web,
                "quickSearch",
                "Card Service",
                "doOpenDtDetailDialog",
                "Card",
                "Service",
                "現場訂房含早",
                1,
            )
            web.base_page.screenshot("Given 使用者進入「訂房明細」視窗")

        with allure.step("When 點擊「服務項目」頁籤並新增服務項目"):
            web.reservation_card_dialog.click_tab("service").sleep(1)
            service_item_step.clear_service_item()
            web.reservation_card_dialog.click_tab_add_btn("service").sleep(1)
            web.base_page.screenshot("When 點擊「服務項目」頁籤並新增服務項目")

        with allure.step("And 輸入服務項目資訊"):
            service_item_step.input_service_item_info("DISC", "-300", price_editable=False)
            web.base_page.screenshot("And 輸入服務項目資訊")

        with allure.step("And 點擊右上的[橘色磁碟片]儲存"):
            web.base_page.click_toolbar_with_icon("save")
            web.reservation_card_dialog.click_detail_toolbar("save").sleep(1)
            web.tip_component.click_ok()
            web.base_page.screenshot("And 點擊右上的[橘色磁碟片]儲存")

        with allure.step("Then 驗證服務項目資料"):
            web.base_page.close_panel()
            web.reservation_card_dialog.click_card_toolbar("doOpenDtDetailDialog").sleep(1)
            web.reservation_card_dialog.click_tab("service").sleep(1)
            web.base_page.screenshot("Then 驗證服務項目資料")
            service_item_step.valid_tab_service_info("DISC", "-300", price_editable=False)

        with allure.step("And 驗證費用明細資料"):
            web.reservation_card_dialog.click_tab("expenseDetail")
            web.base_page.screenshot("And 驗證費用明細資料")
            service_item_step.valid_tab_expense_detail_info("DISC", "-300")
