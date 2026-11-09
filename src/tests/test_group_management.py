import allure
import pytest
from pages.athena_base_page import AthenaBasePage
from pages.co_list_page import CoListPage
from pages.components.header_component import HeaderComponent
from pages.components.share_panel_component import SharePanelComponent
from pages.components.tip_component import TipComponent
from pages.group_management_page import GroupManagementPage
from tests.share_steps import ShareSteps
from tools.driver_helper import DriverHelper
from tools.test_data_helper import get_test_data


@allure.feature("團體管理")
class TestGroupManagement:

    @allure.story("團體管理 - 調整退房日")
    @pytest.mark.xdist_group("test_group_management")
    @pytest.mark.dependency(name="test_change_co_date", scope="session")
    @pytest.mark.parametrize("data_key", ["change_co_date_extend", "change_co_date_shorten"])
    def test_change_co_date(self, logged_in_driver, data_key):
        data = get_test_data("test_group_management", data_key)
        master_nos = data["master_nos"]
        original_co_day = data["original_co_day"]
        original_co_date = data["original_co_date"]
        new_co_day = data["new_co_day"]
        new_co_date = data["new_co_date"]

        pages = [GroupManagementPage, HeaderComponent, TipComponent, AthenaBasePage]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        with allure.step("Given 使用者進入「團體管理」頁面"):
            web.header_component.expand_menu("出納").sleep(1)
            web.header_component.to_func_page("團體管理").sleep(1)
            web.athena_base_page.screenshot("Given 使用者進入「團體管理」頁面")

        with allure.step("Given 復原：若退房日已被改則改回原值"):
            web.group_management_page.search_by_master_nos(master_nos).sleep(1)
            list_co = web.group_management_page.get_list_co_dat()
            if list_co != original_co_date:
                web.group_management_page.click_group_row(master_nos).sleep(0.5)
                web.group_management_page.click_group_detail().sleep(2)
                web.group_management_page.click_change_co_date().sleep(1)
                web.group_management_page.select_new_co_date(original_co_day).sleep(1)
                web.group_management_page.click_save().sleep(1)
                web.tip_component.click_ok().sleep(1)
                web.tip_component.click_ok().sleep(1)
                # 等 grid 刷新完成再關 panel——負載下 close 撞進房價回寫中間態會跳「資料尚未儲存」confirm 攔後續操作
                web.group_management_page.wait_eco_dat_changed(list_co)
                web.group_management_page.close_panel_by_title("改退房日").sleep(0.5)
                web.group_management_page.close_panel_by_title("團體明細").sleep(0.5)
            web.athena_base_page.screenshot("Given 復原：若退房日已被改則改回原值")

        with allure.step("And 點擊欲進行設定之資料列"):
            web.group_management_page.search_by_master_nos(master_nos).sleep(1)
            web.group_management_page.click_group_row(master_nos).sleep(0.5)
            web.athena_base_page.screenshot("And 點擊欲進行設定之資料列")

        with allure.step("And 點擊[團體明細]"):
            web.group_management_page.click_group_detail().sleep(2)
            web.athena_base_page.screenshot("And 點擊[團體明細]")

        with allure.step("When 點擊[退房日期]"):
            web.group_management_page.click_change_co_date().sleep(1)
            web.athena_base_page.screenshot("When 點擊[退房日期]")

        with allure.step("And 「改退房日」視窗選擇[新退房日期]"):
            web.group_management_page.select_new_co_date(new_co_day).sleep(1)
            web.athena_base_page.screenshot("And 「改退房日」視窗選擇[新退房日期]")

        with allure.step("And 點擊[橘色磁碟片]進行儲存"):
            web.group_management_page.click_save().sleep(1)
            web.athena_base_page.screenshot("And 點擊[橘色磁碟片]進行儲存")

        with allure.step("Then 顯示「修改退房日期成功」提示"):
            tip_text = web.tip_component.get_tip_text()
            web.athena_base_page.assert_data("修改退房日期成功提示", tip_text, "修改退房日期成功")
            web.athena_base_page.screenshot("Then 顯示「修改退房日期成功」提示")
            web.tip_component.click_ok().sleep(1)

        with allure.step("And 顯示「請檢查房價」提示"):
            tip_text = web.tip_component.get_tip_text()
            web.athena_base_page.assert_data("請檢查房價提示", tip_text, "請檢查房價")
            web.athena_base_page.screenshot("And 顯示「請檢查房價」提示")
            web.tip_component.click_ok().sleep(1)

        with allure.step("Then 「原退房日」欄位變更為修改後的退房日期"):
            web.group_management_page.wait_eco_dat_changed(original_co_date)
            web.athena_base_page.assert_data(
                "原退房日", web.group_management_page.get_eco_dat(), new_co_date
            )
            web.athena_base_page.screenshot("Then 「原退房日」欄位變更為修改後的退房日期")

        with allure.step("Postcondition 關閉改退房日 Panel"):
            web.group_management_page.close_panel_by_title("改退房日").sleep(0.5)
            web.athena_base_page.screenshot("Postcondition 關閉改退房日 Panel")

    @allure.story("團體管理 - 清子房間")
    @pytest.mark.xdist_group("test_group_management")
    @pytest.mark.dependency(name="test_clear_sub_room", scope="session")
    def test_clear_sub_room(self, logged_in_driver):
        data = get_test_data("test_group_management", "clear_sub_room")
        master_nos = data["master_nos"]
        room_no = data["room_no"]

        pages = [
            GroupManagementPage,
            CoListPage,
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            AthenaBasePage,
        ]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        with allure.step("Given 復原：若子房已退房則還原"):
            web.header_component.expand_menu("出納").sleep(1)
            web.header_component.to_func_page("C/O 清單").sleep(1)
            ShareSteps.restore_room_to_inhouse(web, room_no)
            web.athena_base_page.screenshot("Given 復原：若子房已退房則還原")

        with allure.step("Given 使用者進入「團體管理」頁面"):
            web.header_component.expand_menu("出納").sleep(1)
            web.header_component.to_func_page("團體管理").sleep(1)
            web.athena_base_page.screenshot("Given 使用者進入「團體管理」頁面")

        with allure.step("And 點擊欲進行設定之資料列"):
            web.group_management_page.search_by_master_nos(master_nos).sleep(1)
            web.group_management_page.click_group_row(master_nos).sleep(0.5)
            web.athena_base_page.screenshot("And 點擊欲進行設定之資料列")

        with allure.step("And 點擊[團體明細]"):
            web.group_management_page.click_group_detail().sleep(2)
            web.athena_base_page.screenshot("And 點擊[團體明細]")

        with allure.step("When 已入住頁籤勾選子房並點擊[清子房間]"):
            web.group_management_page.check_ci_sub_room(room_no).sleep(0.5)
            web.group_management_page.click_clean_sub_room().sleep(1)
            # 清子房間為帳務操作，未開班時觸發開班 dialog 攔截首次 click；開班後重 click 進錯誤提示
            if web.athena_base_page.has_element(web.co_list_page.locator.dialog_shift):
                ShareSteps.open_shift(web, "FO : 飯店櫃檯", "a", "autotest")
                web.athena_base_page.sleep(1)
                web.group_management_page.click_clean_sub_room().sleep(1)
            web.athena_base_page.screenshot("When 已入住頁籤勾選子房並點擊[清子房間]")

        with allure.step("And 「尚有未入的預估款」提示勾選子房並確定"):
            web.group_management_page.check_err_dialog_ck().sleep(0.5)
            web.group_management_page.click_err_dialog_confirm().sleep(1)
            web.athena_base_page.screenshot("And 「尚有未入的預估款」提示勾選子房並確定")

        with allure.step("And 「是否要 Early C/O」提示再次勾選並確定"):
            web.group_management_page.check_err_dialog_ck().sleep(0.5)
            web.group_management_page.click_err_dialog_confirm().sleep(1)
            web.athena_base_page.screenshot("And 「是否要 Early C/O」提示再次勾選並確定")

        with allure.step("Then 顯示「退房完成」提示"):
            tip_text = web.tip_component.get_tip_text()
            web.athena_base_page.assert_data("退房完成提示", tip_text, "退房完成")
            web.athena_base_page.screenshot("Then 顯示「退房完成」提示")
            web.tip_component.click_ok().sleep(1)

        with allure.step("Then 「已入住」頁籤移除已退房的子房間"):
            removed = not web.group_management_page.has_ci_room(room_no)
            web.athena_base_page.assert_data("已入住頁籤移除子房", removed, True)
            web.athena_base_page.screenshot("Then 「已入住」頁籤移除已退房的子房間")

        with allure.step("Postcondition 還原子房（避免污染同 group #471 全部子房假設）"):
            web.group_management_page.close_panel_by_title("團體明細").sleep(0.5)
            web.header_component.expand_menu("出納").sleep(1)
            web.header_component.to_func_page("C/O 清單").sleep(1)
            ShareSteps.restore_room_to_inhouse(web, room_no)
            web.athena_base_page.screenshot(
                "Postcondition 還原子房（避免污染同 group #471 全部子房假設）"
            )
