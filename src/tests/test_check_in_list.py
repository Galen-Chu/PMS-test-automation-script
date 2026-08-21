import allure
import pytest
from pages.base_page import BasePage
from pages.check_in_list_page import CheckInListPage
from pages.components.header_component import HeaderComponent
from pages.components.tip_component import TipComponent
from tools.driver_helper import DriverHelper
from tools.test_data_helper import get_group_data


@allure.feature("接待作業 - C/I清單")
class TestCheckInList:

    @allure.story("C/I 清單 - 單筆入住")
    @pytest.mark.xdist_group("test_ci_list_flow_a")
    @pytest.mark.dependency(name="test_single_check_in", scope="session")
    def test_single_check_in(self):
        data = get_group_data("test_ci_list_flow_a")
        room = data["room"]

        pages = [CheckInListPage, HeaderComponent, TipComponent, BasePage]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")

        with allure.step("Given 使用者進入「C/I清單」頁面"):
            web.header_component.expand_menu("接待").sleep(1)
            web.header_component.to_func_page("C/I清單").sleep(1)
            web.base_page.screenshot("Given 使用者進入「C/I清單」頁面")

        with allure.step("Given 復原：若目標房間已入住則取消入住"):
            # 展開篩選欄位，切到「全部」搜尋目標房間
            web.check_in_list_page.expand_filter().sleep(0.5)
            web.check_in_list_page.select_checkin_status("all:全部").sleep(0.5)
            web.check_in_list_page.search_room(room).sleep(1)

            # 偵測是否已入住
            status = web.check_in_list_page.get_order_status(room)
            if "I" in status:
                # 選取 → 取消入住
                web.check_in_list_page.click_room_row(room).sleep(0.5)
                web.check_in_list_page.click_cancel_check_in()
                web.check_in_list_page.sleep(1)
                web.check_in_list_page.cancel_check_in().sleep(1)
                # Alert「住客取消入住成功」
                web.tip_component.click_ok().sleep(0.5)
                # 關閉 Dialog
                web.check_in_list_page.close_check_in_dialog().sleep(0.5)

            # 切回「N:未入住」篩選
            web.check_in_list_page.select_checkin_status("N:未入住").sleep(0.5)
            web.check_in_list_page.search_room(room).sleep(1)
            web.base_page.screenshot("Given 復原完成")

        with allure.step("When 從C/I Table點擊欲進行入住之資料列"):
            web.check_in_list_page.click_room_row(room).sleep(0.5)
            web.base_page.screenshot("When 從C/I Table點擊欲進行入住之資料列")

        with allure.step("And 點擊「入住」"):
            web.check_in_list_page.click_check_in().sleep(1)
            web.base_page.screenshot("And 點擊「入住」")

        with allure.step("And 確認check in視窗未入住頁簽已勾選資料"):
            assert (
                web.check_in_list_page.verify_checkbox_checked()
            ), "NotCiPanel checkbox 未自動勾選"
            web.base_page.screenshot("And 確認check in視窗未入住頁簽已勾選資料")

        with allure.step("And 點擊「入住」執行入住"):
            web.check_in_list_page.click_do_check_in().sleep(2)
            web.base_page.screenshot("And 點擊「入住」執行入住")

        with allure.step("Then 顯示「住客入住成功」提示"):
            web.base_page.wait_visible(web.tip_component.locator.btn_alert_ok)
            tip_text = web.tip_component.get_tip_text()
            web.base_page.assert_data("入住提示", tip_text, "住客入住成功")
            web.tip_component.click_ok().sleep(1)
            web.base_page.screenshot("Then 顯示「住客入住成功」提示")

        with allure.step("And 顯示「製卡」視窗"):
            assert web.base_page.has_element(
                web.check_in_list_page.locator.btn_make_card_new
            ), "製卡 Dialog 未開啟（新卡按鈕不存在）"
            web.check_in_list_page.close_make_card_dialog().sleep(0.5)
            web.base_page.screenshot("And 顯示「製卡」視窗")

        with allure.step("Postcondition 關閉 Check In Dialog"):
            web.check_in_list_page.close_check_in_dialog().sleep(0.5)
            web.base_page.screenshot("Postcondition 關閉 Check In Dialog")

        with allure.step("Then C/I清單狀態變更為「I:今日到達」"):
            # 切篩選到全部，搜尋驗證狀態
            web.check_in_list_page.select_checkin_status("all:全部").sleep(0.5)
            web.check_in_list_page.search_room(room).sleep(1)
            actual_status = web.check_in_list_page.get_order_status(room)
            web.base_page.assert_data("狀態", "I" in actual_status, True)
            web.base_page.screenshot("Then C/I清單狀態變更為「I:今日到達」")
