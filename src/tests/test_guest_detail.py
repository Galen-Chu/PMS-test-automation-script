from datetime import datetime
import allure
import pytest
import names

from pages.base_page import BasePage
from pages.components.share_panel_component import SharePanelComponent
from pages.components.tip_component import TipComponent
from pages.components.header_component import HeaderComponent
from pages.components.todolist_edit_component import TodolistEditComponent
from pages.components.message_edit_component import MessageEditComponent
from pages.components.pre_credit_component import PreCreditComponent
from pages.dialogs.reservation_card_dialog import ReservationCardDialog
from pages.reservation_page import ReservationPage
from tests.share_steps import ShareSteps
from tools.driver_helper import DriverHelper
from tools.random_helper import RandomHelper


@allure.feature("住客明細")
class TestGuestDetail:

    @allure.story("新增一筆住客資料")
    @pytest.mark.xdist_group("add_and_edit_guest")
    @pytest.mark.dependency(name="test_add_one_guest", scope="session")
    def test_add_one_guest(self):
        pages = [
            ReservationCardDialog,
            HeaderComponent,
            TipComponent,
            ReservationPage,
            SharePanelComponent,
            BasePage,
        ]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")

        with allure.step("Given 使用者進入「訂房明細」視窗"):
            ShareSteps.create_or_enter_reservation_detail(
                web,
                "quickSearch",
                "Card Guest Add",
                "doOpenDtDetailDialog",
                "Card",
                "Guest Add",
                "現場訂房含早",
                3,
            )
            web.base_page.screenshot("Given 使用者進入「訂房明細」視窗")

        with allure.step("And 刪除舊住客明細"):
            if web.reservation_card_dialog.get_tab_empty_msg("guest") != "無任何資料":
                for _ in range(web.reservation_card_dialog.get_guest_row_count()):
                    web.reservation_card_dialog.click_tab_toolbar("guest", "刪除")
            web.base_page.screenshot("And 刪除舊住客明細")

        with allure.step("And 點擊右側表格「住客」頁籤中的[綠色加號]"):
            web.reservation_card_dialog.click_tab_add_btn("guest").sleep(2)
            web.base_page.screenshot("And 點擊右側表格「住客」頁籤中的[綠色加號]")

        with allure.step("And 點擊輸入框旁邊的[...]，新增一筆住客歷史"):
            web.reservation_card_dialog.click_edit_guest()
            first_name = names.get_first_name()
            last_name = names.get_last_name()
            web.reservation_page.create_guest(
                first_name, last_name, "Miss.", RandomHelper.generate_phone_mobile()
            )
            web.tip_component.click_ok().sleep(1)
            web.share_panel_component.close_panel("住客歷史").sleep(1)
            web.base_page.screenshot("And 點擊輸入框旁邊的[...]，新增一筆住客歷史")

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

        with allure.step("And 驗證住客資料正確"):
            web.reservation_card_dialog.click_card_toolbar("doOpenDtDetailDialog").sleep(1)
            web.base_page.screenshot("And 驗證住客資料正確")
            web.base_page.assert_data(
                "住客姓名",
                web.reservation_card_dialog.get_guest_table_info_by_row(),
                [first_name + " " + last_name],
            )

    @allure.story("新增多筆住客資料")
    @pytest.mark.xdist_group("add_and_edit_guest")
    @pytest.mark.dependency(
        name="test_add_several_guests", depends=["test_add_one_guest"], scope="session"
    )
    def test_add_several_guests(self):
        pages = [
            ReservationCardDialog,
            HeaderComponent,
            TipComponent,
            ReservationPage,
            SharePanelComponent,
            BasePage,
        ]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")

        with allure.step("Given 使用者進入「訂房明細」視窗"):
            ShareSteps.create_or_enter_reservation_detail(
                web, "quickSearch", "Card Guest Add", "doOpenDtDetailDialog"
            )
            web.base_page.screenshot("Given 使用者進入「訂房明細」視窗")

        with allure.step("And 刪除舊住客明細"):
            if web.reservation_card_dialog.get_tab_empty_msg("guest") != "無任何資料":
                web.base_page.sleep(1)
                for _ in range(web.reservation_card_dialog.get_guest_row_count()):
                    web.reservation_card_dialog.click_tab_toolbar("guest", "刪除")
            web.base_page.screenshot("And 刪除舊住客明細")

        with allure.step("And 重複步驟，新增多筆住客明細"):
            name_list = []
            for _ in range(3):
                web.reservation_card_dialog.click_tab_add_btn("guest").sleep(2)
                web.reservation_card_dialog.click_edit_guest()
                first_name = names.get_first_name()
                last_name = names.get_last_name()
                web.reservation_page.create_guest(
                    first_name, last_name, "Miss.", RandomHelper.generate_phone_mobile()
                )
                web.tip_component.click_ok().sleep(1)
                web.share_panel_component.close_panel("住客歷史").sleep(3)
                name_list.append(first_name + " " + last_name)
            web.base_page.screenshot("And 重複步驟，新增多筆住客明細")
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

        with allure.step("And 驗證住客資料正確"):
            web.reservation_card_dialog.click_card_toolbar("doOpenDtDetailDialog").sleep(1)
            web.base_page.screenshot("And 驗證住客資料正確")
            web.base_page.assert_data(
                "住客姓名", web.reservation_card_dialog.get_guest_table_info_by_row(), name_list
            )

    @allure.story("編輯住客資料")
    @pytest.mark.xdist_group("add_and_edit_guest")
    @pytest.mark.dependency(
        name="test_edit_guest", depends=["test_add_several_guests"], scope="session"
    )
    def test_edit_guest(self):
        pages = [
            ReservationCardDialog,
            HeaderComponent,
            TipComponent,
            ReservationPage,
            SharePanelComponent,
            BasePage,
        ]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")

        with allure.step("Given 使用者進入「訂房明細」視窗"):
            ShareSteps.create_or_enter_reservation_detail(
                web, "quickSearch", "Card Guest Add", "doOpenDtDetailDialog"
            )
            web.base_page.screenshot("Given 使用者進入「訂房明細」視窗")

        with allure.step("And 點擊輸入框旁邊的[...]，新增一筆住客歷史"):
            web.reservation_card_dialog.click_tab_toolbar("guest", "編輯")
            web.reservation_card_dialog.click_edit_guest()
            web.base_page.click_toolbar_with_icon("add")
            first_name = names.get_first_name()
            last_name = names.get_last_name()
            web.reservation_page.create_guest(
                first_name, last_name, "Miss.", RandomHelper.generate_phone_mobile()
            )
            web.tip_component.click_ok().sleep(1)
            web.share_panel_component.close_panel("住客歷史").sleep(1)
            name_list = web.reservation_card_dialog.get_guest_table_info_by_row()
            web.base_page.screenshot("And 點擊輸入框旁邊的[...]，新增一筆住客歷史")

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

        with allure.step("And 驗證住客資料正確"):
            web.reservation_card_dialog.click_card_toolbar("doOpenDtDetailDialog").sleep(1)
            web.base_page.screenshot("And 驗證住客資料正確")
            web.base_page.assert_data(
                "住客姓名", web.reservation_card_dialog.get_guest_table_info_by_row(), name_list
            )

    @allure.story("刪除一筆住客資料")
    @pytest.mark.xdist_group("add_and_edit_guest")
    @pytest.mark.dependency(
        name="test_delete_one_guest", depends=["test_edit_guest"], scope="session"
    )
    def test_delete_one_guest(self):
        pages = [
            ReservationCardDialog,
            HeaderComponent,
            TipComponent,
            ReservationPage,
            SharePanelComponent,
            BasePage,
        ]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")

        with allure.step("Given 使用者進入「訂房明細」視窗"):
            ShareSteps.create_or_enter_reservation_detail(
                web, "quickSearch", "Card Guest Add", "doOpenDtDetailDialog"
            )
            web.base_page.screenshot("Given 使用者進入「訂房明細」視窗")

        with allure.step("And 點擊一筆右側表格「住客」頁籤中想刪除的資料列的[垃圾桶]"):
            web.reservation_card_dialog.click_tab_toolbar("guest", "刪除").sleep(2)
            name_list = web.reservation_card_dialog.get_guest_table_info_by_row()
            web.base_page.screenshot("And 點擊一筆右側表格「住客」頁籤中想刪除的資料列的[垃圾桶]")

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

        with allure.step("And 驗證住客資料正確"):
            web.reservation_card_dialog.click_card_toolbar("doOpenDtDetailDialog").sleep(1)
            web.base_page.screenshot("And 驗證住客資料正確")
            web.base_page.assert_data(
                "住客姓名", web.reservation_card_dialog.get_guest_table_info_by_row(), name_list
            )

    @allure.story("多位住客-新增交辦事項-多選處理部門")
    @pytest.mark.xdist_group("add_and_edit_guest")
    @pytest.mark.dependency(
        name="test_add_todo_with_multi_department",
        depends=["test_delete_one_guest"],
        scope="session",
    )
    def test_add_todo_with_multi_department(self):
        pages = [
            ReservationCardDialog,
            TodolistEditComponent,
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            ReservationPage,
            BasePage,
        ]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")

        with allure.step("Given 使用者進入「訂房明細」視窗"):
            ShareSteps.create_or_enter_reservation_detail(
                web, "quickSearch", "Card Guest Add", "doOpenDtDetailDialog"
            )
            web.base_page.screenshot("Given 使用者進入「訂房明細」視窗")

        with allure.step("And 選擇第一位住客點擊編輯"):
            web.reservation_card_dialog.click_tab_toolbar("guest", "編輯")
            web.base_page.screenshot("And 選擇第一位住客點擊編輯")

        with allure.step("And 點擊「交辦」欄位的[綠色加號]，進入「交辦事項編輯」視窗"):
            web.reservation_card_dialog.click_tab_guest_function("todoListButton").sleep(1)
            web.base_page.screenshot("And 點擊「交辦」欄位的[綠色加號]，進入「交辦事項編輯」視窗")

        with allure.step("And 新增交辦事項並選擇多個處理部門"):
            web.base_page.click_toolbar_with_icon("add")
            web.todolist_edit_component.create_todo(["A001 : 客務部-櫃台", "213 : 中式餐廳"]).sleep(
                1
            )
            web.reservation_card_dialog.input_textarea("Test")
            web.base_page.screenshot("And 新增交辦事項並選擇多個處理部門")

        with allure.step("And 點擊[橘色磁碟片]儲存"):
            ShareSteps.click_btn_save(web)

        with allure.step("Then 顯示'儲存成功'提示"):
            ShareSteps.verify_save_success_tip(web)
            web.share_panel_component.close_panel("交辦事項編輯").sleep(1)

        with allure.step("And 驗證住客明細的交辦欄位狀態"):
            web.base_page.close_panel()
            web.reservation_card_dialog.click_card_toolbar("doOpenDtDetailDialog").sleep(1)
            web.base_page.screenshot("And 驗證住客明細的交辦欄位狀態")
            guest_todo_status = web.reservation_card_dialog.get_all_guests_todo_status()
            web.base_page.assert_data("住客交辦狀態", guest_todo_status, [False, True])

    @allure.story("新增Note")
    @pytest.mark.xdist_group("test_guest_funcion")
    @pytest.mark.dependency(name="test_add_guest_note", scope="session")
    def test_add_guest_note(self, cache):
        pages = [
            ReservationCardDialog,
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            ReservationPage,
            BasePage,
        ]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")

        with allure.step("Given 使用者進入「訂房明細」視窗"):
            first_name = names.get_first_name()
            last_name = names.get_last_name()
            cache.set("full_name_guest_function", f"{first_name} {last_name}")
            ShareSteps.create_or_enter_reservation_detail(
                web,
                "guestName",
                f"{first_name} {last_name}",
                "doOpenDtDetailDialog",
                first_name,
                last_name,
                "現場訂房含早",
                1,
            )
            web.base_page.screenshot("Given 使用者進入「訂房明細」視窗")

        with allure.step("And 點擊右側表格「住客」頁籤中想修改的資料列的[黑色鉛筆]"):
            web.reservation_card_dialog.click_tab_toolbar("guest", "編輯").sleep(1)
            web.base_page.screenshot("And 點擊右側表格「住客」頁籤中想修改的資料列的[黑色鉛筆]")

        with allure.step("And 點擊「Note」欄位的[綠色加號]，進入「Profile Notes」視窗"):
            web.reservation_card_dialog.click_tab_guest_function("notesButton").sleep(1)
            web.base_page.screenshot("And 點擊「Note」欄位的[綠色加號]，進入「Profile Notes」視窗")

        with allure.step("And 點擊表頭左側的[綠色加號]"):
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

        with allure.step("And 驗證Notes正確"):
            web.reservation_card_dialog.click_tab_toolbar("guest", "編輯").sleep(1)
            web.reservation_card_dialog.click_tab_guest_function("notesButton").sleep(1)
            web.base_page.screenshot("And 驗證Notes正確")
            web.base_page.assert_data(
                "Notes內容", web.reservation_card_dialog.get_notes_text(), text
            )

    @allure.story("新增一筆預授權")
    @pytest.mark.xdist_group("test_guest_funcion")
    @pytest.mark.dependency(
        name="test_add_guest_precredit", depends=["test_add_guest_note"], scope="session"
    )
    def test_add_guest_precredit(self, cache):
        pages = [
            ReservationCardDialog,
            PreCreditComponent,
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            ReservationPage,
            BasePage,
        ]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")
        full_name = cache.get("full_name_guest_function", "")

        with allure.step("Given 使用者進入「訂房明細」視窗"):
            ShareSteps.create_or_enter_reservation_detail(
                web, "quickSearch", full_name, "doOpenDtDetailDialog"
            )
            web.base_page.screenshot("Given 使用者進入「訂房明細」視窗")

        with allure.step("And 點擊「預授權」欄位的[數字]，進入「預授權」視窗"):
            precredit_amount = int(
                web.reservation_card_dialog.get_precredit_amount().replace(",", "")
            )
            web.reservation_card_dialog.click_precredit().sleep(1)
            web.base_page.screenshot("And 點擊「預授權」欄位的[數字]，進入「預授權」視窗")

        with allure.step("And 點擊右上[橘色鉛筆]"):
            web.base_page.click_toolbar_with_icon("edit")
            web.base_page.screenshot("And 點擊右上[橘色鉛筆]")

        with allure.step("And 點擊表頭左側的[綠色加號]"):
            web.pre_credit_component.click_add_precredit()
            web.base_page.screenshot("And 點擊表頭左側的[綠色加號]")

        with allure.step("And 點擊選擇或輸入內容<卡別、卡號、有效月/年、授權碼、金額>"):
            web.pre_credit_component.create_precredit("VISA", 4826008693090653, "11/29", 492, 10000)
            web.base_page.screenshot("And 點擊選擇或輸入內容<卡別、卡號、有效月/年、授權碼、金額>")

        with allure.step("And 點擊[橘色磁碟片]儲存"):
            ShareSteps.click_btn_save(
                web, save_method=lambda: web.base_page.click_toolbar_with_icon("save").sleep(1)
            )

        with allure.step("Then 顯示'儲存成功'提示"):
            ShareSteps.verify_save_success_tip(web)
            web.share_panel_component.close_panel("預授權").sleep(1)
            web.reservation_card_dialog.click_detail_toolbar("save").sleep(1)
            web.tip_component.click_ok()
            web.base_page.close_panel()

        with allure.step("And 驗證預授權資訊正確"):
            web.reservation_card_dialog.click_card_toolbar("doOpenDtDetailDialog").sleep(1)
            new_precredit_amount = format(precredit_amount + 10000, ",")
            web.base_page.assert_data(
                "住客明細的預授權金額",
                web.reservation_card_dialog.get_precredit_amount(),
                new_precredit_amount,
            )
            web.reservation_card_dialog.click_precredit().sleep(1)
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

            web.base_page.click_toolbar_with_icon("edit").sleep(1)
            info_list = [("卡號", "creditNos", "4826008693090653"), ("授權碼", "preauthCod", "492")]
            for title, field, expect in info_list:
                web.base_page.assert_data(
                    title, web.pre_credit_component.get_precredit_info(field), expect
                )

    @allure.story("預授權建立後無法刪除")
    @pytest.mark.xdist_group("test_guest_funcion")
    @pytest.mark.dependency(
        name="test_btn_del_precredit_disable", depends=["test_add_guest_precredit"], scope="session"
    )
    def test_btn_del_precredit_disable(self, cache):
        pages = [
            ReservationCardDialog,
            PreCreditComponent,
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            ReservationPage,
            BasePage,
        ]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")
        full_name = cache.get("full_name_guest_function", "")

        with allure.step("Given 使用者進入「訂房明細」視窗"):
            ShareSteps.create_or_enter_reservation_detail(
                web, "quickSearch", full_name, "doOpenDtDetailDialog"
            )
            web.base_page.screenshot("Given 使用者進入「訂房明細」視窗")

        with allure.step("And 點擊「預授權」欄位的[數字]，進入「預授權」視窗"):
            web.reservation_card_dialog.click_precredit().sleep(1)
            web.base_page.screenshot("And 點擊「預授權」欄位的[數字]，進入「預授權」視窗")

        with allure.step("And 點擊右上[橘色鉛筆]"):
            web.base_page.click_toolbar_with_icon("edit")
            web.base_page.screenshot("And 點擊右上[橘色鉛筆]")

        with allure.step("Then 驗證預授權不可刪除"):
            web.base_page.screenshot("Then 驗證預授權不可刪除")
            web.base_page.assert_data(
                "預授權刪除按鈕狀態",
                web.pre_credit_component.btn_del_precredit_is_enabled(),
                "true",
            )

    @allure.story("新增交辦事項")
    @pytest.mark.xdist_group("test_guest_funcion")
    @pytest.mark.dependency(
        name="test_add_todo_item", depends=["test_btn_del_precredit_disable"], scope="session"
    )
    def test_add_todo_item(self, cache):
        pages = [
            ReservationCardDialog,
            TodolistEditComponent,
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            ReservationPage,
            BasePage,
        ]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")
        full_name = cache.get("full_name_guest_function", "")

        with allure.step("Given 使用者進入「訂房明細」視窗"):
            ShareSteps.create_or_enter_reservation_detail(
                web, "quickSearch", full_name, "doOpenDtDetailDialog"
            )
            web.base_page.screenshot("Given 使用者進入「訂房明細」視窗")

        with allure.step("And 點擊右側表格「住客」頁籤中想修改的資料列的[黑色鉛筆]"):
            web.reservation_card_dialog.click_tab_toolbar("guest", "編輯")
            web.base_page.screenshot("And 點擊右側表格「住客」頁籤中想修改的資料列的[黑色鉛筆]")

        with allure.step("And 點擊「交辦」欄位的[綠色加號]，進入「交辦事項編輯」視窗"):
            web.reservation_card_dialog.click_tab_guest_function("todoListButton").sleep(1)
            web.base_page.screenshot("And 點擊「交辦」欄位的[綠色加號]，進入「交辦事項編輯」視窗")

        with allure.step("And 點擊下拉選單選擇或輸入必填欄位和<處理部門>"):
            web.base_page.click_toolbar_with_icon("add")
            web.todolist_edit_component.create_todo(["A001 : 客務部-櫃台"]).sleep(1)
            web.reservation_card_dialog.input_textarea("Test")
            web.base_page.screenshot("And 點擊下拉選單選擇或輸入必填欄位和<處理部門>")

        with allure.step("And 點擊[橘色磁碟片]儲存"):
            ShareSteps.click_btn_save(web)

        with allure.step("Then 顯示'儲存成功'提示"):
            ShareSteps.verify_save_success_tip(web)
            web.share_panel_component.close_panel("交辦事項編輯").sleep(1)
            web.base_page.close_panel()

        with allure.step("And 驗證交辦事項內容"):
            web.reservation_card_dialog.click_card_toolbar("doOpenDtDetailDialog").sleep(1)
            web.reservation_card_dialog.click_tab_toolbar("guest", "編輯")
            web.reservation_card_dialog.click_tab_guest_function("todoListButton").sleep(1)
            web.base_page.screenshot("And 驗證交辦事項內容")
            info_list = [
                ("處理狀態", "proc_sta", "N"),
                ("開始日期", "begin_dat", "2024/01/05"),
                ("結束日期", "end_dat", "2024/01/06"),
                ("處理部門", "dept_sna", "櫃台"),
                ("交辦內容", "todo_rmk", "Test"),
            ]
            for title, label, target in info_list:
                web.base_page.assert_data(
                    title, web.todolist_edit_component.get_todolist_info(label), target
                )

    @allure.story("編輯交辦事項狀態為已處理")
    @pytest.mark.xdist_group("test_guest_funcion")
    @pytest.mark.dependency(
        name="test_edit_todo_to_completed", depends=["test_add_todo_item"], scope="session"
    )
    def test_edit_todo_to_completed(self, cache):
        pages = [
            ReservationCardDialog,
            TodolistEditComponent,
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            ReservationPage,
            BasePage,
        ]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")
        full_name = cache.get("full_name_guest_function", "")

        with allure.step("Given 使用者進入「訂房明細」視窗"):
            ShareSteps.create_or_enter_reservation_detail(
                web, "quickSearch", full_name, "doOpenDtDetailDialog"
            )
            web.base_page.screenshot("Given 使用者進入「訂房明細」視窗")

        with allure.step("And 點擊右側表格「住客」頁籤中想修改的資料列的[黑色鉛筆]"):
            web.reservation_card_dialog.click_tab_toolbar("guest", "編輯")
            web.base_page.screenshot("And 點擊右側表格「住客」頁籤中想修改的資料列的[黑色鉛筆]")

        with allure.step("And 點擊「交辦」欄位的[勾勾]，進入「交辦事項編輯」視窗"):
            web.reservation_card_dialog.click_tab_guest_function("todoListButton").sleep(1)
            web.base_page.screenshot("And 點擊「交辦」欄位的[勾勾]，進入「交辦事項編輯」視窗")

        with allure.step("And 點擊上方表格中欲設定之資料列"):
            web.todolist_edit_component.click_todoitem()
            web.base_page.screenshot("And 點擊上方表格中欲設定之資料列")

        with allure.step("And 點擊左側的[已處理]"):
            web.base_page.click_toolbar_item("已處理").sleep(1)
            web.base_page.screenshot("And 點擊左側的[已處理]")

        with allure.step("Then 顯示'儲存成功'提示"):
            ShareSteps.verify_save_success_tip(web)
            web.share_panel_component.close_panel("交辦事項編輯").sleep(1)
            web.base_page.close_panel()

        with allure.step("And 驗證交辦事項內容"):
            web.reservation_card_dialog.click_card_toolbar("doOpenDtDetailDialog").sleep(1)
            web.reservation_card_dialog.click_tab_toolbar("guest", "編輯")
            web.reservation_card_dialog.click_tab_guest_function("todoListButton").sleep(1)
            web.base_page.screenshot("And 驗證交辦事項內容")
            info_list = [
                ("處理狀態", "proc_sta", "Y"),
                ("開始日期", "begin_dat", "2024/01/05"),
                ("結束日期", "end_dat", "2024/01/06"),
                ("處理部門", "dept_sna", "櫃台"),
                ("交辦內容", "todo_rmk", "Test"),
            ]
            for title, label, target in info_list:
                web.base_page.assert_data(
                    title, web.todolist_edit_component.get_todolist_info(label), target
                )

    @allure.story("編輯交辦事項狀態為未處理")
    @pytest.mark.xdist_group("test_guest_funcion")
    @pytest.mark.dependency(
        name="test_edit_todo_to_incompleted",
        depends=["test_edit_todo_to_completed"],
        scope="session",
    )
    def test_edit_todo_to_incompleted(self, cache):
        pages = [
            ReservationCardDialog,
            TodolistEditComponent,
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            ReservationPage,
            BasePage,
        ]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")
        full_name = cache.get("full_name_guest_function", "")

        with allure.step("Given 使用者進入「訂房明細」視窗"):
            ShareSteps.create_or_enter_reservation_detail(
                web, "quickSearch", full_name, "doOpenDtDetailDialog"
            )
            web.base_page.screenshot("Given 使用者進入「訂房明細」視窗")

        with allure.step("And 點擊右側表格「住客」頁籤中想修改的資料列的[黑色鉛筆]"):
            web.reservation_card_dialog.click_tab_toolbar("guest", "編輯")
            web.base_page.screenshot("And 點擊右側表格「住客」頁籤中想修改的資料列的[黑色鉛筆]")

        with allure.step("And 點擊「交辦」欄位的[勾勾]，進入「交辦事項編輯」視窗"):
            web.reservation_card_dialog.click_tab_guest_function("todoListButton").sleep(1)
            web.base_page.screenshot("And 點擊「交辦」欄位的[勾勾]，進入「交辦事項編輯」視窗")

        with allure.step("And 點擊上方表格中欲設定之資料列"):
            web.todolist_edit_component.click_todoitem()
            web.base_page.screenshot("And 點擊上方表格中欲設定之資料列")

        with allure.step("And 點擊左側的[未處理]"):
            web.base_page.click_toolbar_item("未處理").sleep(1)
            web.base_page.screenshot("And 點擊左側的[未處理]")

        with allure.step("Then 顯示'儲存成功'提示"):
            ShareSteps.verify_save_success_tip(web)
            web.share_panel_component.close_panel("交辦事項編輯").sleep(1)
            web.base_page.close_panel()

        with allure.step("And 驗證交辦事項內容"):
            web.reservation_card_dialog.click_card_toolbar("doOpenDtDetailDialog").sleep(1)
            web.reservation_card_dialog.click_tab_toolbar("guest", "編輯")
            web.reservation_card_dialog.click_tab_guest_function("todoListButton").sleep(1)
            web.base_page.screenshot("And 驗證交辦事項內容")
            info_list = [
                ("處理狀態", "proc_sta", "N"),
                ("開始日期", "begin_dat", "2024/01/05"),
                ("結束日期", "end_dat", "2024/01/06"),
                ("處理部門", "dept_sna", "櫃台"),
                ("交辦內容", "todo_rmk", "Test"),
            ]
            for title, label, target in info_list:
                web.base_page.assert_data(
                    title, web.todolist_edit_component.get_todolist_info(label), target
                )

    @allure.story("新增訂房提醒")
    @pytest.mark.xdist_group("test_guest_funcion_remind")
    @pytest.mark.dependency(name="test_add_reservation_alert", scope="session")
    def test_add_reservation_alert(self):
        pages = [
            ReservationCardDialog,
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            ReservationPage,
            BasePage,
        ]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")

        with allure.step("Given 使用者進入「訂房明細」視窗"):
            first_name = names.get_first_name()
            last_name = names.get_last_name()
            ShareSteps.create_or_enter_reservation_detail(
                web,
                "guestName",
                f"{first_name} {last_name}",
                "doOpenDtDetailDialog",
                first_name,
                last_name,
                "現場訂房含早",
                1,
            )
            web.base_page.screenshot("Given 使用者進入「訂房明細」視窗")

        with allure.step("And 點擊右側表格「住客」頁籤中想修改的資料列的[黑色鉛筆]"):
            web.reservation_card_dialog.click_tab_toolbar("guest", "編輯").sleep(1)
            web.base_page.screenshot("And 點擊右側表格「住客」頁籤中想修改的資料列的[黑色鉛筆]")

        with allure.step("And 點擊「提醒」欄位的[綠色加號]，進入「提醒事項」視窗"):
            web.reservation_card_dialog.click_tab_guest_function("reminderButton").sleep(1)
            web.base_page.screenshot("And 點擊「提醒」欄位的[綠色加號]，進入「提醒事項」視窗")

        with allure.step("And 在「訂房提醒」欄位輸入內容"):
            alert_content = "訂房提醒測試_" + RandomHelper.random_string(5)
            web.reservation_card_dialog.input_reservation_remind_by_field("訂房提醒", alert_content)
            web.base_page.screenshot("And 在「訂房提醒」欄位輸入內容")

        with allure.step("And 點擊儲存"):
            ShareSteps.click_btn_save(web)

        with allure.step("Then 顯示'儲存成功'提示"):
            ShareSteps.verify_save_success_tip(web)
            web.share_panel_component.close_panel("提醒事項").sleep(2)

        with allure.step("And 驗證訂房提醒正確"):
            web.reservation_card_dialog.click_tab_toolbar("guest", "編輯").sleep(1)
            web.reservation_card_dialog.click_tab_guest_function("reminderButton").sleep(1)
            web.base_page.screenshot("And 驗證訂房提醒正確")
            web.base_page.assert_data(
                "提醒內容",
                web.reservation_card_dialog.get_reservation_remind_by_field("訂房提醒"),
                alert_content,
            )
            web.share_panel_component.close_panel("提醒事項")

        with allure.step("And 驗證訂房提醒跳出正確"):
            web.base_page.close_panel().sleep(3)
            popup_alert_content = web.share_panel_component.get_remind_panel_content("訂房提醒")
            web.base_page.screenshot("And 驗證訂房提醒跳出正確")
            web.base_page.assert_data("彈窗提醒內容", popup_alert_content, alert_content)

    @allure.story("新增入住提醒")
    @pytest.mark.xdist_group("test_guest_funcion_remind")
    @pytest.mark.dependency(name="test_add_checkin_alert", scope="session")
    def test_add_checkin_alert(self, cache):
        pages = [
            ReservationCardDialog,
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            ReservationPage,
            BasePage,
        ]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")

        with allure.step("Given 使用者進入「訂房明細」視窗"):
            first_name = names.get_first_name()
            last_name = names.get_last_name()
            cache.set("full_name_remind", f"{first_name} {last_name}")
            ShareSteps.create_or_enter_reservation_detail(
                web,
                "guestName",
                f"{first_name} {last_name}",
                "doOpenDtDetailDialog",
                first_name,
                last_name,
                "現場訂房含早",
                1,
            )
            web.base_page.screenshot("Given 使用者進入「訂房明細」視窗")

        with allure.step("And 點擊右側表格「住客」頁籤中想修改的資料列的[黑色鉛筆]"):
            web.reservation_card_dialog.click_tab_toolbar("guest", "編輯").sleep(1)
            web.base_page.screenshot("And 點擊右側表格「住客」頁籤中想修改的資料列的[黑色鉛筆]")

        with allure.step("And 點擊「提醒」欄位的[綠色加號]，進入「提醒事項」視窗"):
            web.reservation_card_dialog.click_tab_guest_function("reminderButton").sleep(1)
            web.base_page.screenshot("And 點擊「提醒」欄位的[綠色加號]，進入「提醒事項」視窗")

        with allure.step("And 在「入住提醒」欄位輸入內容"):
            checkin_alert = "入住提醒測試_" + RandomHelper.random_string(5)
            cache.set("checkin_alert", checkin_alert)
            web.reservation_card_dialog.input_reservation_remind_by_field("入住提醒", checkin_alert)
            web.base_page.screenshot("And 在「入住提醒」欄位輸入內容")

        with allure.step("And 點擊儲存"):
            ShareSteps.click_btn_save(web)

        with allure.step("Then 顯示'儲存成功'提示"):
            ShareSteps.verify_save_success_tip(web)
            web.share_panel_component.close_panel("提醒事項").sleep(2)

        with allure.step("And 驗證入住提醒正確"):
            web.reservation_card_dialog.click_tab_toolbar("guest", "編輯").sleep(1)
            web.reservation_card_dialog.click_tab_guest_function("reminderButton").sleep(1)
            web.base_page.screenshot("And 驗證入住提醒正確")
            web.base_page.assert_data(
                "入住提醒內容",
                web.reservation_card_dialog.get_reservation_remind_by_field("入住提醒"),
                checkin_alert,
            )
            web.reservation_card_dialog.input_reservation_remind_by_field("入住提醒", "")
            web.base_page.click_toolbar_with_icon("save")

    @allure.story("新增其他提醒")
    @pytest.mark.xdist_group("test_guest_funcion_remind")
    @pytest.mark.dependency(
        name="test_add_other_alert", depends=["test_add_checkin_alert"], scope="session"
    )
    def test_add_other_alert(self, cache):
        pages = [
            ReservationCardDialog,
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            ReservationPage,
            BasePage,
        ]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")
        full_name = cache.get("full_name_remind", "")

        with allure.step("Given 使用者進入「訂房明細」視窗"):
            ShareSteps.create_or_enter_reservation_detail(
                web, "guestName", full_name, "doOpenDtDetailDialog"
            )
            web.base_page.screenshot("Given 使用者進入「訂房明細」視窗")

        with allure.step("And 點擊右側表格「住客」頁籤中想修改的資料列的[黑色鉛筆]"):
            web.reservation_card_dialog.click_tab_toolbar("guest", "編輯").sleep(1)
            web.base_page.screenshot("And 點擊右側表格「住客」頁籤中想修改的資料列的[黑色鉛筆]")

        with allure.step("And 點擊「提醒」欄位的[綠色加號]，進入「提醒事項」視窗"):
            web.reservation_card_dialog.click_tab_guest_function("reminderButton").sleep(1)
            web.base_page.screenshot("And 點擊「提醒」欄位的[綠色加號]，進入「提醒事項」視窗")

        with allure.step("And 在「其他提醒」欄位輸入內容"):
            other_alert = "其他提醒測試_" + RandomHelper.random_string(5)
            cache.set("other_alert", other_alert)
            web.reservation_card_dialog.input_reservation_remind_by_field("其他提醒", other_alert)
            web.base_page.screenshot("And 在「其他提醒」欄位輸入內容")

        with allure.step("And 點擊儲存"):
            ShareSteps.click_btn_save(web)

        with allure.step("Then 顯示'儲存成功'提示"):
            ShareSteps.verify_save_success_tip(web)
            web.share_panel_component.close_panel("提醒事項").sleep(2)

        with allure.step("And 驗證其他提醒正確"):
            web.reservation_card_dialog.click_tab_toolbar("guest", "編輯").sleep(1)
            web.reservation_card_dialog.click_tab_guest_function("reminderButton").sleep(1)
            web.base_page.screenshot("And 驗證其他提醒正確")
            web.base_page.assert_data(
                "其他提醒內容",
                web.reservation_card_dialog.get_reservation_remind_by_field("其他提醒"),
                other_alert,
            )

    @allure.story("新增退房提醒")
    @pytest.mark.xdist_group("test_guest_funcion_remind")
    @pytest.mark.dependency(
        name="test_add_checkout_alert", depends=["test_add_other_alert"], scope="session"
    )
    def test_add_checkout_alert(self, cache):
        pages = [
            ReservationCardDialog,
            TodolistEditComponent,
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            ReservationPage,
            BasePage,
        ]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")
        full_name = cache.get("full_name_remind", "")

        with allure.step("Given 使用者進入「訂房明細」視窗"):
            ShareSteps.create_or_enter_reservation_detail(
                web, "guestName", full_name, "doOpenDtDetailDialog"
            )
            web.base_page.screenshot("Given 使用者進入「訂房明細」視窗")

        with allure.step("And 點擊右側表格「住客」頁籤中想修改的資料列的[黑色鉛筆]"):
            web.reservation_card_dialog.click_tab_toolbar("guest", "編輯").sleep(1)
            web.base_page.screenshot("And 點擊右側表格「住客」頁籤中想修改的資料列的[黑色鉛筆]")

        with allure.step("And 點擊「提醒」欄位的[綠色加號]，進入「提醒事項」視窗"):
            web.reservation_card_dialog.click_tab_guest_function("reminderButton").sleep(1)
            web.base_page.screenshot("And 點擊「提醒」欄位的[綠色加號]，進入「提醒事項」視窗")

        with allure.step("And 在「退房提醒」欄位輸入內容"):
            checkout_alert = "退房提醒測試_" + RandomHelper.random_string(5)
            cache.set("checkout_alert", checkout_alert)
            web.reservation_card_dialog.input_reservation_remind_by_field(
                "退房提醒", checkout_alert
            )
            web.base_page.screenshot("And 在「退房提醒」欄位輸入內容")

        with allure.step("And 點擊儲存"):
            ShareSteps.click_btn_save(web)

        with allure.step("Then 顯示'儲存成功'提示"):
            ShareSteps.verify_save_success_tip(web)
            web.share_panel_component.close_panel("提醒事項").sleep(2)

        with allure.step("And 驗證退房提醒正確"):
            web.reservation_card_dialog.click_tab_toolbar("guest", "編輯").sleep(1)
            web.reservation_card_dialog.click_tab_guest_function("reminderButton").sleep(1)
            web.base_page.screenshot("And 驗證退房提醒正確")
            web.base_page.assert_data(
                "退房提醒內容",
                web.reservation_card_dialog.get_reservation_remind_by_field("退房提醒"),
                checkout_alert,
            )

    @allure.story("新增留言")
    @pytest.mark.xdist_group("test_guest_message")
    @pytest.mark.dependency(name="test_add_guest_message", scope="session")
    def test_add_guest_message(self, cache):
        pages = [
            ReservationCardDialog,
            MessageEditComponent,
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            ReservationPage,
            BasePage,
        ]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")

        with allure.step(
            "Given 使用者從「訂房」進入「訂房卡」頁面並進入「訂房明細」視窗，然後點擊住客的黑色鉛筆"
        ):
            first_name = names.get_first_name()
            last_name = names.get_last_name()
            cache.set("full_name_message", f"{first_name} {last_name}")
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
            web.base_page.screenshot("Given 使用者進入「訂房明細」視窗")

        with allure.step("And 點擊右側表格「住客」頁籤中想修改的資料列的[黑色鉛筆]"):
            web.reservation_card_dialog.click_tab_toolbar("guest", "編輯").sleep(1)
            web.base_page.screenshot("And 點擊右側表格「住客」頁籤中想修改的資料列的[黑色鉛筆]")

        with allure.step("And 點擊「留言」欄位的[綠色加號]，進入「留言編輯」視窗"):
            web.reservation_card_dialog.click_tab_guest_function("messageButton").sleep(1)
            web.base_page.screenshot("And 點擊「留言」欄位的[綠色加號]，進入「留言編輯」視窗")

        with allure.step("And 點擊下拉選單選擇或者輸入必填內容"):
            message_from = f"{names.get_first_name()} {names.get_last_name()}"
            phone_number = RandomHelper.generate_phone_mobile()
            message_content = "留言測試_" + RandomHelper.random_string(10)

            cache.set("guest_message_from", message_from)
            cache.set("guest_phone_number", phone_number)
            cache.set("guest_message_content", message_content)

            web.message_edit_component.fill_message_fields(
                message_from, phone_number, message_content
            )
            web.base_page.screenshot("And 點擊下拉選單選擇或者輸入必填內容")

        with allure.step("And 點擊右上的[橘色磁碟片]儲存"):
            ShareSteps.click_btn_save(web)

        with allure.step("Then 顯示'新增成功'訊息"):
            ShareSteps.verify_save_success_tip(web, "新增成功")
            initial_values = {
                "guest_name": web.message_edit_component.get_message_field_value("住客姓名"),
                "guest_status": web.message_edit_component.get_message_field_value("住客狀態"),
                "card_no": web.message_edit_component.get_message_field_value("訂房卡號"),
                "message_no": web.message_edit_component.get_message_field_value("留言編號"),
                "message_time": web.message_edit_component.get_message_field_value("留言時間"),
                "create_date": web.message_edit_component.get_message_field_value("新增日"),
                "modify_date": web.message_edit_component.get_message_field_value("修改日"),
            }

            web.share_panel_component.close_panel("留言編輯")
            web.reservation_card_dialog.click_detail_toolbar("save").sleep(1)
            web.tip_component.click_ok()

        with allure.step("And 驗證留言編輯視窗的所有欄位"):
            web.reservation_card_dialog.click_tab_toolbar("guest", "編輯")
            web.reservation_card_dialog.click_tab_guest_function("messageButton").sleep(1)
            web.message_edit_component.click_message_grid_last_row().sleep(1)
            web.base_page.screenshot("And 驗證留言編輯視窗的所有欄位")

            field_validations = [
                ("住客姓名", initial_values["guest_name"]),
                ("住客狀態", initial_values["guest_status"]),
                ("訂房卡號", initial_values["card_no"]),
                ("入住日期", "2024/01/05"),
                ("退房日期", "2024/01/06"),
                ("留言編號", initial_values["message_no"]),
                ("留言狀態", "N : 新留言"),
                ("留言日期", datetime.now().strftime("%Y/%m/%d")),
                ("留言時間", initial_values["message_time"]),
                ("留言者", message_from),
                ("連絡電話", phone_number),
                ("留言內容", message_content),
                ("新增日", initial_values["create_date"]),
                ("新增者", "autotest"),
                ("修改日", initial_values["modify_date"]),
                ("修改者", "autotest"),
            ]

            for title, expected in field_validations:
                web.base_page.assert_data(
                    title, web.message_edit_component.get_message_field_value(title), expected
                )

        with allure.step("And 驗證留言表格資料正確"):
            web.base_page.screenshot("And 驗證留言表格資料正確")
            for title, col, expected in [
                ("留言狀態", "1", "N : 新留言"),
                ("留言日期", "2", datetime.now().strftime("%Y/%m/%d")),
                ("留言時間", "3", initial_values["message_time"]),
                ("入住日期", "5", "2024/01/05"),
                ("退房日期", "6", "2024/01/06"),
                ("住客狀態", "7", initial_values["guest_status"]),
            ]:
                web.base_page.assert_data(
                    title, web.message_edit_component.get_message_grid_cell_text(col), expected
                )

    @allure.story("留言更改狀態為已告知")
    @pytest.mark.xdist_group("test_guest_message")
    @pytest.mark.dependency(
        name="test_edit_guest_message_informed", depends=["test_add_guest_message"], scope="session"
    )
    def test_edit_guest_message_informed(self, cache):
        pages = [
            ReservationCardDialog,
            MessageEditComponent,
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            ReservationPage,
            BasePage,
        ]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")
        full_name = cache.get("full_name_message", "")

        with allure.step(
            "Given 使用者從「訂房」進入「訂房卡」頁面並進入「訂房明細」視窗，然後點擊住客的黑色鉛筆"
        ):
            ShareSteps.create_or_enter_reservation_detail(
                web, "guestName", full_name, "doOpenDtDetailDialog"
            )
            web.base_page.screenshot("Given 使用者進入「訂房明細」視窗")

        with allure.step("And 點擊右側表格「住客」頁籤中想修改的資料列的[黑色鉛筆]"):
            web.reservation_card_dialog.click_tab_toolbar("guest", "編輯").sleep(1)
            web.base_page.screenshot("And 點擊右側表格「住客」頁籤中想修改的資料列的[黑色鉛筆]")

        with allure.step("And 點擊「留言」欄位的[綠色加號]，進入「留言編輯」視窗"):
            web.reservation_card_dialog.click_tab_guest_function("messageButton").sleep(1)
            web.base_page.screenshot("And 點擊「留言」欄位的[綠色加號]，進入「留言編輯」視窗")

        with allure.step("And 點擊上方表格中的留言紀錄"):
            web.message_edit_component.click_message_grid_last_row().sleep(1)
            web.base_page.screenshot("And 點擊上方表格中的留言紀錄")

        with allure.step("And 點擊左側[已告知]"):
            web.base_page.click_toolbar_item_2("已告知").sleep(1)
            initial_values = {
                "inform_time": web.message_edit_component.get_message_field_value("告知時間"),
                "guest_name": web.message_edit_component.get_message_field_value("住客姓名"),
                "guest_status": web.message_edit_component.get_message_field_value("住客狀態"),
                "card_no": web.message_edit_component.get_message_field_value("訂房卡號"),
                "message_no": web.message_edit_component.get_message_field_value("留言編號"),
                "message_time": web.message_edit_component.get_message_field_value("留言時間"),
                "create_date": web.message_edit_component.get_message_field_value("新增日"),
                "modify_date": web.message_edit_component.get_message_field_value("修改日"),
            }
            web.base_page.screenshot("And 點擊左側[已告知]")
            web.share_panel_component.close_panel("留言編輯")
            web.reservation_card_dialog.click_detail_toolbar("save").sleep(1)
            web.tip_component.click_ok()

        with allure.step("And 驗證留言編輯視窗的所有欄位"):
            web.reservation_card_dialog.click_tab_toolbar("guest", "編輯")
            web.reservation_card_dialog.click_tab_guest_function("messageButton").sleep(1)
            web.message_edit_component.click_message_grid_last_row().sleep(1)
            web.base_page.screenshot("And 驗證留言編輯視窗的所有欄位")

            field_validations = [
                ("住客姓名", initial_values["guest_name"]),
                ("住客狀態", initial_values["guest_status"]),
                ("訂房卡號", initial_values["card_no"]),
                ("入住日期", "2024/01/05"),
                ("退房日期", "2024/01/06"),
                ("留言編號", initial_values["message_no"]),
                ("留言狀態", "Y : 已告知"),
                ("告知時間", initial_values["inform_time"]),
                ("留言日期", datetime.now().strftime("%Y/%m/%d")),
                ("留言時間", initial_values["message_time"]),
                ("留言者", cache.get("guest_message_from", "")),
                ("連絡電話", cache.get("guest_phone_number", "")),
                ("留言內容", cache.get("guest_message_content", "")),
                ("新增日", initial_values["create_date"]),
                ("新增者", "autotest"),
                ("修改日", initial_values["modify_date"]),
                ("修改者", "autotest"),
            ]

            for title, expected in field_validations:
                web.base_page.assert_data(
                    title, web.message_edit_component.get_message_field_value(title), expected
                )

            web.base_page.assert_data(
                "留言者不可編輯",
                web.message_edit_component.message_field_is_enabled("留言者"),
                "true",
            )
            web.base_page.assert_data(
                "連絡電話不可編輯",
                web.message_edit_component.message_field_is_enabled("連絡電話"),
                "true",
            )
            web.base_page.assert_data(
                "留言內容不可編輯",
                web.message_edit_component.message_textarea_field_is_enabled(),
                "true",
            )

        with allure.step("And 驗證留言表格資料正確"):
            web.base_page.screenshot("And 驗證留言表格資料正確")
            for title, col, expected in [
                ("留言狀態", "1", "Y : 已告知"),
                ("留言日期", "2", datetime.now().strftime("%Y/%m/%d")),
                ("留言時間", "3", initial_values["message_time"]),
                ("入住日期", "5", "2024/01/05"),
                ("退房日期", "6", "2024/01/06"),
                ("住客狀態", "7", initial_values["guest_status"]),
            ]:
                web.base_page.assert_data(
                    title, web.message_edit_component.get_message_grid_cell_text(col), expected
                )

    @allure.story("住客明細-No Info")
    @pytest.mark.xdist_group("test_guest_detail")
    @pytest.mark.dependency(name="test_guest_detail_no_info", scope="session")
    def test_guest_detail_no_info(self, cache):
        pages = [
            ReservationCardDialog,
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            ReservationPage,
            BasePage,
        ]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")

        with allure.step("Given 使用者從「訂房」進入「訂房卡」頁面"):
            first_name = names.get_first_name()
            last_name = names.get_last_name()
            cache.set("full_name_no_info", f"{first_name} {last_name}")
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
            web.base_page.screenshot("Given 使用者進入「訂房明細」視窗")

        with allure.step("And 點擊右側表格「住客」頁籤中想修改的資料列的[黑色鉛筆]"):
            web.reservation_card_dialog.click_tab_toolbar("guest", "編輯").sleep(1)
            web.base_page.screenshot("And 點擊右側表格「住客」頁籤中想修改的資料列的[黑色鉛筆]")

        with allure.step("And 點擊「No info」欄位選擇'是'"):
            web.reservation_card_dialog.click_tab_guest_function("noInfo")
            web.reservation_card_dialog.select_guest_no_info("是")
            web.base_page.screenshot("And 點擊「No info」欄位選擇'是'")

        with allure.step("And 點擊左側「黑色磁碟片」或頁面空白處"):
            web.reservation_card_dialog.click_tab_toolbar("guest", "儲存")
            web.base_page.screenshot("And 點擊左側「黑色磁碟片」或頁面空白處")

        with allure.step("Then 住客名字顯示紅色背景"):
            web.reservation_card_dialog.click_detail_toolbar("save").sleep(1)
            web.tip_component.click_ok()
            web.base_page.close_panel()
            web.reservation_card_dialog.click_card_toolbar("doOpenDtDetailDialog").sleep(1)
            web.base_page.screenshot("Then 住客名字顯示紅色背景")
            web.base_page.assert_data(
                "住客名稱的背景為紅色", web.reservation_card_dialog.is_guest_name_red(), True
            )

    @allure.story("住客明細 - 費用明細")
    def test_expense_detail(self):
        pages = [
            ReservationCardDialog,
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            ReservationPage,
            BasePage,
        ]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")

        with allure.step("Given 使用者從「訂房」進入「訂房卡」頁面並進入「訂房明細」視窗"):
            first_name = names.get_first_name()
            last_name = names.get_last_name()
            full_name = f"{first_name} {last_name}"
            ShareSteps.create_or_enter_reservation_detail(
                web,
                "guestName",
                full_name,
                "doOpenDtDetailDialog",
                first_name,
                last_name,
                "現場訂房含早",
                1,
            )
            web.reservation_card_dialog.click_tab_toolbar("guest", "編輯")
            web.base_page.screenshot("Given 使用者進入「訂房明細」視窗")

        with allure.step("When 點擊右側表格「費用明細」頁籤"):
            web.reservation_card_dialog.click_tab("expenseDetail").sleep(1)
            web.base_page.screenshot("When 點擊右側表格「費用明細」頁籤")

        with allure.step("And 點擊房租項目打開房租細項視窗"):
            web.reservation_card_dialog.click_tab_expense_rent().sleep(1)
            web.base_page.screenshot("And 點擊房租項目打開房租細項視窗")

        with allure.step("Then 驗證房租細項各欄位資料正確性"):
            web.base_page.screenshot("Then 驗證房租細項各欄位資料正確性")
            today = datetime.now().strftime("%Y-%m-%d")
            web.base_page.assert_data(
                "第一列資料",
                web.reservation_card_dialog.get_expense_detail_data(1),
                ["2024-01-05", "房租", "7,400", "1", "7,400", "2024-01-05", "autotest", today],
            )
            web.base_page.assert_data(
                "第二列資料",
                web.reservation_card_dialog.get_expense_detail_data(2),
                ["2024-01-05", "早餐拆帳大人", "250", "2", "500", "2024-01-06", "autotest", today],
            )
