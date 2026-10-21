import allure
import names
import pytest
from pages.base_page import BasePage
from pages.checkin_page import CheckinPage
from pages.components.header_component import HeaderComponent
from pages.components.share_panel_component import SharePanelComponent
from pages.components.tip_component import TipComponent
from pages.dialogs.reservation_card_dialog import ReservationCardDialog
from pages.guest_account_page import GuestAccountPage
from pages.home_page import HomePage
from pages.housekeeping_account_page import HousekeepingAccountPage
from pages.login_page import LoginPage
from pages.reservation_page import ReservationPage
from tests.share_steps import ShareSteps
from tools.driver_helper import DriverHelper
from tools.random_helper import RandomHelper


@allure.feature("訂房")
class TestReservation:

    @allure.story("依房號訂房")
    @pytest.mark.xdist_group("roomno_reservation")
    @pytest.mark.dependency(name="test_roomno_reservation", scope="session")
    def test_roomno_reservation(self, logged_in_driver, cache):
        pages = [BasePage, LoginPage, HomePage, HeaderComponent, TipComponent, ReservationPage]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")
        with allure.step("選擇空房"):
            web.header_component.expand_menu("訂房").sleep(1)
            web.header_component.to_func_page("依房號訂房").sleep(10)
            web.reservation_page.select("房型", "STD : 標準客房")
            web.reservation_page.select("樓層", "5 : 5")
            web.reservation_page.search().sleep(1)
            web.reservation_page.click_empty_room()
            web.reservation_page.click_empty_room()
            room_no = web.reservation_page.get_selected_room_no()
            cache.set("room_no", room_no)
            web.reservation_page.screenshot("選擇空房")
        with allure.step("建立訂房卡"):
            web.reservation_page.click_reservation().sleep(3)
            web.reservation_page.click_edit_guest().sleep(3)
            last_name = names.get_last_name()
            first_name = names.get_first_name()
            web.reservation_page.create_guest(
                first_name, last_name, "Miss.", RandomHelper.generate_phone_mobile()
            )
            web.tip_component.click_ok().sleep(1)
            web.reservation_page.save_card()
            web.tip_component.click_ok().sleep(2)
            web.reservation_page.screenshot("建立訂房卡")
        with allure.step("驗證訂房明細"):
            web.reservation_page.to_detail_tab().sleep(2)
            web.reservation_page.screenshot("驗證訂房明細")
            full_name = f"{first_name} {last_name}"
            cache.set("full_name", full_name)
            cache.set("dialog_ikey", web.reservation_page.get_dialog_ikey().split(":")[1].strip())
            web.reservation_page.assert_data(
                "訂房公司", web.base_page.get_dropdown_input_value("acustCode"), "一般散客"
            )
            web.reservation_page.assert_data(
                "稱謂", web.reservation_page.get_salute_code(), "Miss."
            )
            web.reservation_page.assert_data(
                "姓名", web.reservation_page.get_guest_info("guestName"), full_name
            )
            web.reservation_page.assert_data(
                "入住日期",
                web.reservation_page.get_guest_info("ciDate").split(" ")[0],
                "2024/01/05",
            )
            web.reservation_page.assert_data(
                "退房日期",
                web.reservation_page.get_guest_info("coDate").split(" ")[0],
                "2024/01/06",
            )
            web.reservation_page.assert_data(
                "房價代碼", web.reservation_page.get_guest_info("rateCode"), "現場訂房含早"
            )
            web.reservation_page.assert_data(
                "使用房型", web.reservation_page.get_guest_info("useCode"), "STD: 標準客房1"
            )
            web.reservation_page.assert_data(
                "計價房型", web.reservation_page.get_guest_info("roomCode"), "STD: 標準客房1"
            )
            web.reservation_page.assert_data(
                "單價", web.reservation_page.get_guest_info("rentAmount"), "7,900"
            )
            web.reservation_page.assert_data(
                "房號", web.reservation_page.get_guest_info("roomNos"), room_no
            )
            web.reservation_page.sleep(4)

    @allure.story("新增客房預收款")
    @pytest.mark.xdist_group("roomno_reservation")
    @pytest.mark.dependency(
        name="test_add_deposit", depends=["test_roomno_reservation"], scope="session"
    )
    def test_add_deposit(self, logged_in_driver, cache):
        pages = [HeaderComponent, TipComponent, SharePanelComponent, GuestAccountPage, CheckinPage]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        dialog_ikey = cache.get("dialog_ikey", "")
        room_no = cache.get("room_no", "")
        full_name = cache.get("full_name", "")
        with allure.step("確認入住資料"):
            web.header_component.expand_menu("接待").sleep(1)
            web.header_component.to_func_page("C/I清單")
            web.checkin_page.click_target_ikey_2(dialog_ikey)
            web.checkin_page.click_toolbar_item_2("入住").sleep(3)
            web.checkin_page.click_dialog_checkin()
            web.tip_component.click_ok().sleep(3)
            web.checkin_page.screenshot("確認入住資料")
            web.share_panel_component.close_panel("製卡")
            web.share_panel_component.close_panel("check In")

        with allure.step("建立客房預收款"):
            web.header_component.expand_menu("出納").sleep(2)
            web.header_component.to_func_page("住客帳維護").sleep(2)
            web.guest_account_page.set_condition_value("房號", room_no)
            web.guest_account_page.search().sleep(2)
            web.guest_account_page.click_target_ikey(dialog_ikey)
            web.guest_account_page.click_guest_maintain().sleep(3)
            ShareSteps.open_shift(web, "FO : 飯店櫃檯", "a", "autotest")
            web.guest_account_page.click_credit().sleep(3)
            web.guest_account_page.select_consumption_code("9999 : 客房預收款").sleep(2)
            web.guest_account_page.set_amount("7900")

            web.share_panel_component.click_panel_save("入帳").sleep(4)
            web.share_panel_component.select_by_panel("請輸入預收款方式", "32:MASTER信用卡").sleep(
                2
            )
            web.share_panel_component.input_by_label("信用卡卡號", "5555111122223333").sleep(2)
            web.share_panel_component.click_panel_save("請輸入預收款方式").sleep(5)
            web.guest_account_page.screenshot("建立客房預收款")
            web.share_panel_component.close_panel("入帳").sleep(3)

        with allure.step("驗證客房預收款"):
            web.guest_account_page.screenshot("驗證客房預收款")
            web.guest_account_page.assert_data(
                "住客姓名", web.guest_account_page.get_guest_maintain_info("姓名"), full_name
            )
            web.guest_account_page.assert_data(
                "訂房公司", web.guest_account_page.get_guest_maintain_info("訂房公司"), "一般散客"
            )
            web.guest_account_page.assert_data(
                "小記", web.guest_account_page.get_deposit_info("item_tot"), "-7,900"
            )
            web.guest_account_page.assert_data(
                "帳單備註",
                web.guest_account_page.get_deposit_info("remark4"),
                f"MASTER信用卡 {room_no}-1",
            )
            web.guest_account_page.assert_data(
                "消費項目", web.guest_account_page.get_deposit_info("item_nam"), "9999:客房預收款"
            )

    @allure.story("新增房務帳作業")
    @pytest.mark.xdist_group("roomno_reservation")
    @pytest.mark.dependency(
        name="test_new_housekeeping_account", depends=["test_add_deposit"], scope="session"
    )
    def test_new_housekeeping_account(self, logged_in_driver, cache):
        pages = [
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            HousekeepingAccountPage,
            GuestAccountPage,
        ]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        dialog_ikey = cache.get("dialog_ikey", "")
        room_no = cache.get("room_no", "")

        with allure.step("新增房務帳資料"):
            web.header_component.expand_menu("房務").sleep(2)
            web.header_component.to_func_page("房務帳作業").sleep(5)
            web.housekeeping_account_page.add_housekeeping_account()

            web.housekeeping_account_page.select_class("FO", "a")
            web.housekeeping_account_page.select_room_nos(room_no)
            web.housekeeping_account_page.add_housekeeping("H001", "L01")
            web.housekeeping_account_page.add_housekeeping("H002", "M001")
            web.housekeeping_account_page.save_housekeeping_setting()
            web.tip_component.click_ok().sleep(2)
            web.housekeeping_account_page.close_housekeeping_setting().sleep(2)
            web.housekeeping_account_page.screenshot("新增房務帳資料")

        with allure.step("驗證房務帳資料"):
            web.header_component.expand_menu("出納").sleep(2)
            web.header_component.to_func_page("住客帳維護")
            web.guest_account_page.set_condition_value("房號", room_no)
            web.guest_account_page.search().sleep(2)
            web.guest_account_page.click_target_ikey(dialog_ikey)
            web.guest_account_page.click_guest_maintain().sleep(5)
            ShareSteps.open_shift(web, "FO : 飯店櫃檯", "a", "autotest")
            web.guest_account_page.click_item_detail().sleep(3)
            web.guest_account_page.screenshot("驗證房務帳資料")
            web.guest_account_page.assert_data(
                "廳別", web.guest_account_page.get_input_values("rsptCode"), "FO:飯店櫃檯"
            )
            web.guest_account_page.assert_data(
                "班別", web.guest_account_page.get_input_value("shiftCode"), "a"
            )
            web.guest_account_page.assert_data(
                "房號", web.guest_account_page.get_input_value("roomNos"), room_no
            )
            web.guest_account_page.assert_data(
                "小分類代號_1",
                web.guest_account_page.get_row_item("1", "smallType"),
                "H001: Laundry",
            )
            web.guest_account_page.assert_data(
                "消費代號_1",
                web.guest_account_page.get_row_item("1", "productNos"),
                "L01: 洗衣-襯衫",
            )
            web.guest_account_page.assert_data(
                "小分類代號_2",
                web.guest_account_page.get_row_item("2", "smallType"),
                "H002: Mini Bar",
            )
            web.guest_account_page.assert_data(
                "消費代號_2", web.guest_account_page.get_row_item("2", "productNos"), "M001: 可樂"
            )

    @allure.story("預估款維護-轉至住客帳")
    @pytest.mark.xdist_group("roomno_reservation")
    @pytest.mark.dependency(
        name="test_transfer_to_guest_account",
        depends=["test_new_housekeeping_account"],
        scope="session",
    )
    def test_transfer_to_guest_account(self, logged_in_driver, cache):
        pages = [
            HeaderComponent,
            GuestAccountPage,
            HousekeepingAccountPage,
            SharePanelComponent,
            TipComponent,
        ]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        dialog_ikey = cache.get("dialog_ikey", "")
        room_no = cache.get("room_no", "")

        with allure.step("開啟預估款維護"):
            web.header_component.expand_menu("出納").sleep(2)
            web.header_component.to_func_page("住客帳維護")
            web.guest_account_page.set_condition_value("房號", room_no)
            web.guest_account_page.search().sleep(2)
            web.guest_account_page.click_target_ikey(dialog_ikey)
            web.guest_account_page.click_guest_maintain().sleep(3)
            ShareSteps.open_shift(web, "FO : 飯店櫃檯", "a", "autotest")
            web.guest_account_page.click_toolbar_item("預估款維護").sleep(2)
            web.guest_account_page.screenshot("開啟預估款維護")

        with allure.step("轉至住客帳"):
            web.guest_account_page.click_toolbar_item("轉至住客帳")
            web.tip_component.click_btn_by_text("當天")
            web.tip_component.click_ok().sleep(2)
            web.share_panel_component.close_panel("預估款維護").sleep(2)
            web.share_panel_component.click_toolbar_item("結帳").sleep(2)
            web.tip_component.click_btn_by_text("確定").sleep(2)
            web.tip_component.click_ok()
            web.guest_account_page.add_pay_type()
            web.share_panel_component.select_by_panel("請輸入付款方式", "10:現  金")
            web.share_panel_component.click_panel_save("請輸入付款方式")
            web.share_panel_component.input_by_label("統一編號", "23598233")
            web.share_panel_component.screenshot("結帳輸入統編")
            web.share_panel_component.click_toolbar_item(panel="結帳", item="結帳").sleep(2)
            web.share_panel_component.click_panel_footer_btn("發票載具", "確定").sleep(2)
            web.tip_component.click_ok().sleep(2)
            web.share_panel_component.click_toolbar_item(panel="列印帳單", item="列印").sleep(2)
            web.tip_component.click_ok().sleep(2)
            web.share_panel_component.close_panel("列印帳單").sleep(2)
            web.tip_component.click_btn_by_text("確定").sleep(2)
            web.tip_component.click_ok().sleep(2)
            web.share_panel_component.screenshot("轉至住客帳完成")

        with allure.step("驗證已結帳內容"):
            web.guest_account_page.click_checkout_more().sleep(2)
            web.guest_account_page.screenshot("驗證已結帳內容")
            pay_types = web.guest_account_page.get_table_column_values("付款方式名稱")
            pay_totals = web.guest_account_page.get_table_column_values("付款金額")
            web.guest_account_page.assert_data_in_list("付款方式名稱1", pay_types, "10: 現 金")
            web.guest_account_page.assert_data_in_list("付款金額1", pay_totals, "286")
            web.guest_account_page.assert_data_in_list(
                "付款方式名稱2", pay_types, "A0: 沖客房預收款"
            )
            web.guest_account_page.assert_data_in_list("付款金額2", pay_totals, "7,900")

        with allure.step("驗證發票統一編號"):
            web.guest_account_page.click_toolbar_item(panel="已結帳", item="發票明細").sleep(2)
            web.guest_account_page.screenshot("驗證發票統一編號")
            web.guest_account_page.assert_data(
                "統一編號", web.guest_account_page.get_uni_cod(), "23598233"
            )

    @allure.story("依房型訂房")
    def test_roomtype_reservation(self, logged_in_driver, cache):
        pages = [BasePage, HeaderComponent, TipComponent, SharePanelComponent, ReservationPage]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")
        with allure.step("選擇房型"):
            web.header_component.expand_menu("訂房").sleep(1)
            web.header_component.to_func_page("依房型訂房")
            web.reservation_page.select_room_type_pointer("STD")
            web.reservation_page.select_room_type_pointer("STD")
            web.reservation_page.screenshot("選擇房型")
            web.reservation_page.click_reservation_by_room_type().sleep(3)
            first_name = names.get_first_name()
            last_name = names.get_last_name()
            web.reservation_page.click_edit_guest().sleep(3)
            web.reservation_page.create_guest(
                first_name, last_name, "Miss.", RandomHelper.generate_phone_mobile()
            )
            web.tip_component.click_ok().sleep(3)

        with allure.step("更改退房日期"):
            web.reservation_page.change_co_date("2024/01/09").sleep(2)
            web.reservation_page.screenshot("更改退房日期")
            total = web.reservation_page.get_rent_total_detail()
            web.reservation_page.screenshot("房租明細")
            web.reservation_page.close_panel_by_title("浮動房價")
            web.reservation_page.assert_data("總金額", web.reservation_page.get_rent_total(), total)
            web.reservation_page.save_card()
            web.tip_component.click_ok().sleep(1)

        with allure.step("建立訂房卡後，可查詢到訂房資料"):
            panel_title = web.reservation_page.get_dialog_ikey()
            web.base_page.sleep(2)
            web.reservation_page.close_panel_by_title(panel_title)
            dialog_ikey = panel_title.split(":")[1].strip()
            cache.set("dialog_ikey", dialog_ikey)

            web.header_component.expand_menu("接待").sleep(1)
            web.header_component.to_func_page("住客查詢")
            web.reservation_page.expand_search_condition().sleep(1)
            web.reservation_page.select("過濾條件", "A : Arrival")
            web.reservation_page.set_condition_value("訂房卡號", dialog_ikey)
            web.reservation_page.search().sleep(1)

            assert web.reservation_page.has_target_ikey(dialog_ikey)
            web.reservation_page.screenshot("建立訂房卡後，可查詢到訂房資料")

    @allure.story("依房型訂房-有訂房公司")
    @pytest.mark.parametrize("month, day", [("1月", "6"), ("1月", "12"), ("2月", "4")])
    def test_roomtype_reservation_with_contract(self, month, day):
        pages = [
            BasePage,
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            ReservationPage,
            ReservationCardDialog,
        ]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        with allure.step("Given 進入依房型訂房並選擇房型"):
            web.header_component.expand_menu("訂房").sleep(1)
            web.header_component.to_func_page("依房型訂房")
            web.reservation_page.select_room_type_pointer("STD")
            web.reservation_page.select_room_type_pointer("STD")
            web.reservation_page.screenshot("Given 進入依房型訂房並選擇房型")

        with allure.step("When 點擊訂房並建立住客歷史"):
            web.reservation_page.click_reservation_by_room_type().sleep(3)
            first_name = names.get_first_name()
            last_name = names.get_last_name()
            mobile = RandomHelper.generate_phone_mobile()

            web.reservation_page.click_edit_guest().sleep(3)
            web.reservation_page.create_guest(first_name, last_name, "Miss.", mobile)
            web.tip_component.click_ok().sleep(3)
            web.reservation_page.screenshot("When 點擊訂房並建立住客歷史")

        with allure.step("And 更改退房日期"):
            web.base_page.click_date_icon("coDate")
            web.base_page.select_date("2024年", month, day)
            web.reservation_page.screenshot("And 更改退房日期")

        with allure.step("And 選擇商務公司"):
            web.base_page.click_by_data_field("acustCode").sleep(1)
            web.base_page.set_dropdown_filter("測測").sleep(1)
            web.reservation_page.select_company("測測BB22").sleep(1)
            web.reservation_page.screenshot("And 選擇商務公司")

        with allure.step("And 選擇淺橘色底的合約價"):
            web.reservation_page.click_btn_edit().sleep(1)
            web.reservation_card_dialog.set_rate_code_by_search_name("comcon3", 1).sleep(1)
            web.reservation_page.screenshot("And 選擇淺橘色底的合約價")
            total = web.reservation_page.get_rent_total_detail()
            web.reservation_page.screenshot("房租明細")
            web.reservation_page.close_panel_by_title("浮動房價")
            web.reservation_page.assert_data("總金額", web.reservation_page.get_rent_total(), total)

        with allure.step("And 點擊橘色磁碟片儲存"):
            web.reservation_page.save_card().sleep(2)
            web.reservation_page.screenshot("And 點擊橘色磁碟片儲存")

        with allure.step("Then 驗證儲存成功提示"):
            ShareSteps.verify_save_success_tip(web)

        with allure.step("And 住客查詢功能查詢驗證"):
            panel_title = web.reservation_page.get_dialog_ikey()
            web.reservation_page.close_panel_by_title(panel_title).sleep(2)
            dialog_ikey = panel_title.split(":")[1].strip()

            web.header_component.expand_menu("接待").sleep(1)
            web.header_component.to_func_page("住客查詢")
            web.reservation_page.expand_search_condition().sleep(1)
            web.reservation_page.select("過濾條件", "A : Arrival")
            web.reservation_page.set_condition_value("訂房卡號", dialog_ikey)
            web.reservation_page.search().sleep(1)
            web.reservation_page.screenshot("And 住客查詢功能查詢驗證")

            web.base_page.assert_data(
                "訂房卡存在", web.reservation_page.has_target_ikey(dialog_ikey), True
            )
            web.base_page.assert_data(
                "訂房公司", web.base_page.get_field_text("acust_nam"), "測測BB22"
            )
