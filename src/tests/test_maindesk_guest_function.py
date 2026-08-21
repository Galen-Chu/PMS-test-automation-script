from datetime import datetime
import allure
import pytest
import names
from pages.base_page import BasePage
from pages.components.header_component import HeaderComponent
from pages.components.tip_component import TipComponent
from pages.components.share_panel_component import SharePanelComponent
from pages.components.pre_credit_component import PreCreditComponent
from pages.components.todolist_edit_component import TodolistEditComponent
from pages.components.message_edit_component import MessageEditComponent
from pages.components.transport_services_component import TransportServicesComponent
from pages.dialogs.reservation_card_dialog import ReservationCardDialog
from pages.lost_management_page import LostManagementPage
from pages.maindesk_page import MaindeskPage
from tests.share_steps import ShareSteps
from tools.driver_helper import DriverHelper
from tools.random_helper import RandomHelper


@allure.feature("接待作業 - 綜合櫃檯-住客功能")
class TestMaindeskHeaderToolbar:

    @allure.story("綜合櫃檯 - 新增注意事項")
    @pytest.mark.xdist_group("test_maindesk_flow_c")
    @pytest.mark.dependency(name="test_add_note_at_maindesk", scope="session")
    def test_add_note_at_maindesk(self):
        pages = [MaindeskPage, HeaderComponent, TipComponent, SharePanelComponent, BasePage]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")

        with allure.step("Given 使用者從「綜合櫃檯」頁面進入「房間細節」視窗"):
            web.header_component.expand_menu("接待").sleep(1)
            web.header_component.to_func_page("綜合櫃檯").sleep(1)
            web.base_page.set_value_by_label("住客姓名", "Card Maindesk FLow C")
            web.base_page.search().sleep(1)
            web.maindesk_page.click_first_room().sleep(1)
            web.base_page.screenshot("Given 使用者從「綜合櫃檯」頁面進入「房間細節」視窗")

        with allure.step("When 點擊[橘色筆]進行編輯"):
            web.base_page.click_toolbar_with_icon("edit").sleep(1)
            web.base_page.screenshot("When 點擊[橘色筆]進行編輯")

        with allure.step("And 點擊注意事項欄位框旁之「...」"):
            web.maindesk_page.click_edit_button("open_notice_rmk").sleep(1)
            web.base_page.screenshot("And 點擊注意事項欄位框旁之「...」")

        with allure.step("And 點擊輸入[注意事項]"):
            note_content = "這是測試注意事項_" + RandomHelper.random_string()
            web.maindesk_page.input_note_content(note_content).sleep(1)
            web.base_page.screenshot("And 點擊輸入[注意事項]")

        with allure.step("And 點擊[確定]"):
            web.share_panel_component.click_panel_footer_btn("注意事項", "確定").sleep(1)
            web.base_page.screenshot("And 點擊[確定]")

        with allure.step("And 點擊[橘色磁碟片]進行儲存"):
            ShareSteps.click_btn_save(web).sleep(1)
            web.base_page.screenshot("And 點擊[橘色磁碟片]進行儲存")

        with allure.step("Then 顯示'儲存成功'提示"):
            ShareSteps.verify_save_success_tip(web)
            web.share_panel_component.close_panel("房間細節").sleep(2)

        with allure.step("And 房間細節的注意事項欄位正確顯示"):
            web.maindesk_page.click_first_room().sleep(1)
            web.base_page.screenshot("And 房間細節的注意事項欄位正確顯示")

            web.base_page.assert_data(
                "注意事項內容", web.maindesk_page.get_notice_content(), note_content
            )

    @allure.story("綜合櫃檯 - 新增住客")
    @pytest.mark.xdist_group("test_maindesk_flow_c")
    @pytest.mark.dependency(
        name="test_add_guest_at_maindesk", depends=["test_add_note_at_maindesk"], scope="session"
    )
    def test_add_guest_at_maindesk(self):
        pages = [MaindeskPage, HeaderComponent, TipComponent, SharePanelComponent, BasePage]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")

        with allure.step("Given 使用者從「綜合櫃檯」頁面進入「房間細節」視窗"):
            web.header_component.expand_menu("接待").sleep(1)
            web.header_component.to_func_page("綜合櫃檯").sleep(1)
            web.base_page.set_value_by_label("住客姓名", "Card Maindesk FLow C")
            web.base_page.search().sleep(1)
            web.maindesk_page.click_first_room().sleep(1)
            web.base_page.screenshot("Given 使用者從「綜合櫃檯」頁面進入「房間細節」視窗")

        with allure.step("When 點擊[橘色筆]進行編輯"):
            web.base_page.click_toolbar_with_icon("edit").sleep(1)
            web.base_page.screenshot("When 點擊[橘色筆]進行編輯")

        with allure.step("And 點擊[綠色加號]新增一筆資料"):
            web.maindesk_page.click_add_guest().sleep(1)
            web.base_page.screenshot("And 點擊[綠色加號]新增一筆資料")

        with allure.step("And 點擊輸入[住客姓名]"):
            web.maindesk_page.input_guest_name("cathy").sleep(1)
            web.base_page.screenshot("And 點擊輸入[住客姓名]")

        with allure.step("And 點擊住客下拉選單"):
            web.maindesk_page.click_dropdown_guest("cathy").sleep(1)
            web.base_page.screenshot("And 點擊住客下拉選單")

        with allure.step("And 點擊[橘色磁碟片]進行儲存"):
            ShareSteps.click_btn_save(web).sleep(1)
            web.base_page.screenshot("And 點擊[橘色磁碟片]進行儲存")

        with allure.step("Then 顯示'儲存成功'提示"):
            ShareSteps.verify_save_success_tip(web)
            web.share_panel_component.close_panel("房間細節").sleep(2)

        with allure.step("And 房間細節的注意事項欄位正確顯示"):
            web.maindesk_page.click_first_room().sleep(1)
            web.base_page.screenshot("And 房間細節的注意事項欄位正確顯示")

            web.base_page.assert_data(
                "住客姓名", web.maindesk_page.get_roomdetail_guest_name(), "cathy"
            )

    @allure.story("綜合櫃檯 - 新增預授權")
    @pytest.mark.xdist_group("test_maindesk_flow_c")
    @pytest.mark.dependency(
        name="test_add_guest_precredit_at_maindesk",
        depends=["test_add_guest_at_maindesk"],
        scope="session",
    )
    def test_add_guest_precredit_at_maindesk(self):
        pages = [
            MaindeskPage,
            HeaderComponent,
            PreCreditComponent,
            TipComponent,
            SharePanelComponent,
            BasePage,
        ]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")

        with allure.step("Given 使用者從「綜合櫃檯」頁面進入「房間細節」視窗"):
            web.header_component.expand_menu("接待").sleep(1)
            web.header_component.to_func_page("綜合櫃檯").sleep(1)
            web.base_page.set_value_by_label("住客姓名", "Card Maindesk FLow C")
            web.base_page.search().sleep(1)
            web.maindesk_page.click_first_room().sleep(1)
            web.base_page.screenshot("Given 使用者從「綜合櫃檯」頁面進入「房間細節」視窗")

        with allure.step("And 點擊「預授權」欄位的[數字]，進入「預授權」視窗"):
            precredit_amount = int(
                web.maindesk_page.get_maindesk_precredit_amount().replace(",", "")
            )
            web.maindesk_page.click_guest_function_roomdetail("precredit_amt").sleep(1)
            web.base_page.screenshot("And 點擊「預授權」欄位的[數字]，進入「預授權」視窗")

        with allure.step("And 點擊右上[橘色鉛筆]"):
            web.maindesk_page.click_edit_precredit()
            web.base_page.screenshot("And 點擊右上[橘色鉛筆]")

        with allure.step("And 點擊表頭左側的[綠色加號]按鈕"):
            web.pre_credit_component.click_add_precredit()
            web.base_page.screenshot("And 點擊表頭左側的[綠色加號]按鈕")

        with allure.step("And 點擊選擇或輸入內容<卡別、卡號、有效月/年、授權碼、金額>"):
            web.pre_credit_component.create_precredit("VISA", 4826008693090653, "11/29", 492, 10000)
            web.base_page.screenshot("And 點擊選擇或輸入內容<卡別、卡號、有效月/年、授權碼、金額>")

        with allure.step("And 點擊[橘色磁碟片]"):
            ShareSteps.click_btn_save(
                web, save_method=lambda: web.base_page.click_toolbar_with_icon("save").sleep(1)
            )

        with allure.step("Then 顯示'儲存成功'提示"):
            ShareSteps.verify_save_success_tip(web)
            web.share_panel_component.close_panel("預授權").sleep(1)
            web.share_panel_component.close_panel("房間細節").sleep(2)

        with allure.step("And 驗證預授權資訊正確"):
            web.maindesk_page.click_first_room().sleep(1)
            new_precredit_amount = format(precredit_amount + 10000, ",")
            web.base_page.assert_data(
                "住客明細的預授權金額",
                web.maindesk_page.get_maindesk_precredit_amount(),
                new_precredit_amount,
            )

            web.maindesk_page.click_guest_function_roomdetail("precredit_amt").sleep(1)
            web.base_page.screenshot("And 驗證預授權資訊正確")
            today = datetime.now().strftime("%Y/%m/%d")
            info_list = [
                ("預刷日期", "precreditDat", today),
                ("卡別", "payWay", "31 : VISA信用卡"),
                ("卡號隱碼", "creditNos", "482600******0653"),
                ("有效月/年", "expiraDat", "11/29"),
                ("授權碼隱碼", "preauthCod", "***"),
                ("金額", "precreditAmt", "10,000"),
            ]
            for title, field, expect in info_list:
                web.base_page.assert_data(
                    title, web.pre_credit_component.get_precredit_info(field), expect
                )

            web.maindesk_page.click_edit_precredit().sleep(1)
            web.base_page.screenshot("And 驗證編輯狀態資訊正確")
            info_list = [("卡號", "creditNos", "4826008693090653"), ("授權碼", "preauthCod", "492")]
            for title, field, expect in info_list:
                web.base_page.assert_data(
                    title, web.pre_credit_component.get_precredit_info(field), expect
                )

    @allure.story("綜合櫃檯 - 新增Note")
    @pytest.mark.xdist_group("test_maindesk_flow_c")
    @pytest.mark.dependency(
        name="test_add_guest_profile_note_at_maindesk",
        depends=["test_add_guest_precredit_at_maindesk"],
        scope="session",
    )
    def test_add_guest_profile_note_at_maindesk(self):
        pages = [
            MaindeskPage,
            ReservationCardDialog,
            HeaderComponent,
            PreCreditComponent,
            TipComponent,
            SharePanelComponent,
            BasePage,
        ]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")

        with allure.step("Given 使用者從「綜合櫃檯」頁面進入「房間細節」視窗"):
            web.header_component.expand_menu("接待").sleep(1)
            web.header_component.to_func_page("綜合櫃檯").sleep(1)
            web.base_page.set_value_by_label("住客姓名", "Card Maindesk FLow C")
            web.base_page.search().sleep(1)
            web.maindesk_page.click_first_room().sleep(1)
            web.base_page.screenshot("Given 使用者從「綜合櫃檯」頁面進入「房間細節」視窗")

        with allure.step("And 點擊「Note」欄位的[綠色加號]，進入「Profile Notes」視窗"):
            has_profile_note = web.maindesk_page.has_profile_note()
            web.maindesk_page.click_guest_function_roomdetail("notes").sleep(1)
            web.base_page.screenshot("And 點擊「Note」欄位的[綠色加號]，進入「Profile Notes」視窗")

        with allure.step("And 點擊表頭左側的[綠色加號]"):
            if has_profile_note:
                web.reservation_card_dialog.click_remove_notes()
            web.reservation_card_dialog.click_add_notes()
            web.base_page.screenshot("And 點擊表頭左側的[綠色加號]")

        with allure.step("And 點擊「備註」欄位輸入備註內容"):
            text = "Note測試_" + RandomHelper.random_string(5)
            web.reservation_card_dialog.input_textarea(text)
            web.base_page.screenshot("And 點擊「備註」欄位輸入備註內容")

        with allure.step("And 點擊儲存"):
            ShareSteps.click_btn_save(
                web, save_method=lambda: web.base_page.click_toolbar_item_2("儲存").sleep(1)
            )

        with allure.step("Then 顯示'儲存成功'提示"):
            ShareSteps.verify_save_success_tip(web)
            web.share_panel_component.close_panel("Profile Notes").sleep(2)
            web.share_panel_component.close_panel("房間細節").sleep(2)

        with allure.step("And 驗證Notes正確"):
            web.maindesk_page.click_first_room().sleep(1)
            web.maindesk_page.click_guest_function_roomdetail("notes").sleep(1)
            web.base_page.screenshot("And 驗證Notes正確")
            web.base_page.assert_data(
                "Notes內容", web.reservation_card_dialog.get_notes_text(), text
            )

    @allure.story("綜合櫃檯 - 新增交辦事項")
    @pytest.mark.xdist_group("test_maindesk_flow_c")
    @pytest.mark.dependency(
        name="test_add_guest_todo_item_at_maindesk",
        depends=["test_add_guest_profile_note_at_maindesk"],
        scope="session",
    )
    def test_add_guest_todo_item_at_maindesk(self):
        pages = [
            MaindeskPage,
            ReservationCardDialog,
            HeaderComponent,
            TodolistEditComponent,
            TipComponent,
            SharePanelComponent,
            BasePage,
        ]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")

        with allure.step("Given 使用者從「綜合櫃檯」頁面進入「房間細節」視窗"):
            web.header_component.expand_menu("接待").sleep(1)
            web.header_component.to_func_page("綜合櫃檯").sleep(1)
            web.base_page.set_value_by_label("住客姓名", "Card Maindesk FLow C")
            web.base_page.search().sleep(1)
            web.maindesk_page.click_first_room().sleep(1)
            web.base_page.screenshot("Given 使用者從「綜合櫃檯」頁面進入「房間細節」視窗")

        with allure.step("And 點擊「交辦」欄位的[綠色加號]，進入「交辦事項編輯」視窗"):
            web.maindesk_page.click_guest_function_roomdetail("todo_list").sleep(1)
            web.base_page.screenshot("And 點擊「交辦」欄位的[綠色加號]，進入「交辦事項編輯」視窗")

        with allure.step("And 點擊下拉選單輸入必填欄位和<處理部門>"):
            web.base_page.click_toolbar_with_icon("add")
            web.todolist_edit_component.create_todo(["A001 : 客務部-櫃台"]).sleep(1)
            web.reservation_card_dialog.input_textarea("Test")
            web.base_page.screenshot("And 點擊下拉選單輸入必填欄位和<處理部門>")

        with allure.step("And 點擊[橘色磁碟片]"):
            ShareSteps.click_btn_save(web)

        with allure.step("Then 顯示'儲存成功'提示"):
            ShareSteps.verify_save_success_tip(web)
            web.share_panel_component.close_panel("交辦事項編輯").sleep(1)
            web.share_panel_component.close_panel("房間細節").sleep(2)

        with allure.step("And 驗證交辦事項內容"):
            web.maindesk_page.click_first_room().sleep(1)
            web.maindesk_page.click_guest_function_roomdetail("todo_list").sleep(1)
            web.base_page.screenshot("And 驗證交辦事項內容")
            info_data = [
                ("處理狀態", "proc_sta", "N"),
                ("開始日期", "begin_dat", "2024/01/05"),
                ("結束日期", "end_dat", "2024/01/06"),
                ("處理部門", "dept_sna", "櫃台"),
                ("交辦內容", "todo_rmk", "Test"),
            ]
            for title, label, target in info_data:
                web.base_page.assert_data(
                    title, web.todolist_edit_component.get_todolist_info(label), target
                )

    @allure.story("綜合櫃檯 - 新增其他提醒")
    @pytest.mark.xdist_group("test_maindesk_flow_d")
    @pytest.mark.dependency(name="test_add_guest_other_remind_at_maindesk", scope="session")
    def test_add_guest_other_remind_at_maindesk(self):
        pages = [
            MaindeskPage,
            ReservationCardDialog,
            HeaderComponent,
            TodolistEditComponent,
            TipComponent,
            SharePanelComponent,
            BasePage,
        ]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")

        with allure.step("Given 使用者從「綜合櫃檯」頁面進入「房間細節」視窗"):
            web.header_component.expand_menu("接待").sleep(1)
            web.header_component.to_func_page("綜合櫃檯").sleep(1)
            web.base_page.set_value_by_label("住客姓名", "Card Maindesk FLow D")
            web.base_page.search().sleep(1)
            web.maindesk_page.click_first_room().sleep(1)
            web.base_page.screenshot("Given 使用者從「綜合櫃檯」頁面進入「房間細節」視窗")

        with allure.step("And 點擊「提醒」欄位的[綠色加號]，進入「提醒事項」視窗"):
            web.maindesk_page.click_guest_function_roomdetail("reminder").sleep(1)
            web.base_page.screenshot("And 點擊「提醒」欄位的[綠色加號]，進入「提醒事項」視窗")

        with allure.step("And 在「其他提醒」欄位輸入內容"):
            alert_content = "其他提醒測試_" + RandomHelper.random_string(5)
            web.reservation_card_dialog.input_reservation_remind_by_field("其他提醒", alert_content)
            web.base_page.screenshot("And 在「其他提醒」欄位輸入內容")

        with allure.step("And 點擊儲存按鈕"):
            ShareSteps.click_btn_save(web)

        with allure.step("Then 顯示'儲存成功'提示"):
            ShareSteps.verify_save_success_tip(web)
            web.share_panel_component.close_panel("提醒事項").sleep(2)
            web.share_panel_component.close_panel("房間細節").sleep(2)

        with allure.step("And 驗證提醒彈窗內容正確"):
            web.maindesk_page.click_first_room().sleep(1)
            web.base_page.screenshot("And 驗證提醒彈窗內容正確")
            popup_alert_content = web.share_panel_component.get_remind_panel_content("其他提醒")
            web.base_page.assert_data("彈窗提醒內容", popup_alert_content, alert_content)
            web.share_panel_component.click_panel_footer_btn("其他提醒", "確定")

        with allure.step("And 驗證提醒內容正確"):
            web.maindesk_page.click_guest_function_roomdetail("reminder").sleep(1)
            web.base_page.screenshot("And 驗證提醒內容正確")
            web.base_page.assert_data(
                "提醒內容",
                web.reservation_card_dialog.get_reservation_remind_by_field("其他提醒"),
                alert_content,
            )

            web.reservation_card_dialog.input_reservation_remind_by_field("其他提醒", " ")
            ShareSteps.click_btn_save(web)

    @allure.story("綜合櫃檯 - 新增提醒")
    @pytest.mark.xdist_group("test_maindesk_flow_d")
    @pytest.mark.parametrize("remind_type", ["訂房提醒", "退房提醒"])
    @pytest.mark.dependency(
        name="test_add_guest_remind_at_maindesk",
        depends=["test_add_guest_other_remind_at_maindesk"],
        scope="session",
    )
    def test_add_guest_remind_at_maindesk(self, remind_type):
        pages = [
            MaindeskPage,
            ReservationCardDialog,
            HeaderComponent,
            TodolistEditComponent,
            TipComponent,
            SharePanelComponent,
            BasePage,
        ]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")

        with allure.step("Given 使用者從「綜合櫃檯」頁面進入「房間細節」視窗"):
            web.header_component.expand_menu("接待").sleep(1)
            web.header_component.to_func_page("綜合櫃檯").sleep(1)
            web.base_page.set_value_by_label("住客姓名", "Card Maindesk FLow D")
            web.base_page.search().sleep(1)
            web.maindesk_page.click_first_room().sleep(1)
            web.base_page.screenshot("Given 使用者從「綜合櫃檯」頁面進入「房間細節」視窗")

        with allure.step("And 點擊「提醒」欄位的[綠色加號]，進入「提醒事項」視窗"):
            web.maindesk_page.click_guest_function_roomdetail("reminder").sleep(1)
            web.base_page.screenshot("And 點擊「提醒」欄位的[綠色加號]，進入「提醒事項」視窗")

        with allure.step(f"And 在「{remind_type}」欄位輸入內容"):
            alert_content = f"{remind_type}測試_" + RandomHelper.random_string(5)
            web.reservation_card_dialog.input_reservation_remind_by_field(
                remind_type, alert_content
            )
            web.base_page.screenshot(f"And 在「{remind_type}」欄位輸入內容")

        with allure.step("And 點擊儲存按鈕"):
            ShareSteps.click_btn_save(web)

        with allure.step("Then 顯示'儲存成功'提示"):
            ShareSteps.verify_save_success_tip(web)
            web.share_panel_component.close_panel("提醒事項").sleep(2)
            web.share_panel_component.close_panel("房間細節").sleep(2)

        with allure.step("And 驗證提醒內容正確"):
            web.maindesk_page.click_first_room().sleep(1)
            web.maindesk_page.click_guest_function_roomdetail("reminder").sleep(1)
            web.base_page.screenshot("And 驗證提醒內容正確")
            web.base_page.assert_data(
                "提醒內容",
                web.reservation_card_dialog.get_reservation_remind_by_field(remind_type),
                alert_content,
            )
            web.share_panel_component.close_panel("提醒事項")

        with allure.step("And 驗證提醒彈窗內容正確"):
            if remind_type == "訂房提醒":
                web.maindesk_page.click_toolbar_button_roomdetail("訂房卡").sleep(2)
            elif remind_type == "退房提醒":
                web.maindesk_page.click_guest_function_roomdetail("unpaid_amt").sleep(2)
                ShareSteps.open_shift(web, "FO : 飯店櫃檯", "a", "autotest")

            popup_alert_content = web.share_panel_component.get_remind_panel_content(remind_type)
            web.base_page.screenshot("And 驗證提醒彈窗內容正確")
            web.base_page.assert_data("彈窗提醒內容", popup_alert_content, alert_content)

    @allure.story("綜合櫃檯 - 新增留言")
    @pytest.mark.xdist_group("test_maindesk_flow_d")
    @pytest.mark.dependency(
        name="test_add_guest_message_at_maindesk",
        depends=["test_add_guest_remind_at_maindesk"],
        scope="session",
    )
    def test_add_guest_message_at_maindesk(self):
        pages = [
            MaindeskPage,
            ReservationCardDialog,
            HeaderComponent,
            MessageEditComponent,
            TipComponent,
            SharePanelComponent,
            BasePage,
        ]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")

        with allure.step("Given 使用者從「綜合櫃檯」頁面進入「房間細節」視窗"):
            web.header_component.expand_menu("接待").sleep(1)
            web.header_component.to_func_page("綜合櫃檯").sleep(1)
            web.base_page.set_value_by_label("住客姓名", "Card Maindesk FLow D")
            web.base_page.search().sleep(1)
            web.maindesk_page.click_first_room().sleep(1)
            web.base_page.screenshot("Given 使用者從「綜合櫃檯」頁面進入「房間細節」視窗")

        with allure.step("And 點擊「提醒」欄位的[綠色加號]，進入「提醒事項」視窗"):
            web.maindesk_page.click_guest_function_roomdetail("message").sleep(1)
            web.base_page.screenshot("And 點擊「提醒」欄位的[綠色加號]，進入「提醒事項」視窗")

        with allure.step("And 點擊下拉選單選擇或者輸入必填內容"):
            if web.message_edit_component.has_message():
                web.message_edit_component.click_delete_message()
                web.tip_component.click_ok()
                web.tip_component.click_ok()
                web.maindesk_page.click_guest_function_roomdetail("message").sleep(1)
            message_from = f"{names.get_first_name()} {names.get_last_name()}"
            phone_number = RandomHelper.generate_phone_mobile()
            message_content = "留言測試_" + RandomHelper.random_string(10)

            web.message_edit_component.fill_message_fields(
                message_from, phone_number, message_content
            )
            web.base_page.screenshot("And 點擊下拉選單選擇或者輸入必填內容")

        with allure.step("And 點擊右上的[橘色磁碟片]儲存"):
            ShareSteps.click_btn_save(web)

        with allure.step("Then 顯示'新增成功'"):
            ShareSteps.verify_save_success_tip(web, "新增成功")
            initial_data = {
                "guest_name": web.message_edit_component.get_message_field_value("住客姓名"),
                "guest_status": web.message_edit_component.get_message_field_value("住客狀態"),
                "card_no": web.message_edit_component.get_message_field_value("訂房卡號"),
                "message_no": web.message_edit_component.get_message_field_value("留言編號"),
                "message_time": web.message_edit_component.get_message_field_value("留言時間"),
                "create_date": web.message_edit_component.get_message_field_value("新增日"),
                "modify_date": web.message_edit_component.get_message_field_value("修改日"),
            }

            web.share_panel_component.close_panel("留言編輯")
            web.share_panel_component.close_panel("房間細節").sleep(2)

        with allure.step("And 驗證留言編輯視窗的所有欄位"):
            web.maindesk_page.click_first_room().sleep(1)
            web.maindesk_page.click_guest_function_roomdetail("message").sleep(1)
            web.base_page.screenshot("And 驗證留言編輯視窗的所有欄位")

            field_validations = [
                ("住客姓名", initial_data["guest_name"]),
                ("住客狀態", initial_data["guest_status"]),
                ("訂房卡號", initial_data["card_no"]),
                ("入住日期", "2024/01/05"),
                ("退房日期", "2024/01/06"),
                ("留言編號", initial_data["message_no"]),
                ("留言狀態", "N : 新留言"),
                ("留言日期", datetime.now().strftime("%Y/%m/%d")),
                ("留言時間", initial_data["message_time"]),
                ("留言者", message_from),
                ("連絡電話", phone_number),
                ("留言內容", message_content),
                ("新增日期", initial_data["create_date"]),
                ("新增者", "autotest"),
                ("修改日期", initial_data["modify_date"]),
                ("修改者", "autotest"),
            ]

            for title, expected in field_validations:
                web.base_page.assert_data(
                    title, web.message_edit_component.get_message_field_value(title), expected
                )

        with allure.step("And 驗證留言表格資料"):
            web.base_page.screenshot("And 驗證留言表格資料")
            for title, col, expected in [
                ("留言狀態", "1", "N : 新留言"),
                ("留言日期", "2", datetime.now().strftime("%Y/%m/%d")),
                ("留言時間", "3", initial_data["message_time"]),
                ("入住日", "5", "2024/01/05"),
                ("退房日", "6", "2024/01/06"),
                ("住客狀態", "7", initial_data["guest_status"]),
            ]:
                web.base_page.assert_data(
                    title, web.message_edit_component.get_message_grid_cell_text(col), expected
                )

    @allure.story("綜合櫃檯 - 新增失物")
    @pytest.mark.xdist_group("test_maindesk_flow_d")
    @pytest.mark.dependency(
        name="test_add_guest_lost_at_maindesk",
        depends=["test_add_guest_remind_at_maindesk"],
        scope="session",
    )
    def test_add_guest_lost_at_maindesk(self):
        pages = [
            MaindeskPage,
            LostManagementPage,
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            BasePage,
        ]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")

        with allure.step("Given 使用者從「綜合櫃檯」頁面進入「房間細節」視窗"):
            web.header_component.expand_menu("接待").sleep(1)
            web.header_component.to_func_page("綜合櫃檯").sleep(1)
            web.base_page.set_value_by_label("住客姓名", "Card Maindesk FLow D")
            web.base_page.search().sleep(1)
            web.maindesk_page.click_first_room().sleep(1)
            web.base_page.screenshot("Given 使用者從「綜合櫃檯」頁面進入「房間細節」視窗")

        with allure.step("And 點擊「提醒」欄位的[綠色加號]，進入「提醒事項」視窗"):
            web.maindesk_page.click_guest_function_roomdetail("lost").sleep(1)
            web.base_page.screenshot("And 點擊「提醒」欄位的[綠色加號]，進入「提醒事項」視窗")

        with allure.step("And 選擇[狀態]為<遺失>"):
            if web.lost_management_page.item_enabled("remove"):
                web.base_page.click_toolbar_with_icon("remove")
                web.tip_component.click_ok()
                web.base_page.click_toolbar_with_icon("add")
            web.lost_management_page.select_status_in_dialog("遺失")
            web.base_page.screenshot("And 選擇[狀態]為<遺失>")

        with allure.step("And 輸入[物品名稱]"):
            lost_item_name = "lost_" + RandomHelper.random_string(3)
            web.base_page.set_value_by_label("物品名稱", lost_item_name)
            web.base_page.screenshot("And 輸入[物品名稱]")

        with allure.step("And 點擊[橘色磁碟片]進行儲存"):
            web.base_page.click_toolbar_with_icon("save").sleep(1)
            web.base_page.screenshot("And 點擊[橘色磁碟片]進行儲存")

        with allure.step("Then 顯示'儲存成功'提示"):
            web.base_page.screenshot("顯示'儲存成功'提示")
            web.base_page.assert_data("儲存成功", web.tip_component.get_tip_text(), "儲存成功")
            web.tip_component.click_ok()
            web.share_panel_component.close_panel("編輯失物")
            web.share_panel_component.close_panel("房間細節").sleep(2)

        with allure.step("And 驗證失物資料"):
            web.maindesk_page.click_first_room().sleep(1)
            web.maindesk_page.click_guest_function_roomdetail("lost").sleep(1)
            today = datetime.now().strftime("%Y/%m/%d")
            web.lost_management_page.screenshot("And 驗證失物資料")
            web.lost_management_page.assert_data(
                "遺失日期",
                web.lost_management_page.get_lost_item_data_from_dialog("lostDate"),
                today,
            )
            web.lost_management_page.assert_data(
                "物品名稱",
                web.lost_management_page.get_lost_item_data_from_dialog("item"),
                lost_item_name,
            )
            web.lost_management_page.assert_data(
                "狀態", web.lost_management_page.get_lost_item_data_from_dialog("status"), "遺失"
            )

    @allure.story("綜合櫃檯 - 新增接送服務")
    @pytest.mark.xdist_group("test_maindesk_flow_d")
    @pytest.mark.dependency(
        name="test_add_transport_service_at_maindesk",
        depends=["test_add_guest_message_at_maindesk"],
        scope="session",
    )
    def test_add_transport_service_at_maindesk(self):
        pages = [
            MaindeskPage,
            HeaderComponent,
            TransportServicesComponent,
            TipComponent,
            SharePanelComponent,
            BasePage,
        ]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")

        with allure.step("Given 使用者從「綜合櫃檯」頁面進入「房間細節」視窗"):
            web.header_component.expand_menu("接待").sleep(1)
            web.header_component.to_func_page("綜合櫃檯").sleep(1)
            web.base_page.set_value_by_label("住客姓名", "Card Maindesk FLow D")
            web.base_page.search().sleep(1)
            web.maindesk_page.click_first_room().sleep(1)
            web.base_page.screenshot("Given 使用者從「綜合櫃檯」頁面進入「房間細節」視窗")

        with allure.step("When 點擊接送欄位值之[綠色加號]進行編輯"):
            web.maindesk_page.click_guest_function_roomdetail("transfer").sleep(2)
            web.base_page.screenshot("When 點擊接送欄位值之[綠色加號]進行編輯")

        with allure.step("And 點擊下拉選單選擇或輸入接送視窗必填欄位"):
            if web.transport_services_component.has_transport_service():
                web.base_page.click_toolbar_with_icon("remove")
                web.tip_component.click_ok()
            web.transport_services_component.set_transport_service().sleep(1)
            input_time = web.transport_services_component.get_transport_field_value("時間")
            web.base_page.screenshot("And 點擊下拉選單選擇或輸入接送視窗必填欄位")

        with allure.step("And 記錄初始值"):
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
            web.base_page.screenshot("And 記錄初始值")

        with allure.step("And 點擊[橘色磁碟片]進行儲存"):
            web.base_page.click_toolbar_with_icon("save").sleep(1)
            web.base_page.screenshot("And 點擊[橘色磁碟片]進行儲存")

        with allure.step("Then 顯示「儲存成功」提示"):
            ShareSteps.verify_save_success_tip(web)
            web.share_panel_component.close_panel("接送服務編輯").sleep(1)
            web.share_panel_component.close_panel("房間細節").sleep(2)

        with allure.step("And 視窗右方接送之Table新增資料列"):
            web.maindesk_page.click_first_room().sleep(1)
            web.maindesk_page.click_guest_function_roomdetail("transfer").sleep(2)
            web.base_page.screenshot("And 視窗右方接送之Table新增資料列")

            # 驗證表格資料筆數
            row_count = web.transport_services_component.get_transport_row_count()
            web.base_page.assert_data("接送服務表格資料筆數", row_count, 1)

        with allure.step("And 驗證接送服務表單欄位值"):
            web.transport_services_component.click_transport_grid_last_row().sleep(1)
            web.base_page.screenshot("And 驗證接送服務表單欄位值")

            field_validations = [
                ("接/送", "combobox", "接/送", initial_values["type"]),
                ("日期", "field", "日期", initial_values["date"]),
                ("時間", "field", "時間", input_time),
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

        with allure.step("And 驗證接送表格資料"):
            web.base_page.screenshot("And 驗證接送表格資料")
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

    @allure.story("綜合櫃檯 - 住客新增車號")
    @pytest.mark.xdist_group("test_maindesk_flow_e")
    @pytest.mark.dependency(name="test_add_car_number_at_maindesk", scope="session")
    def test_add_car_number_at_maindesk(self):
        pages = [MaindeskPage, HeaderComponent, TipComponent, SharePanelComponent, BasePage]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")

        with allure.step("Given 使用者從「綜合櫃檯」頁面進入「房間細節」視窗"):
            web.header_component.expand_menu("接待").sleep(1)
            web.header_component.to_func_page("綜合櫃檯").sleep(1)
            web.base_page.set_value_by_label("住客姓名", "Card Maindesk Flow E")
            web.base_page.search().sleep(1)
            web.maindesk_page.click_first_room().sleep(1)
            web.base_page.screenshot("Given 使用者從「綜合櫃檯」頁面進入「房間細節」視窗")

        with allure.step("When 點擊[橘色筆]進行編輯"):
            web.base_page.click_toolbar_with_icon("edit").sleep(2)
            web.base_page.screenshot("When 點擊[橘色筆]進行編輯")

        with allure.step("And 下方資料表滾輪右移、點擊輸入[車號]欄位值"):
            car_number = "ABC-" + str(RandomHelper.random_number())
            web.maindesk_page.click_edit_card_nos_button()
            web.maindesk_page.input_car_nos(car_number).sleep(1)
            web.maindesk_page.click_confirm_button()
            web.base_page.screenshot("And 下方資料表滾輪右移、點擊輸入[車號]欄位值")

        with allure.step("And 點擊[橘色磁碟片]進行儲存"):
            ShareSteps.click_btn_save(web)
            web.base_page.screenshot("And 點擊[橘色磁碟片]進行儲存")

        with allure.step("Then 顯示'儲存成功'提示"):
            ShareSteps.verify_save_success_tip(web)
            web.share_panel_component.close_panel("房間細節").sleep(2)

        with allure.step("And 依輸入車號內容顯示[車號]欄位值"):
            web.maindesk_page.click_first_room().sleep(1)
            web.base_page.screenshot("And 依輸入車號內容顯示[車號]欄位值")

            web.base_page.click_toolbar_with_icon("edit").sleep(2)
            web.maindesk_page.click_edit_card_nos_button()
            web.base_page.assert_data("車號", web.maindesk_page.get_car_nos(), car_number)

    @allure.story("綜合櫃檯 - 新增住客備註")
    @pytest.mark.xdist_group("test_maindesk_flow_e")
    @pytest.mark.dependency(
        name="test_add_guest_remark_at_maindesk",
        depends=["test_add_car_number_at_maindesk"],
        scope="session",
    )
    def test_add_guest_remark_at_maindesk(self):
        pages = [MaindeskPage, HeaderComponent, TipComponent, SharePanelComponent, BasePage]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")

        with allure.step("Given 使用者從「綜合櫃檯」頁面進入「房間細節」視窗"):
            web.header_component.expand_menu("接待").sleep(1)
            web.header_component.to_func_page("綜合櫃檯").sleep(1)
            web.base_page.set_value_by_label("住客姓名", "Card Maindesk Flow E")
            web.base_page.search().sleep(1)
            web.maindesk_page.click_first_room().sleep(1)
            web.base_page.screenshot("Given 使用者從「綜合櫃檯」頁面進入「房間細節」視窗")

        with allure.step("When 點擊[橘色筆]進行編輯"):
            web.base_page.click_toolbar_with_icon("edit").sleep(2)
            web.base_page.screenshot("When 點擊[橘色筆]進行編輯")

        with allure.step("And 下方資料表滾輪右移、點擊輸入[住客備註]欄位值"):
            guest_remark = "測試備註-" + RandomHelper.random_string()
            web.maindesk_page.input_guest_remark(guest_remark).sleep(1)
            web.base_page.screenshot("And 下方資料表滾輪右移、點擊輸入[住客備註]欄位值")

        with allure.step("And 點擊[橘色磁碟片]進行儲存"):
            ShareSteps.click_btn_save(web)
            web.base_page.screenshot("And 點擊[橘色磁碟片]進行儲存")

        with allure.step("Then 顯示'儲存成功'提示訊息"):
            ShareSteps.verify_save_success_tip(web)
            web.share_panel_component.close_panel("房間細節").sleep(2)

        with allure.step("And 依輸入住客備註內容顯示[住客備註]欄位值"):
            web.maindesk_page.click_first_room().sleep(1)
            web.base_page.screenshot("And 依輸入住客備註內容顯示[住客備註]欄位值")

            web.base_page.click_toolbar_with_icon("edit").sleep(2)
            web.base_page.assert_data(
                "住客備註", web.maindesk_page.get_guest_remark(), guest_remark
            )
