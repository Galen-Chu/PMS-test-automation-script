import allure
import pytest
from pages.components.header_component import HeaderComponent
from pages.components.share_panel_component import SharePanelComponent
from pages.components.tip_component import TipComponent
from pages.room_control_page import RoomControlPage
from tools.driver_helper import DriverHelper
from tools.date_hepler import DateHelper


@allure.feature("房控管理")
class TestRoomControl:

    @allure.story("設定清掃房間-髒房")
    @pytest.mark.xdist_group("room_clean")
    @pytest.mark.dependency(name="test_room_control_dirty", scope="session")
    def test_room_control_dirty(self):
        self._test_room_control_status(
            floor="2F",
            room_no="220",
            status="髒房",
            icon_index=5,
            status_color="rgb(240, 45, 45)",
            toolbar_item="設定髒房",
        )

    @allure.story("設定清掃房間-乾淨")
    @pytest.mark.xdist_group("room_clean")
    @pytest.mark.dependency(
        name="test_room_control_clean", depends=["test_room_control_dirty"], scope="session"
    )
    def test_room_control_clean(self):
        self._test_room_control_status(
            floor="2F",
            room_no="220",
            status="乾淨",
            icon_index=0,
            status_color="rgb(53, 251, 14)",
            toolbar_item="設定乾淨",
        )

    @allure.story("設定清掃房間-待檢查")
    @pytest.mark.xdist_group("room_floor")
    @pytest.mark.dependency(name="test_room_control_check", scope="session")
    def test_room_control_check(self):
        self._test_room_control_status(
            floor="2F",
            room_no="222",
            status="髒房",
            icon_index=3,
            status_color="rgb(240, 45, 45)",
            toolbar_item="待檢查",
        )

    @allure.story("設定清掃樓層-髒房")
    @pytest.mark.xdist_group("room_floor")
    @pytest.mark.dependency(
        name="test_room_control_dirty_floor", depends=["test_room_control_check"], scope="session"
    )
    def test_room_control_dirty_floor(self):
        self._test_room_control_floor_status(
            floor="2F",
            room_nos=["221", "223"],
            filter_before="乾淨",
            icon_index=5,
            status_color="rgb(240, 45, 45)",
            toolbar_item="改髒房",
            filter_after="髒房",
        )

    @allure.story("設定清掃樓層-待檢查")
    @pytest.mark.xdist_group("room_floor")
    @pytest.mark.dependency(
        name="test_room_control_check_floor", depends=["test_room_control_check"], scope="session"
    )
    def test_room_control_check_floor(self):
        self._test_room_control_floor_status(
            floor="2F",
            room_nos=["224", "225"],
            filter_before="乾淨",
            icon_index=3,
            status_color="rgb(240, 45, 45)",
            toolbar_item="待檢查",
            filter_after="髒房",
        )

    @allure.story("設定清掃樓層-乾淨")
    @pytest.mark.xdist_group("room_floor")
    @pytest.mark.dependency(
        name="test_room_control_clean_floor", depends=["test_room_control_check"], scope="session"
    )
    def test_room_control_clean_floor(self):
        pages = [HeaderComponent, TipComponent, RoomControlPage, SharePanelComponent]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")
        with allure.step("Given 使用者進入「房控管理」頁面"):
            web.header_component.expand_menu("房務").sleep(1)
            web.header_component.to_func_page("房控管理").sleep(1)
            web.room_control_page.screenshot("Given 使用者進入「房控管理」頁面")

        with allure.step("When 選擇點擊欲變更狀態之房間所在樓層畫面中任意房間圖示之[方框]"):
            web.room_control_page.change_floor("2F")
            web.room_control_page.choose_room("221").sleep(1)
            web.room_control_page.screenshot(
                "When 選擇點擊欲變更狀態之��間所在樓層畫面中任意房間圖示之[方框]"
            )

        with allure.step("And 點擊[清掃樓層]"):
            web.room_control_page.click_toolbar_item_2("清掃樓層").sleep(1)
            web.room_control_page.screenshot("And 點擊[清掃樓層]")

        with allure.step("And 依篩選出的Table勾選欲變更狀態之房間號"):
            web.room_control_page.check_all_rooms().sleep(1)
            web.room_control_page.screenshot("And 依篩選出的Table勾選欲變更狀態之房間號")

        with allure.step("And 點擊選擇欲變更狀態之<清掃、待檢查、改髒房>"):
            web.room_control_page.click_toolbar_item_2("清掃").sleep(1)
            web.room_control_page.screenshot("And 點擊選擇欲變更狀態之<清掃、待檢查、改髒房>")

        with allure.step("Then 顯示'修改成功'提示"):
            web.tip_component.screenshot("顯示'修改成功'提示")
            web.tip_component.assert_data("修改成功", web.tip_component.get_tip_text(), "修改成功")
            web.tip_component.click_ok().sleep(1)

        with allure.step("And 依據<清掃、待檢查、改髒房>選擇變更房間顯示圖示"):
            web.room_control_page.close_clean_floor_dialog()
            web.share_panel_component.close_panel("功能選項").sleep(3)
            web.room_control_page.screenshot("房間顯示圖示")
            for room in ["221", "222", "223", "224", "225"]:
                web.room_control_page.assert_data_in_list(
                    f"房間{room}框顏色",
                    web.room_control_page.get_room_color(room),
                    "rgb(53, 251, 14)",
                )
                web.room_control_page.assert_data_not_in_list(
                    f"房間{room}顯示icon[3]",
                    web.room_control_page.get_room_icon(room, 3),
                    "iconShow",
                )
                web.room_control_page.assert_data_not_in_list(
                    f"房間{room}顯示icon[5]",
                    web.room_control_page.get_room_icon(room, 5),
                    "iconShow",
                )

    @allure.story("設定修理/參觀房間")
    @pytest.mark.xdist_group("room_repair_visit")
    @pytest.mark.dependency(name="test_room_control_repair_visit", scope="session")
    @pytest.mark.parametrize(
        "floor, room_no, category, start_date, end_date, reason, status_color",
        [
            (
                "2F",
                "226",
                "R : 修理",
                "2024.01.05",
                "2024.01.12",
                "測試用修理房",
                "rgb(5, 255, 226)",
            ),
            (
                "2F",
                "227",
                "S : 參觀",
                "2024.01.05",
                "2024.01.12",
                "測試用參觀房",
                "rgb(253, 148, 255)",
            ),
        ],
    )
    def test_room_control_repair_visit(
        self, floor, room_no, category, start_date, end_date, reason, status_color
    ):
        pages = [HeaderComponent, TipComponent, RoomControlPage, SharePanelComponent]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")
        with allure.step("Given 使用者進入「房控管理」頁面"):
            web.header_component.expand_menu("房務").sleep(1)
            web.header_component.to_func_page("房控管理").sleep(1)
            web.room_control_page.screenshot("Given 使用者進入「房控管理」頁面")

        with allure.step("When 選擇點擊欲變更狀態(類別)之房間圖示之[方框]"):
            web.room_control_page.change_floor(floor)
            web.room_control_page.choose_room(room_no).sleep(1)
            web.room_control_page.screenshot("When 選擇點擊欲變更狀態(類別)之房間圖示之[方框]")

        with allure.step("And 點擊[修理/參觀]"):
            web.room_control_page.click_toolbar_item_2("修理/參觀").sleep(1)
            web.room_control_page.screenshot("And 點擊[修理/參觀]")

        with allure.step(f"And [修理/參觀]選擇<{category}>"):
            web.room_control_page.select_category(category).sleep(1)
            web.room_control_page.screenshot(f"And [修理/參觀]選擇<{category}>")

        with allure.step("And 填寫必填欄位"):
            start_month = DateHelper.month_number_to_name(start_date.split(".")[1])
            end_month = DateHelper.month_number_to_name(end_date.split(".")[1])
            start_day = DateHelper.clear_0_prefix(start_date.split(".")[2])
            end_day = DateHelper.clear_0_prefix(end_date.split(".")[2])
            web.room_control_page.select_date_by_label(
                "開始日期", start_date.split(".")[0], start_month, start_day
            ).sleep(1)
            web.room_control_page.select_date_by_label(
                "結束日期", end_date.split(".")[0], end_month, end_day
            ).sleep(1)
            web.room_control_page.input_reason(reason).sleep(1)
            web.room_control_page.screenshot("And 填寫必填欄位")

        with allure.step("And 點擊儲存"):
            web.room_control_page.save_repair_visit_changes().sleep(1)
            web.room_control_page.screenshot("And 點擊儲存")

        with allure.step("Then 顯示'儲存成功'提示"):
            web.tip_component.screenshot("顯示'儲存成功'提示")
            web.tip_component.assert_data("儲存成功", web.tip_component.get_tip_text(), "儲存成功")
            web.tip_component.click_ok().sleep(1)

        with allure.step("And 依據<R：修理、S：參觀>選擇變更房間顯示圖示"):
            web.share_panel_component.close_panel("修理/參觀")
            web.share_panel_component.close_panel("功能選項").sleep(3)
            web.room_control_page.screenshot("房間顯示圖示")
            web.room_control_page.assert_data_in_list(
                "房間框顏色", web.room_control_page.get_room_color(room_no), status_color
            )
            web.room_control_page.assert_data(
                "顯示日期",
                web.room_control_page.has_use_date(
                    room_no,
                    f"{start_date.split('.')[1]}/{start_date.split('.')[2]}-{end_date.split('.')[1]}/{end_date.split('.')[2]}",
                ),
                True,
            )
            web.room_control_page.assert_data(
                "顯示原因", web.room_control_page.has_use_reason(room_no, reason), True
            )

    @allure.story("新增修理樓層")
    @pytest.mark.xdist_group("room_repair_visit")
    @pytest.mark.dependency(
        name="test_room_control_repair_floor",
        depends=["test_room_control_repair_visit"],
        scope="session",
    )
    def test_room_control_repair_floor(self):
        pages = [HeaderComponent, TipComponent, RoomControlPage, SharePanelComponent]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")
        with allure.step("Given 使用者進入「房控管理」頁面"):
            web.header_component.expand_menu("房務").sleep(1)
            web.header_component.to_func_page("房控管理").sleep(1)
            web.room_control_page.screenshot("Given 使用者進入「房控管理」頁面")

        with allure.step("When 選擇點擊欲變更狀態之房間所在樓層畫面中任意房間圖示之[方框]"):
            web.room_control_page.change_floor("2F")
            web.room_control_page.choose_room("226").sleep(1)
            web.room_control_page.screenshot(
                "When 選擇點擊欲變更狀態之房間所在樓層畫面中任意房間圖示之[方框]"
            )

        with allure.step("And 點擊[修理樓層]"):
            web.room_control_page.click_toolbar_item_2("修理樓層").sleep(1)
            web.room_control_page.screenshot("And 點擊[修理樓層]")

        with allure.step("And 填寫必填欄位"):
            web.room_control_page.select_date_by_label("從", "2024", "一月", "5").sleep(1)
            web.room_control_page.select_date_by_label("至", "2024", "一月", "12").sleep(1)
            web.room_control_page.set_reason_floor("多筆測試用修理樓層").sleep(1)
            web.room_control_page.screenshot("And 填寫必填欄位")

        with allure.step("And 依篩選出的Table勾選欲變更狀態之房間號"):
            for room in ["226", "227", "228", "229"]:
                web.room_control_page.check_room_floor(room).sleep(1)
            web.room_control_page.screenshot("And 依篩選出的Table勾選欲變更狀態之房間號")

        with allure.step("And 點擊[修理]"):
            web.room_control_page.click_toolbar_item_2("修理").sleep(1)
            web.room_control_page.screenshot("And 點擊[修理]")

        with allure.step("Then 顯示'error'房間提示"):
            web.tip_component.screenshot("顯示錯誤提示")
            web.tip_component.assert_data(
                "與已設定的日期重疊，請確認並重新選擇日期",
                web.room_control_page.get_error_rooms(),
                ["226", "227"],
            )

        with allure.step("And 依據修改內容變更房間顯示圖示之內容"):
            web.share_panel_component.close_panel("Todo")
            web.share_panel_component.close_panel("修理樓層")
            web.share_panel_component.close_panel("功能選項").sleep(3)
            web.room_control_page.screenshot("房間顯示圖示")
            for room in ["228", "229"]:
                web.room_control_page.assert_data_in_list(
                    f"房間{room}框顏色",
                    web.room_control_page.get_room_color(room),
                    "rgb(5, 255, 226)",
                )
                web.room_control_page.assert_data(
                    "顯示日期", web.room_control_page.has_use_date(room, "01/05-01/12"), True
                )
                web.room_control_page.assert_data(
                    "顯示原因",
                    web.room_control_page.has_use_reason(room, "多筆測試用修理樓層"),
                    True,
                )

    @allure.story("查詢修理/參觀樓層")
    @pytest.mark.xdist_group("room_repair_visit")
    @pytest.mark.dependency(
        name="test_room_control_visit_floor",
        depends=["test_room_control_repair_floor"],
        scope="session",
    )
    @pytest.mark.parametrize(
        "field, option, room_nos",
        [
            ("類別", "R : 修理", ["226", "228", "229"]),
            ("類別", "S : 參觀", ["227"]),
            ("樓層", "2 : 2", ["226", "227", "228", "229"]),
        ],
    )
    def test_room_control_search_repair_visit_floor(self, field, option, room_nos):
        pages = [HeaderComponent, TipComponent, RoomControlPage, SharePanelComponent]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")

        with allure.step("Given 使用者進入「房控管理」頁面"):
            web.header_component.expand_menu("房務").sleep(1)
            web.header_component.to_func_page("房控管理").sleep(1)
            web.room_control_page.screenshot("Given 使用者進入「房控管理」頁面")

        with allure.step("When 選擇點擊欲查詢修改狀態(類別)之房間圖示之「方框」"):
            web.room_control_page.change_floor("2F")
            web.room_control_page.choose_room("226").sleep(1)
            web.room_control_page.screenshot(
                "When 選擇點擊欲查詢修改狀態(類別)之房間圖示之「方框」"
            )

        with allure.step("And 點擊[查詢修理/參觀]"):
            web.room_control_page.click_toolbar_item_2("查詢修理/參觀").sleep(1)
            web.room_control_page.screenshot("And 點擊[查詢修理/參觀]")

        with allure.step("And 填寫欲查詢之<類別、樓層、房號>"):
            web.room_control_page.clear_value_by_label("房號").sleep(1)
            web.room_control_page.select(field, option).sleep(1)
            web.room_control_page.screenshot("And 填寫欲查詢之<類別、樓層、房號>")

        with allure.step("And 點擊[藍色放大鏡]進行查詢"):
            web.room_control_page.search().sleep(1)
            web.room_control_page.screenshot("And 點擊[藍色放大鏡]進行查詢")

        with allure.step("Then 顯示查詢結果"):
            web.room_control_page.screenshot("顯示查詢結果")
            for room_no in room_nos:
                web.room_control_page.assert_data_in_list(
                    f"查詢結果房號 {room_no}", web.room_control_page.get_room_repair_list(), room_no
                )

    @allure.story("修改修理/參觀樓層")
    @pytest.mark.xdist_group("room_repair_visit")
    @pytest.mark.dependency(
        name="test_room_control_modify_repair_visit",
        depends=["test_room_control_repair_floor"],
        scope="session",
    )
    def test_room_control_modify_repair_visit(self):
        pages = [HeaderComponent, TipComponent, RoomControlPage, SharePanelComponent]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")

        with allure.step("Given 使用者進入「房控管理」頁面"):
            web.header_component.expand_menu("房務").sleep(1)
            web.header_component.to_func_page("房控管理").sleep(1)
            web.room_control_page.screenshot("Given 使用者進入「房控管理」頁面")

        with allure.step("When 選擇點擊欲查詢修改狀態(類別)之房間圖示之「方框」"):
            web.room_control_page.change_floor("2F")
            web.room_control_page.choose_room("227").sleep(1)
            web.room_control_page.screenshot(
                "When 選擇點擊欲查詢修改狀態(類別)之房間圖示之「方框」"
            )

        with allure.step("And 點擊[查詢修理/參觀]"):
            web.room_control_page.click_toolbar_item_2("查詢修理/參觀").sleep(1)
            web.room_control_page.screenshot("And 點擊[查詢修理/參觀]")

        with allure.step("And 點擊[藍色放大鏡]進行查詢"):
            web.room_control_page.search().sleep(1)
            web.room_control_page.screenshot("And 點擊[藍色放大鏡]進行查詢")

        with allure.step("And 點擊Table之資料條或進行勾選"):
            web.room_control_page.check_room_repair_item("227").sleep(1)
            web.room_control_page.screenshot("And 點擊Table之資料條或進行勾選")

        with allure.step("And 點擊[橘色筆]進行修改"):
            web.room_control_page.click_toolbar_with_icon("edit").sleep(1)
            web.room_control_page.screenshot("And 點擊[橘色筆]進行修改")

        with allure.step("And 選擇並修改[開始日期]、[結束日期]、[修理/參觀原因]"):
            web.room_control_page.change_room_repair_day("結束日期", "26").sleep(1)
            web.room_control_page.input_room_repair_reason("編輯測試用修理樓層").sleep(1)
            web.room_control_page.screenshot(
                "And 選擇並修改[開始日期]、[結束日期]、[修理/參觀原因]"
            )

        with allure.step("And 點擊[確定]"):
            web.room_control_page.save_room_repair().sleep(1)
            web.room_control_page.screenshot("And 點擊[確定]")

        with allure.step("Then 顯示'儲存成功'提示"):
            web.tip_component.screenshot("顯示'儲存成功'提示")
            web.tip_component.assert_data("儲存成功", web.tip_component.get_tip_text(), "儲存成功")
            web.tip_component.click_ok().sleep(1)

        with allure.step("And 依據修改內容變更房間顯示圖示之內容"):
            web.share_panel_component.close_panel("查詢修理/參觀")
            web.share_panel_component.close_panel("功能選項").sleep(3)
            web.room_control_page.screenshot("房間顯示圖示")
            web.room_control_page.assert_data_in_list(
                "房間框顏色", web.room_control_page.get_room_color("227"), "rgb(253, 148, 255)"
            )
            web.room_control_page.assert_data(
                "顯示日期", web.room_control_page.has_use_date("227", "01/05-01/26"), True
            )
            web.room_control_page.assert_data(
                "顯示原因", web.room_control_page.has_use_reason("227", "編輯測試用修理樓層"), True
            )

    @allure.story("刪除修理/參觀樓層")
    @pytest.mark.xdist_group("room_repair_visit")
    @pytest.mark.dependency(
        name="test_room_control_remove_repair_visit_floor",
        depends=["test_room_control_repair_floor"],
        scope="session",
    )
    def test_room_control_remove_repair_visit_floor(self):
        pages = [HeaderComponent, TipComponent, RoomControlPage, SharePanelComponent]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")

        with allure.step("Given 使用者進入「房控管理」頁面"):
            web.header_component.expand_menu("房務").sleep(1)
            web.header_component.to_func_page("房控管理").sleep(1)
            web.room_control_page.screenshot("Given 使用者進入「房控管理」頁面")

        with allure.step("When 選擇點擊欲查詢修改狀態(類別)之房間圖示之「方框」"):
            web.room_control_page.change_floor("2F")
            web.room_control_page.choose_room("226").sleep(1)
            web.room_control_page.screenshot(
                "When 選擇點擊欲查詢修改狀態(類別)之房間圖示之「方框」"
            )

        with allure.step("And 點擊[查詢修理/參觀]"):
            web.room_control_page.click_toolbar_item_2("查詢修理/參觀").sleep(1)
            web.room_control_page.screenshot("And 點擊[查詢修理/參觀]")

        with allure.step("And 填寫欲查詢之<類別、樓層、房號>"):
            web.room_control_page.clear_value_by_label("房號").sleep(1)
            web.room_control_page.select("樓層", "2 : 2").sleep(1)
            web.room_control_page.screenshot("And 填寫欲查詢之<類別、樓層、房號>")

        with allure.step("And 點擊[藍色放大鏡]進行查詢"):
            web.room_control_page.search().sleep(1)
            web.room_control_page.screenshot("And 點擊[藍色放大鏡]進行查詢")

        with allure.step("And 點擊Table之資料條或進行勾選"):
            web.room_control_page.check_all_room_repair()
            web.room_control_page.screenshot("And 點擊Table之資料條或進行勾選")

        with allure.step("And 點擊[橘色減號]進行刪除"):
            web.room_control_page.click_toolbar_with_icon("remove").sleep(1)
            web.room_control_page.screenshot("And 點擊[橘色減號]進行刪除")

        with allure.step("Then 顯示'儲存成功'提示"):
            web.tip_component.screenshot("顯示'儲存成功'提示")
            web.tip_component.assert_data("儲存成功", web.tip_component.get_tip_text(), "儲存成功")
            web.tip_component.click_ok().sleep(1)

        with allure.step("And 根據刪除變更房間清掃狀態及房間顯示圖示之方框"):
            web.share_panel_component.close_panel("查詢修理/參觀")
            web.share_panel_component.close_panel("功能選項").sleep(3)
            web.room_control_page.screenshot("房間顯示圖示")
            for room_no in ["226", "227", "228", "229"]:
                web.room_control_page.assert_data_in_list(
                    f"房間{room_no}框顏色",
                    web.room_control_page.get_room_color(room_no),
                    "rgb(240, 45, 45)",
                )
                web.room_control_page.assert_data(
                    f"房間{room_no}顯示日期", web.room_control_page.has_use_date(room_no, ""), True
                )
                web.room_control_page.assert_data(
                    f"房間{room_no}顯示原因",
                    web.room_control_page.has_use_reason(room_no, ""),
                    True,
                )
                web.room_control_page.assert_data_in_list(
                    f"房間{room_no}顯示icon[5]",
                    web.room_control_page.get_room_icon(room_no, 5),
                    "iconShow",
                )

    @allure.story("清掃修理/參觀後髒房")
    @pytest.mark.xdist_group("room_repair_visit")
    @pytest.mark.dependency(
        name="test_room_control_clean_repair_rooms",
        depends=["test_room_control_remove_repair_visit_floor"],
        scope="session",
    )
    def test_room_control_clean_repair_rooms(self):
        pages = [HeaderComponent, TipComponent, RoomControlPage, SharePanelComponent]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")

        with allure.step("Given 使用者進入「房控管理」頁面"):
            web.header_component.expand_menu("房務").sleep(1)
            web.header_component.to_func_page("房控管理").sleep(1)
            web.room_control_page.screenshot("Given 使用者進入「房控管理」頁面")

        with allure.step("When 選擇點擊欲變更狀態之房間所在樓層畫面中任意房間圖示之[方框]"):
            web.room_control_page.change_floor("2F")
            web.room_control_page.choose_room("226").sleep(1)
            web.room_control_page.screenshot(
                "When 選擇點擊欲變更狀態之房間所在樓層畫面中任意房間圖示之[方框]"
            )

        with allure.step("And 點擊[清掃樓層]"):
            web.room_control_page.click_toolbar_item_2("清掃樓層").sleep(1)
            web.room_control_page.screenshot("And 點擊[清掃樓層]")

        with allure.step("And 依篩選出的Table勾選欲變更狀態之房間號"):
            web.room_control_page.check_all_rooms().sleep(1)
            web.room_control_page.screenshot("And 依篩選出的Table勾選欲變更狀態之房間號")

        with allure.step("And 點擊選擇欲變更狀態之<清掃、待檢查、改髒房>"):
            web.room_control_page.click_toolbar_item_2("清掃").sleep(1)
            web.room_control_page.screenshot("And 點擊選擇欲變更狀態之<清掃、待檢查、改髒房>")

        with allure.step("Then 顯示'修改成功'提示"):
            web.tip_component.screenshot("顯示'修改成功'提示")
            web.tip_component.assert_data("修改成功", web.tip_component.get_tip_text(), "修改成功")
            web.tip_component.click_ok().sleep(1)

        with allure.step("And 依據<清掃、待檢查、改髒房>選擇變更房間顯示圖示"):
            web.room_control_page.close_clean_floor_dialog()
            web.share_panel_component.close_panel("功能選項").sleep(3)
            web.room_control_page.screenshot("房間顯示圖示")
            for room in ["226", "227", "228", "229"]:
                web.room_control_page.assert_data_in_list(
                    f"房間{room}框顏色",
                    web.room_control_page.get_room_color(room),
                    "rgb(53, 251, 14)",
                )
                web.room_control_page.assert_data_not_in_list(
                    f"房間{room}顯示icon[3]",
                    web.room_control_page.get_room_icon(room, 3),
                    "iconShow",
                )
                web.room_control_page.assert_data_not_in_list(
                    f"房間{room}顯示icon[5]",
                    web.room_control_page.get_room_icon(room, 5),
                    "iconShow",
                )

    @allure.story("設定房間-瑕疵房")
    @pytest.mark.xdist_group("room_oos")
    @pytest.mark.dependency(name="test_room_control_oos", scope="session")
    def test_room_control_oos(self):
        pages = [HeaderComponent, TipComponent, RoomControlPage, SharePanelComponent]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")

        with allure.step("Given 使用者進入「房控管理」頁面"):
            web.header_component.expand_menu("房務").sleep(1)
            web.header_component.to_func_page("房控管理").sleep(1)
            web.room_control_page.screenshot("Given 使用者進入「房控管理」頁面")

        with allure.step("When 選擇點擊欲設定為瑕疵房之房間"):
            web.room_control_page.change_floor("2F")
            web.room_control_page.choose_room("217").sleep(1)
            web.room_control_page.screenshot("When 選擇點擊欲設定為瑕疵房之房間")

        with allure.step("And 點擊[瑕疵房]"):
            web.room_control_page.click_toolbar_item_2("瑕疵房").sleep(1)
            web.room_control_page.screenshot("And 點擊[瑕疵房]")

        with allure.step("And 輸入瑕疵房設定之理由敘述"):
            web.room_control_page.input_defect_reason("測試用瑕疵房設定").sleep(1)
            web.room_control_page.screenshot("And 輸入瑕疵房設定之理由敘述")

        with allure.step("And 點擊[設定]"):
            web.room_control_page.click_toolbar_item_2("設定").sleep(1)
            web.room_control_page.screenshot("And 點擊[設定]")

        with allure.step("Then 顯示'設定成功'提示"):
            web.tip_component.screenshot("顯示'設定成功'提示")
            web.tip_component.assert_data("設定成功", web.tip_component.get_tip_text(), "設定成功")
            web.tip_component.click_ok().sleep(1)

        with allure.step("And 依據瑕疵房設定變更房間顯示圖示"):
            web.share_panel_component.close_panel("功能選項").sleep(3)
            web.room_control_page.screenshot("房間顯示圖示")
            web.room_control_page.assert_data_in_list(
                "房間框顏色", web.room_control_page.get_room_color("217"), "rgb(155, 160, 161)"
            )
            web.room_control_page.assert_data_in_list(
                "房間顯示icon[4]", web.room_control_page.get_room_icon("217", 4), "iconShow"
            )

    @allure.story("設定房間-清除瑕疵房")
    @pytest.mark.xdist_group("room_oos")
    @pytest.mark.dependency(
        name="test_room_control_clear_oos", depends=["test_room_control_oos"], scope="session"
    )
    def test_room_control_clear_oos(self):
        pages = [HeaderComponent, TipComponent, RoomControlPage, SharePanelComponent]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")

        with allure.step("Given 使用者進入「房控管理」頁面"):
            web.header_component.expand_menu("房務").sleep(1)
            web.header_component.to_func_page("房控管理").sleep(1)
            web.room_control_page.screenshot("Given 使用者進入「房控管理」頁面")

        with allure.step("When 選擇點擊欲刪除設定為瑕疵房之房間"):
            web.room_control_page.change_floor("2F")
            web.room_control_page.choose_room("217").sleep(1)
            web.room_control_page.screenshot("When 選擇點擊欲刪除設定為瑕疵房之房間")

        with allure.step("And 點擊[瑕疵房]"):
            web.room_control_page.click_toolbar_item_2("瑕疵房").sleep(1)
            web.room_control_page.screenshot("And 點擊[瑕疵房]")

        with allure.step("And 點擊[清除]"):
            web.room_control_page.click_toolbar_item_2("清除").sleep(1)
            web.room_control_page.screenshot("And 點擊[清除]")

        with allure.step("Then 顯示'清除成功'提示"):
            web.tip_component.screenshot("顯示'清除成功'提示")
            web.tip_component.assert_data("清除成功", web.tip_component.get_tip_text(), "清除成功")
            web.tip_component.click_ok().sleep(1)

        with allure.step("And 房間圖示顯示還原為原始狀態"):
            web.share_panel_component.close_panel("功能選項").sleep(3)
            web.room_control_page.screenshot("房間顯示圖示")
            web.room_control_page.assert_data_in_list(
                "房間框顏色", web.room_control_page.get_room_color("217"), "rgb(53, 251, 14)"
            )
            web.room_control_page.assert_data_not_in_list(
                "房間顯示icon[4]", web.room_control_page.get_room_icon("217", 4), "iconShow"
            )

    @allure.story("設定房間-拆併床")
    @pytest.mark.xdist_group("room_bed_setup")
    @pytest.mark.parametrize(
        "floor, room_no, bed_setting",
        [("2F", "215", "拆床"), ("2F", "215", "併床"), ("2F", "215", "無設定")],
    )
    def test_room_control_bed_setup(self, floor, room_no, bed_setting):
        pages = [HeaderComponent, TipComponent, RoomControlPage, SharePanelComponent]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")

        with allure.step("Given 使用者進入「房控管理」頁面"):
            web.header_component.expand_menu("房務").sleep(1)
            web.header_component.to_func_page("房控管理").sleep(1)
            web.room_control_page.screenshot("Given 使用者進入「房控管理」頁面")

        with allure.step("When 選擇點擊欲變更拆併床設定之房間"):
            web.room_control_page.change_floor(floor)
            web.room_control_page.choose_room(room_no).sleep(1)
            web.room_control_page.screenshot("When 選擇點擊欲變更拆併床設定之房間")

        with allure.step("And 點擊[拆併床]"):
            web.room_control_page.click_toolbar_item_2("拆併床").sleep(1)
            web.room_control_page.screenshot("And 點擊[拆併床]")

        with allure.step("And 點擊Table勾選該樓層欲變更拆併床設定之房型房號"):
            web.room_control_page.check_bed_setup_room(room_no).sleep(1)
            web.room_control_page.screenshot("And 點擊Table勾選該樓層欲變更拆併床設定之房型房號")

        with allure.step(f"And 選擇<{bed_setting}>"):
            web.room_control_page.select_bed_setting(bed_setting).sleep(1)
            web.room_control_page.screenshot(f"And 選擇<{bed_setting}>")

        with allure.step("And 點擊[橘色磁碟片]進行儲存"):
            web.room_control_page.save_bed_setup().sleep(1)
            web.room_control_page.screenshot("And 點擊[橘色磁碟片]進行儲存")

        with allure.step("Then 顯示'儲存成功'提示"):
            web.tip_component.screenshot("顯示'儲存成功'提示")
            web.tip_component.assert_data("儲存成功", web.tip_component.get_tip_text(), "儲存成功")
            web.tip_component.click_ok().sleep(1)

        with allure.step(f"And Table之拆併床欄位依據<{bed_setting}>設定進行變更"):
            web.room_control_page.screenshot(f"Table之拆併床欄位依據<{bed_setting}>設定進行變更")
            web.room_control_page.assert_data(
                f"房間{room_no}拆併床設定",
                web.room_control_page.get_bed_setup_status(room_no),
                bed_setting,
            )

        with allure.step("And 點擊「關閉」視窗回到「房控管理」頁面"):
            web.room_control_page.close_bed_setup_dialog().sleep(1)
            web.share_panel_component.close_panel("功能選項").sleep(2)
            web.room_control_page.screenshot("And 點擊「關閉」視窗回到「房控管理」頁面")
            web.room_control_page.assert_data_in_list(
                "房間框顏色", web.room_control_page.get_room_color(room_no), "rgb(53, 251, 14)"
            )
            if bed_setting == "併床":
                web.room_control_page.assert_data_in_list(
                    "房間顯示icon[8]", web.room_control_page.get_room_icon(room_no, 8), "iconShow"
                )
            else:
                web.room_control_page.assert_data_not_in_list(
                    "房間顯示icon[8]", web.room_control_page.get_room_icon(room_no, 8), "iconShow"
                )

    def _test_room_control_status(
        self,
        floor="2F",
        room_no="220",
        status="髒房",
        icon_index=2,
        status_color="rgb(240, 45, 45)",
        toolbar_item="設定髒房",
    ):
        pages = [HeaderComponent, TipComponent, RoomControlPage, SharePanelComponent]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")

        with allure.step("Given 使用者進入「房控管理」頁面"):
            web.header_component.expand_menu("房務").sleep(1)
            web.header_component.to_func_page("房控管理").sleep(1)
            web.room_control_page.screenshot("Given 使用者進入「房控管理」頁面")

        with allure.step("When 選擇點擊欲變更狀態之房間所在樓層畫面中任意房間圖示之[方框]"):
            web.room_control_page.change_floor(floor)
            web.room_control_page.choose_room(room_no).sleep(1)
            web.room_control_page.screenshot(
                "When 選擇點擊欲變更狀態之房間所在樓層畫面中任意房間圖示之[方框]"
            )

        with allure.step("And 點擊[清掃]"):
            web.room_control_page.click_toolbar_item_2("清掃")
            web.room_control_page.screenshot("And 點擊[清掃]")

        with allure.step("And 選擇欲變更狀態之<清掃、待檢查、改髒房>"):
            web.room_control_page.click_toolbar_item_2(toolbar_item).sleep(1)
            web.room_control_page.screenshot("And 選擇欲變更狀態之<清掃、待檢查、改髒房>")

        with allure.step("Then 顯示'儲存成功'提示"):
            web.tip_component.screenshot("顯示'儲存成功'提示")
            web.tip_component.assert_data("儲存成功", web.tip_component.get_tip_text(), "儲存成功")
            web.tip_component.click_ok().sleep(1)

        with allure.step("And 依據<清掃、待檢查、改髒房>更新清掃狀態"):
            web.room_control_page.screenshot("更新清掃狀態")
            web.room_control_page.assert_data(
                "清掃狀態", web.room_control_page.get_room_status(), status
            )

        with allure.step("And 依據<清掃、待檢查、改髒房>選擇變更房間顯示圖示"):
            web.share_panel_component.close_panel("清掃房間")
            web.share_panel_component.close_panel("功能選項").sleep(3)
            web.room_control_page.screenshot("房間顯示圖示")
            web.room_control_page.assert_data_in_list(
                "房間框顏色", web.room_control_page.get_room_color(room_no), status_color
            )
            if icon_index > 0:
                web.room_control_page.assert_data_in_list(
                    f"房間顯示icon[{icon_index}]",
                    web.room_control_page.get_room_icon(room_no, icon_index),
                    "iconShow",
                )

    def _test_room_control_floor_status(
        self,
        floor="2F",
        room_nos=None,
        filter_before="乾淨",
        icon_index=2,
        status_color="rgb(240, 45, 45)",
        toolbar_item="改髒房",
        filter_after="髒房",
    ):
        pages = [HeaderComponent, TipComponent, RoomControlPage, SharePanelComponent]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")
        with allure.step("Given 使用者進入「房控管理」頁面"):
            web.header_component.expand_menu("房務").sleep(1)
            web.header_component.to_func_page("房控管理").sleep(1)
            web.room_control_page.screenshot("Given 使用者進入「房控管理」頁面")

        with allure.step("When 選擇點擊欲變更狀態之房間所在樓層畫面中任意房間圖示之[方框]"):
            web.room_control_page.change_floor(floor)
            web.room_control_page.choose_room(room_nos[0]).sleep(1)
            web.room_control_page.screenshot(
                "When 選擇點擊欲變更狀態之房間所在樓層畫面中任意房間圖示之[方框]"
            )

        with allure.step("And 點擊[清掃樓層]"):
            web.room_control_page.click_toolbar_item_2("清掃樓層").sleep(1)
            web.room_control_page.screenshot("點擊[清掃樓層]")
            web.room_control_page.assert_data_in_list(
                "髒房有一筆222房間資料", web.room_control_page.get_room_status_list(), "222"
            )

        with allure.step("And 依篩選出的Table勾選欲變更狀態之房間號"):
            web.room_control_page.filter_room_status(filter_before)
            for room in room_nos:
                web.room_control_page.check_room(room).sleep(1)
            web.room_control_page.screenshot("And 依篩選出的Table勾選欲變更狀態之房間號")

        with allure.step("And 點擊選擇欲變更狀態之<清掃、待檢查、改髒房>"):
            web.room_control_page.click_toolbar_item_2(toolbar_item).sleep(1)
            web.room_control_page.screenshot("And 點擊選擇欲變更狀態之<清掃、待檢查、改髒房>")

        with allure.step("Then 顯示'修改成功'提示"):
            web.tip_component.screenshot("顯示'修改成功'提示")
            web.tip_component.assert_data("修改成功", web.tip_component.get_tip_text(), "修改成功")
            web.tip_component.click_ok().sleep(1)

        with allure.step(f"And 確認{filter_after}清單"):
            web.room_control_page.filter_room_status(filter_after).sleep(1)
            web.room_control_page.screenshot(f"確認{filter_after}清單")
            for room in room_nos:
                web.room_control_page.assert_data_in_list(
                    f"房間號碼{room}", web.room_control_page.get_room_status_list(), room
                )

        with allure.step("And 依據<清掃、待檢查、改髒房>選擇變更房間顯示圖示"):
            web.room_control_page.close_clean_floor_dialog()
            web.share_panel_component.close_panel("功能選項").sleep(3)
            web.room_control_page.screenshot("房間顯示圖示")
            for room in room_nos:
                web.room_control_page.assert_data_in_list(
                    f"房間{room}框顏色", web.room_control_page.get_room_color(room), status_color
                )
                web.room_control_page.assert_data_in_list(
                    f"房間{room}顯示icon[{icon_index}]",
                    web.room_control_page.get_room_icon(room, icon_index),
                    "iconShow",
                )
