import allure
import pytest

from pages.base_page import BasePage
from pages.components.tip_component import TipComponent
from pages.components.header_component import HeaderComponent
from pages.room_assignment_page import RoomAssignmentPage
from tools.driver_helper import DriverHelper


@allure.feature("排房作業")
class TestRoomAssignment:

    @allure.story("明細排房")
    @pytest.mark.xdist_group("room_assignment")
    @pytest.mark.dependency(name="test_room_assignment_detail", scope="session")
    def test_room_assignment_detail(self):
        pages = [HeaderComponent, TipComponent, RoomAssignmentPage, BasePage]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")

        with allure.step("Given 使用者進入「排房作業」頁面"):
            web.header_component.expand_menu("接待").sleep(1)
            web.header_component.to_func_page("排房作業").sleep(1)
            web.base_page.screenshot("Given 使用者進入「排房作業」頁面")

        with allure.step("And 點擊「彙總」變更為「明細」Table"):
            web.base_page.click_toolbar_item("彙總").sleep(1)
            web.base_page.screenshot("And 點擊「彙總」變更為「明細」Table")

        with allure.step("And 搜尋訂房卡號"):
            web.room_assignment_page.search_ikey("00012539").sleep(1)
            web.base_page.screenshot("And 搜尋訂房卡號")

        with allure.step("And 從房間可排房Table點擊欲進行排房之方框"):
            if web.room_assignment_page.get_text_in_detail_tab("room_nos"):
                web.room_assignment_page.click_room_sta_checkbox()
                web.tip_component.click_ok().sleep(2)
            web.room_assignment_page.select_room_no("222")
            web.base_page.screenshot("And 從房間可排房Table點擊欲進行排房之方框")

        with allure.step("Then 房間圖示顯示為紅色方框並顯示住客姓名、入住日期、退房日期"):
            web.room_assignment_page.click_assignable_room_checkbox().sleep(1)
            web.base_page.assert_data(
                "房型", web.room_assignment_page.get_biggraph_room_type(222), "STD"
            )
            web.base_page.assert_data(
                "日期區間", web.room_assignment_page.get_biggraph_date_range(222), "04/14-04/15"
            )
            web.base_page.screenshot(
                "Then 房間圖示顯示為紅色方框並顯示住客姓名、入住日期、退房日期"
            )

        with allure.step("And 訂房卡明細之資料列顯示點擊房間之房號"):
            web.base_page.assert_data(
                "房號", web.room_assignment_page.get_text_in_detail_tab("room_nos"), "222"
            )
            web.base_page.screenshot("And 訂房卡明細之資料列顯示點擊房間之房號")

    @allure.story("明細鎖定排房")
    @pytest.mark.xdist_group("room_assignment")
    @pytest.mark.parametrize(
        "action, is_lock, is_readonly", [("勾選鎖定", True, True), ("取消鎖定", False, False)]
    )
    @pytest.mark.dependency(
        name="test_lock_room_assignment", depends=["test_room_assignment_detail"], scope="session"
    )
    def test_lock_room_assignment(self, action, is_lock, is_readonly):
        pages = [HeaderComponent, TipComponent, RoomAssignmentPage, BasePage]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")

        with allure.step("Given 使用者進入「排房作業」頁面"):
            web.header_component.expand_menu("接待").sleep(1)
            web.header_component.to_func_page("排房作業").sleep(1)
            web.base_page.screenshot("Given 使用者進入「排房作業」頁面")

        with allure.step("And 點擊[彙總]變更為「明細」Table"):
            web.base_page.click_toolbar_item("彙總").sleep(1)
            web.base_page.screenshot("And 點擊[彙總]變更為「明細」Table")

        with allure.step(f"And {action}[鎖定排房]欄位之CheckBox"):
            web.room_assignment_page.search_ikey("00012539").sleep(2)
            # 只有勾選鎖定的測試需要先判斷有沒有鎖定並解除，取消鎖定不用
            if web.room_assignment_page.is_lock_assign_checked() and action == "勾選鎖定":
                web.room_assignment_page.click_lock_assignment_checkbox()
                web.tip_component.click_ok()
            web.room_assignment_page.click_lock_assignment_checkbox()
            web.base_page.screenshot("And 勾選[鎖定排房]欄位之CheckBox")

        with allure.step("And 點擊[確定]"):
            web.tip_component.click_ok()
            web.base_page.screenshot("And 點擊[確定]")

            web.base_page.click_toolbar_item("明細").sleep(1)
            web.base_page.click_toolbar_item("彙總").sleep(1)

        with allure.step("And 訂房卡明細之房號欄位填滿紅色背景"):
            web.base_page.assert_data(
                "房號背景", web.room_assignment_page.is_room_nos_readonly(), is_readonly
            )
            web.base_page.screenshot("And 訂房卡明細之房號欄位填滿紅色背景")

        with allure.step("And 訂房卡明細之鎖定排房CheckBox顯示勾選"):
            web.base_page.assert_data(
                "鎖定排房勾選", web.room_assignment_page.is_lock_assign_checked(), is_lock
            )
            web.base_page.screenshot("And 訂房卡明細之鎖定排房CheckBox顯示勾選")
