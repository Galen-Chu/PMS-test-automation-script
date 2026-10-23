from datetime import datetime
import allure
import pytest

from pages.athena_base_page import AthenaBasePage
from pages.components.share_panel_component import SharePanelComponent
from pages.components.tip_component import TipComponent
from pages.components.header_component import HeaderComponent
from pages.lost_management_page import LostManagementPage
from pages.reservation_page import ReservationPage
from tools.driver_helper import DriverHelper
from tools.random_helper import RandomHelper


@allure.feature("失物管理")
class TestLostManagement:

    @allure.story("新增一筆遺失")
    @pytest.mark.xdist_group("lost_item")
    @pytest.mark.dependency(name="test_add_lost_item", scope="session")
    def test_add_lost_item(self, logged_in_driver):
        pages = [
            LostManagementPage,
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            AthenaBasePage,
        ]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        with allure.step("Given 使用者進入「失物管理」頁面"):
            web.header_component.expand_menu("接待").sleep(1)
            web.header_component.to_func_page("失物管理").sleep(1)
            web.athena_base_page.screenshot("Given 使用者進入「失物管理」頁面")

        with allure.step("When 點擊[橘色加號]進行新增"):
            web.athena_base_page.click_toolbar_with_icon("add")
            web.athena_base_page.screenshot("When 點擊[橘色加號]進行新增")

        with allure.step("And 選擇[狀態]為<遺失>"):
            web.lost_management_page.select_status_in_dialog("遺失")
            web.athena_base_page.screenshot("And 選擇[狀態]為<遺失>")

        with allure.step("And 輸入[物品名稱]"):
            lost_item_name = "lost_" + RandomHelper.random_string(3)
            web.athena_base_page.set_value_by_label("物品名稱", lost_item_name)
            web.athena_base_page.screenshot("And 輸入[物品名稱]")

        with allure.step("And 選擇[遺失日期]"):
            web.lost_management_page.select_date("遺失日期", "2025", "六月", "18").sleep(2)
            web.athena_base_page.screenshot("And 選擇[遺失日期]")

        with allure.step("And 輸入選擇[遺失者]"):
            web.lost_management_page.input_loser_name()
            web.athena_base_page.screenshot("And 輸入選擇[遺失者]")

        with allure.step("And 點擊[橘色磁碟片]進行儲存"):
            web.athena_base_page.click_toolbar_with_icon("save").sleep(1)
            web.athena_base_page.screenshot("And 點擊[橘色磁碟片]進行儲存")

        with allure.step("Then 顯示'儲存成功'提示"):
            web.athena_base_page.screenshot("顯示'儲存成功'提示")
            web.athena_base_page.assert_data(
                "儲存成功", web.tip_component.get_tip_text(), "儲存成功"
            )
            web.tip_component.click_ok()
            lost_item_code = web.lost_management_page.get_lost_item_data_from_dialog("code")
            web.share_panel_component.close_panel("編輯失物")

        with allure.step("And 驗證失物資料"):
            web.lost_management_page.search_lost_item(lost_item_code, "遺失")
            web.lost_management_page.click_first_row()
            web.athena_base_page.click_toolbar_with_icon("edit").sleep(2)
            web.lost_management_page.screenshot("And 驗證失物資料")
            web.lost_management_page.assert_data(
                "遺失日期",
                web.lost_management_page.get_lost_item_data_from_dialog("lostDate"),
                "2025/06/18",
            )
            web.lost_management_page.assert_data(
                "物品名稱",
                web.lost_management_page.get_lost_item_data_from_dialog("item"),
                lost_item_name,
            )
            web.lost_management_page.assert_data(
                "狀態", web.lost_management_page.get_lost_item_data_from_dialog("status"), "遺失"
            )

    @allure.story("單筆 - 從編輯失物視窗新增資料")
    @pytest.mark.xdist_group("lost_item")
    @pytest.mark.dependency(
        name="test_add_item_from_dialog", depends=["test_add_lost_item"], scope="session"
    )
    @pytest.mark.parametrize(
        "status, date, date_field",
        [("遺失", "遺失日期", "lostDate"), ("拾獲", "拾獲日期", "foundDate")],
    )
    def test_add_item_from_dialog(self, logged_in_driver, status, date, date_field):
        pages = [
            LostManagementPage,
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            AthenaBasePage,
        ]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        with allure.step("Given 使用者進入「失物管理」頁面"):
            web.header_component.expand_menu("接待").sleep(1)
            web.header_component.to_func_page("失物管理").sleep(1)
            web.athena_base_page.screenshot("Given 使用者進入「失物管理」頁面")

        with allure.step("When 點擊一筆遺失資料列"):
            web.athena_base_page.clear()
            web.athena_base_page.search()
            web.lost_management_page.click_first_row()
            web.athena_base_page.screenshot("When 點擊一筆遺失資料列")

        with allure.step("And 點擊[橘色筆]進行編輯"):
            web.athena_base_page.click_toolbar_with_icon("edit").sleep(2)
            web.athena_base_page.screenshot("And 點擊[橘色筆]進行編輯")

        with allure.step("And 點擊[橘色加號]進行新增"):
            web.athena_base_page.click_toolbar_with_icon("add", "編輯失物").sleep(1)
            web.athena_base_page.screenshot("And 點擊[橘色加號]進行新增")

        with allure.step(f"And 選擇[狀態]為<{status}>"):
            web.lost_management_page.select_status_in_dialog(status)
            web.athena_base_page.screenshot(f"And 選擇[狀態]為<{status}>")

        with allure.step("And 輸入[物品名稱]"):
            item_name = "item_" + RandomHelper.random_string(3)
            web.athena_base_page.set_value_by_label("物品名稱", item_name)
            web.athena_base_page.screenshot("And 輸入[物品名稱]")

        with allure.step("And 點擊[橘色磁碟片]進行儲存"):
            web.athena_base_page.click_toolbar_with_icon("save").sleep(1)
            web.athena_base_page.screenshot("And 點擊[橘色磁碟片]進行儲存")

        with allure.step("Then 顯示'儲存成功'提示"):
            web.athena_base_page.screenshot("顯示'儲存成功'提示")
            web.athena_base_page.assert_data(
                "儲存成功", web.tip_component.get_tip_text(), "儲存成功"
            )
            lost_item_code = web.lost_management_page.get_field_value_in_dialog("失物編號")
            web.tip_component.click_ok()
            web.share_panel_component.close_panel("編輯失物")

        with allure.step("And 驗證失物資料"):
            web.lost_management_page.search_lost_item(lost_item_code, status).sleep(1)
            web.lost_management_page.screenshot("And 驗證失物資料")
            today = datetime.now().strftime("%Y/%m/%d")
            web.lost_management_page.assert_data(
                date, web.lost_management_page.get_lost_item_data_from_page(date_field), today
            )
            web.lost_management_page.assert_data(
                "物品名稱", web.lost_management_page.get_lost_item_data_from_page("item"), item_name
            )
            web.lost_management_page.assert_data(
                "狀態",
                web.lost_management_page.get_lost_item_data_from_page("statusDisplay"),
                status,
            )

    @allure.story("單筆 - 遺失變成遺失已尋獲")
    @pytest.mark.xdist_group("lost_item")
    @pytest.mark.dependency(
        name="test_change_to_lost_and_found", depends=["test_add_item_from_dialog"], scope="session"
    )
    def test_change_to_lost_and_found(self, logged_in_driver):
        pages = [
            LostManagementPage,
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            AthenaBasePage,
        ]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        with allure.step("Given 使用者進入「失物管理」頁面"):
            web.header_component.expand_menu("接待").sleep(1)
            web.header_component.to_func_page("失物管理").sleep(1)
            web.athena_base_page.screenshot("Given 使用者進入「失物管理」頁面")

        with allure.step("When 選擇[狀態]為<遺失>"):
            web.lost_management_page.select_status_from_page("遺失")
            web.athena_base_page.screenshot("When 選擇[狀態]為<遺失>")

        with allure.step("And 點擊[藍色放大鏡]進行查詢"):
            web.athena_base_page.clear()
            web.athena_base_page.search()
            web.athena_base_page.screenshot("And 點擊[藍色放大鏡]進行查詢")

        with allure.step("And 點擊一筆遺失資料列"):
            lost_item_code = web.lost_management_page.get_lost_item_data_from_page("code")
            web.lost_management_page.click_first_row()
            web.athena_base_page.screenshot("And 點擊一筆遺失資料列")

        with allure.step("And 點擊[橘色筆]進行編輯"):
            web.athena_base_page.click_toolbar_with_icon("edit").sleep(2)
            web.athena_base_page.screenshot("And 點擊[橘色筆]進行編輯")

        with allure.step("And 於「編輯失物」視窗中選擇[狀態]為<遺失已尋獲>"):
            web.lost_management_page.select_status_in_dialog("遺失已尋獲").sleep(2)
            web.athena_base_page.screenshot("And 於「編輯失物」視窗中選擇[狀態]為<遺失已尋獲>")

        with allure.step("And 輸入[拾獲者]"):
            web.athena_base_page.set_value_by_label("拾獲者", "Jimmy")
            web.athena_base_page.screenshot("And 輸入[拾獲者]")

        with allure.step("And 點擊[橘色磁碟片]進行儲存"):
            web.athena_base_page.click_toolbar_with_icon("save").sleep(1)
            web.athena_base_page.screenshot("And 點擊[橘色磁碟片]進行儲存")

        with allure.step("Then 顯示'儲存成功'提示"):
            web.athena_base_page.screenshot("顯示'儲存成功'提示")
            web.athena_base_page.assert_data(
                "儲存成功", web.tip_component.get_tip_text(), "儲存成功"
            )
            web.tip_component.click_ok()
            web.share_panel_component.close_panel("編輯失物")

        with allure.step("And 驗證變更狀態成功"):
            web.lost_management_page.search_lost_item(lost_item_code, "遺失已尋獲").sleep(1)
            web.lost_management_page.screenshot("And 驗證變更狀態成功")
            today = datetime.now().strftime("%Y/%m/%d")
            web.lost_management_page.assert_data(
                "狀態",
                web.lost_management_page.get_lost_item_data_from_page("statusDisplay"),
                "遺失已尋獲",
            )
            web.lost_management_page.assert_data(
                "拾獲者", web.lost_management_page.get_lost_item_data_from_page("picker"), "Jimmy"
            )
            web.lost_management_page.assert_data(
                "拾獲日期",
                web.lost_management_page.get_lost_item_data_from_page("foundDate"),
                today,
            )

    @allure.story("單筆 - 遺失已尋獲變成領回")
    @pytest.mark.xdist_group("lost_item")
    @pytest.mark.dependency(
        name="test_lost_and_found_change_to_claim",
        depends=["test_change_to_lost_and_found"],
        scope="session",
    )
    def test_lost_and_found_change_to_claim(self, logged_in_driver):
        pages = [
            LostManagementPage,
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            AthenaBasePage,
        ]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        with allure.step("Given 使用者進入「失物管理」頁面"):
            web.header_component.expand_menu("接待").sleep(1)
            web.header_component.to_func_page("失物管理").sleep(1)
            web.athena_base_page.screenshot("Given 使用者進入「失物管理」頁面")

        with allure.step("When 選擇[狀態]為<遺失已尋獲>"):
            web.lost_management_page.select_status_from_page("遺失已尋獲")
            web.athena_base_page.screenshot("When 選擇[狀態]為<遺失已尋獲>")

        with allure.step("And 點擊[藍色放大鏡]進行查詢"):
            web.athena_base_page.clear()
            web.athena_base_page.search()
            web.athena_base_page.screenshot("And 點擊[藍色放大鏡]進行查詢")

        with allure.step("And 點擊一筆資料列"):
            lost_item_code = web.lost_management_page.get_lost_item_data_from_page("code")
            web.lost_management_page.click_first_row()
            web.athena_base_page.screenshot("And 點擊一筆資料列")

        with allure.step("And 點擊[橘色筆]進行編輯"):
            web.athena_base_page.click_toolbar_with_icon("edit").sleep(2)
            web.athena_base_page.screenshot("And 點擊[橘色筆]進行編輯")

        with allure.step("And 選擇[狀態]為<領回>"):
            web.lost_management_page.select_status_in_dialog("領回").sleep(2)
            web.athena_base_page.screenshot("And 選擇[狀態]為<領回>")

        with allure.step("And 選擇輸入[領回者]"):
            web.athena_base_page.set_value_by_label("領回者", "Bark")
            web.athena_base_page.screenshot("And 選擇輸入[領回者]")

        with allure.step("And 點擊[橘色磁碟片]進行儲存"):
            web.athena_base_page.click_toolbar_with_icon("save").sleep(1)
            web.athena_base_page.screenshot("And 點擊[橘色磁碟片]進行儲存")

        with allure.step("Then 顯示'儲存成功'提示"):
            web.athena_base_page.screenshot("顯示'儲存成功'提示")
            web.athena_base_page.assert_data(
                "儲存成功", web.tip_component.get_tip_text(), "儲存成功"
            )
            web.tip_component.click_ok()
            web.share_panel_component.close_panel("編輯失物")

        with allure.step("And 驗證變更狀態成功"):
            web.lost_management_page.search_lost_item(lost_item_code, "領回").sleep(1)
            web.athena_base_page.screenshot("And 驗證變更狀態成功")
            today = datetime.now().strftime("%Y/%m/%d")
            web.lost_management_page.assert_data(
                "狀態",
                web.lost_management_page.get_lost_item_data_from_page("statusDisplay"),
                "領回",
            )
            web.lost_management_page.assert_data(
                "領回者", web.lost_management_page.get_lost_item_data_from_page("recipient"), "Bark"
            )
            web.lost_management_page.assert_data(
                "領回日期",
                web.lost_management_page.get_lost_item_data_from_page("claimDate"),
                today,
            )

    @allure.story("單筆 - 領回變成拾獲")
    @pytest.mark.xdist_group("lost_item")
    @pytest.mark.dependency(
        name="test_claim_change_to_found",
        depends=["test_lost_and_found_change_to_claim"],
        scope="session",
    )
    def test_claim_change_to_found(self, logged_in_driver):
        pages = [
            LostManagementPage,
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            AthenaBasePage,
        ]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        with allure.step("Given 使用者進入「失物管理」頁面"):
            web.header_component.expand_menu("接待").sleep(1)
            web.header_component.to_func_page("失物管理").sleep(1)
            web.athena_base_page.screenshot("Given 使用者進入「失物管理」頁面")

        with allure.step("When 選擇[狀態]為<領回>"):
            web.lost_management_page.select_status_from_page("領回")
            web.athena_base_page.screenshot("When 選擇[狀態]為<領回>")

        with allure.step("And 點擊[藍色放大鏡]進行查詢"):
            web.athena_base_page.clear()
            web.athena_base_page.search()
            web.athena_base_page.screenshot("And 點擊[藍色放大鏡]進行查詢")

        with allure.step("And 點擊一筆資料列"):
            lost_item_code = web.lost_management_page.get_lost_item_data_from_page("code")
            picker = web.lost_management_page.get_lost_item_data_from_page("picker")
            found_date = web.lost_management_page.get_lost_item_data_from_page("foundDate")
            web.lost_management_page.click_first_row()
            web.athena_base_page.screenshot("And 點擊一筆資料列")

        with allure.step("And 點擊[橘色筆]進行編輯"):
            web.athena_base_page.click_toolbar_with_icon("edit").sleep(2)
            web.athena_base_page.screenshot("And 點擊[橘色筆]進行編輯")

        with allure.step("And 選擇[狀態]為<拾獲>"):
            web.lost_management_page.select_status_in_dialog("拾獲").sleep(2)
            lost_date_enabled = web.lost_management_page.date_field_enabled("遺失日期")
            loser_name_enabled = web.lost_management_page.loser_name_field_enabled()
            lost_remark_enabled = web.lost_management_page.label_enabled("遺失備註")
            web.athena_base_page.screenshot("And 選擇[狀態]為<拾獲>")

        with allure.step("And 點擊[橘色磁碟片]進行儲存"):
            web.athena_base_page.click_toolbar_with_icon("save").sleep(1)
            web.athena_base_page.screenshot("And 點擊[橘色磁碟片]進行儲存")

        with allure.step("Then 顯示'儲存成功'提示"):
            web.athena_base_page.screenshot("顯示'儲存成功'提示")
            web.athena_base_page.assert_data(
                "儲存成功", web.tip_component.get_tip_text(), "儲存成功"
            )
            web.tip_component.click_ok()
            web.share_panel_component.close_panel("編輯失物")

        with allure.step("And 驗證變更狀態成功"):
            web.lost_management_page.search_lost_item(lost_item_code, "拾獲").sleep(1)
            web.athena_base_page.screenshot("And 驗證變更狀態成功")
            web.lost_management_page.assert_data(
                "狀態",
                web.lost_management_page.get_lost_item_data_from_page("statusDisplay"),
                "拾獲",
            )
            web.lost_management_page.assert_data(
                "領回者被清空",
                web.lost_management_page.get_lost_item_data_from_page("recipient"),
                "",
            )
            web.lost_management_page.assert_data(
                "領回日期被清空",
                web.lost_management_page.get_lost_item_data_from_page("claimDate"),
                "",
            )
            web.lost_management_page.assert_data(
                "拾獲者保持原樣",
                web.lost_management_page.get_lost_item_data_from_page("picker"),
                picker,
            )
            web.lost_management_page.assert_data(
                "拾獲日期保持原樣",
                web.lost_management_page.get_lost_item_data_from_page("foundDate"),
                found_date,
            )
            web.lost_management_page.assert_data(
                "領回變成拾獲時，遺失日期可編輯", lost_date_enabled, True
            )
            web.lost_management_page.assert_data(
                "領回變成拾獲時，遺失者可編輯", loser_name_enabled, True
            )
            web.lost_management_page.assert_data(
                "領回變成拾獲時，遺失備註可編輯", lost_remark_enabled, True
            )

    @allure.story("多筆 - 拾獲變更為拾獲者領回")
    @pytest.mark.xdist_group("lost_item")
    @pytest.mark.dependency(
        name="test_change_to_picker_claim", depends=["test_claim_change_to_found"], scope="session"
    )
    def test_change_to_picker_claim(self, logged_in_driver):
        pages = [
            LostManagementPage,
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            AthenaBasePage,
        ]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        with allure.step("Given 使用者進入「失物管理」頁面"):
            web.header_component.expand_menu("接待").sleep(1)
            web.header_component.to_func_page("失物管理").sleep(1)
            web.athena_base_page.screenshot("Given 使用者進入「失物管理」頁面")

        with allure.step("When 選擇[狀態]為<拾獲>"):
            web.lost_management_page.select_status_from_page("拾獲")
            web.athena_base_page.screenshot("When 選擇[狀態]為<拾獲>")

        with allure.step("And 點擊[藍色放大鏡]進行查詢"):
            web.athena_base_page.clear()
            web.athena_base_page.search().sleep(1)
            web.athena_base_page.screenshot("And 點擊[藍色放大鏡]進行查詢")

        with allure.step("勾選多筆資料列"):
            lost_item_codes = []
            for row in range(0, 2):
                web.lost_management_page.click_check_box_by_row(row)
                lost_item_codes.append(
                    web.lost_management_page.get_lost_item_data_from_page("code", row)
                )
            web.athena_base_page.screenshot("勾選多筆資料列")

        with allure.step("點擊[拾獲者領回]"):
            web.athena_base_page.click_toolbar_item("拾獲者領回")
            web.athena_base_page.screenshot("點擊[拾獲者領回]")

        with allure.step("輸入[領回備註]"):
            claim_note = "claim note test"
            web.lost_management_page.input_claim_note(claim_note)
            web.athena_base_page.screenshot("輸入[領回備註]")

        with allure.step("And 點擊[橘色磁碟片]進行儲存"):
            web.athena_base_page.click_toolbar_with_icon("save").sleep(1)
            web.athena_base_page.screenshot("And 點擊[橘色磁碟片]進行儲存")

        with allure.step("Then 顯示'儲存成功'提示"):
            web.athena_base_page.screenshot("顯示'儲存成功'提示")
            web.athena_base_page.assert_data(
                "儲存成功", web.tip_component.get_tip_text(), "儲存成功"
            )
            web.tip_component.click_ok()
            web.share_panel_component.close_panel("拾獲者領回")

        with allure.step("And 驗證失物資料"):
            for code in lost_item_codes:
                web.lost_management_page.search_lost_item(code, "領回").sleep(1)
                web.athena_base_page.screenshot("And 驗證失物資料")
                today = datetime.now().strftime("%Y/%m/%d")
                web.lost_management_page.assert_data(
                    "狀態",
                    web.lost_management_page.get_lost_item_data_from_page("statusDisplay"),
                    "領回",
                )
                web.lost_management_page.assert_data(
                    "領回者",
                    web.lost_management_page.get_lost_item_data_from_page("recipient"),
                    web.lost_management_page.get_lost_item_data_from_page("picker"),
                )
                web.lost_management_page.assert_data(
                    "領回日期",
                    web.lost_management_page.get_lost_item_data_from_page("claimDate"),
                    today,
                )

                web.lost_management_page.click_first_row()
                web.athena_base_page.click_toolbar_with_icon("edit").sleep(2)
                web.lost_management_page.assert_data(
                    "領回備註",
                    web.lost_management_page.get_field_value_in_dialog("領回備註"),
                    claim_note,
                )
                web.share_panel_component.close_panel("編輯失物")

    @allure.story("新增一筆拾獲")
    @pytest.mark.xdist_group("found_item")
    @pytest.mark.dependency(name="test_add_found_item", scope="session")
    def test_add_found_item(self, logged_in_driver):
        pages = [
            LostManagementPage,
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            AthenaBasePage,
        ]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        with allure.step("Given 使用者進入「失物管理」頁面"):
            web.header_component.expand_menu("接待").sleep(1)
            web.header_component.to_func_page("失物管理").sleep(1)
            web.athena_base_page.screenshot("Given 使用者進入「失物管理」頁面")

        with allure.step("When 點擊[橘色加號]進行新增"):
            web.athena_base_page.click_toolbar_with_icon("add")
            web.athena_base_page.screenshot("When 點擊[橘色加號]進行新增")

        with allure.step("And 選擇[狀態]為<拾獲>"):
            web.lost_management_page.select_status_in_dialog("拾獲")
            web.athena_base_page.screenshot("And 選擇[狀態]為<拾獲>")

        with allure.step("And 輸入[物品名稱]"):
            found_item_name = "found_" + RandomHelper.random_string(3)
            web.athena_base_page.set_value_by_label("物品名稱", found_item_name)
            web.athena_base_page.screenshot("And 輸入[物品名稱]")

        with allure.step("And 選擇[拾獲日期]"):
            web.lost_management_page.select_date("拾獲日期", "2025", "六月", "18").sleep(2)
            web.athena_base_page.screenshot("And 選擇[拾獲日期]")

        with allure.step("And 選擇輸入[拾獲者]"):
            web.athena_base_page.set_value_by_label("拾獲者", "Jimmy")
            web.athena_base_page.screenshot("And 選擇輸入[拾獲者]")

        with allure.step("And 點擊[橘色磁碟片]進行儲存"):
            web.athena_base_page.click_toolbar_with_icon("save").sleep(1)
            web.athena_base_page.screenshot("And 點擊[橘色磁碟片]進行儲存")

        with allure.step("Then 顯示'儲存成功'提示"):
            web.athena_base_page.screenshot("顯示'儲存成功'提示")
            web.athena_base_page.assert_data(
                "儲存成功", web.tip_component.get_tip_text(), "儲存成功"
            )
            web.tip_component.click_ok()
            lost_item_code = web.lost_management_page.get_lost_item_data_from_dialog("code")
            web.share_panel_component.close_panel("編輯失物")

        with allure.step("And 驗證失物資料"):
            web.lost_management_page.search_lost_item(lost_item_code, "拾獲").sleep(1)
            web.athena_base_page.screenshot("And 驗證失物資料")
            web.lost_management_page.assert_data(
                "狀態",
                web.lost_management_page.get_lost_item_data_from_page("statusDisplay"),
                "拾獲",
            )
            web.lost_management_page.assert_data(
                "拾獲者", web.lost_management_page.get_lost_item_data_from_page("picker"), "Jimmy"
            )
            web.lost_management_page.assert_data(
                "拾獲日期",
                web.lost_management_page.get_lost_item_data_from_page("foundDate"),
                "2025/06/18",
            )
            web.lost_management_page.assert_data(
                "物品名稱",
                web.lost_management_page.get_lost_item_data_from_page("item"),
                found_item_name,
            )

    @allure.story("單筆 - 拾獲變成領回")
    @pytest.mark.xdist_group("found_item")
    @pytest.mark.dependency(
        name="test_found_change_to_claim", depends=["test_add_found_item"], scope="session"
    )
    def test_found_change_to_claim(self, logged_in_driver):
        pages = [
            LostManagementPage,
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            AthenaBasePage,
        ]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        with allure.step("Given 使用者進入「失物管理」頁面"):
            web.header_component.expand_menu("接待").sleep(1)
            web.header_component.to_func_page("失物管理").sleep(1)
            web.athena_base_page.screenshot("Given 使用者進入「失物管理」頁面")

        with allure.step("When 選擇[狀態]為<拾獲>"):
            web.lost_management_page.select_status_from_page("拾獲")
            web.athena_base_page.screenshot("When 選擇[狀態]為<拾獲>")

        with allure.step("And 點擊[藍色放大鏡]進行查詢"):
            web.athena_base_page.clear()
            web.athena_base_page.search()
            web.athena_base_page.screenshot("And 點擊[藍色放大鏡]進行查詢")

        with allure.step("And 點擊一筆拾獲資料列"):
            lost_item_code = web.lost_management_page.get_lost_item_data_from_page("code")
            web.lost_management_page.click_first_row()
            web.athena_base_page.screenshot("And 點擊一筆拾獲資料列")

        with allure.step("And 點擊[橘色筆]進行編輯"):
            web.athena_base_page.click_toolbar_with_icon("edit").sleep(2)
            web.athena_base_page.screenshot("And 點擊[橘色筆]進行編輯")

        with allure.step("And 於「編輯失物」視窗中選擇[狀態]為<領回>"):
            web.lost_management_page.select_status_in_dialog("領回").sleep(2)
            web.athena_base_page.screenshot("And 於「編輯失物」視窗中選擇[狀態]為<領回>")

        with allure.step("And 輸入[領回者]"):
            web.athena_base_page.set_value_by_label("領回者", "Bark")
            web.athena_base_page.screenshot("And 輸入[領回者]")

        with allure.step("And 點擊[橘色磁碟片]進行儲存"):
            web.athena_base_page.click_toolbar_with_icon("save").sleep(1)
            web.athena_base_page.screenshot("And 點擊[橘色磁碟片]進行儲存")

        with allure.step("Then 顯示'儲存成功'提示"):
            web.athena_base_page.screenshot("顯示'儲存成功'提示")
            web.athena_base_page.assert_data(
                "儲存成功", web.tip_component.get_tip_text(), "儲存成功"
            )
            web.tip_component.click_ok()
            web.share_panel_component.close_panel("編輯失物")

        with allure.step("And 驗證變更狀態成功"):
            web.lost_management_page.search_lost_item(lost_item_code, "領回").sleep(1)
            web.athena_base_page.screenshot("And 驗證變更狀態成功")
            today = datetime.now().strftime("%Y/%m/%d")
            web.lost_management_page.assert_data(
                "狀態",
                web.lost_management_page.get_lost_item_data_from_page("statusDisplay"),
                "領回",
            )
            web.lost_management_page.assert_data(
                "領回者", web.lost_management_page.get_lost_item_data_from_page("recipient"), "Bark"
            )
            web.lost_management_page.assert_data(
                "領回日期",
                web.lost_management_page.get_lost_item_data_from_page("claimDate"),
                today,
            )

    @allure.story("單筆 - 刪除")
    @pytest.mark.xdist_group("found_item")
    @pytest.mark.dependency(
        name="test_delete_lost_item", depends=["test_found_change_to_claim"], scope="session"
    )
    def test_delete_lost_item(self, logged_in_driver):
        pages = [
            LostManagementPage,
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            AthenaBasePage,
        ]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        with allure.step("Given 使用者進入「失物管理」頁面"):
            web.header_component.expand_menu("接待").sleep(1)
            web.header_component.to_func_page("失物管理").sleep(1)
            web.athena_base_page.screenshot("Given 使用者進入「失物管理」頁面")

        with allure.step("When 點擊一筆遺失資料列"):
            web.athena_base_page.clear()
            web.athena_base_page.search()
            lost_item_code = web.lost_management_page.get_lost_item_data_from_page("code")
            web.lost_management_page.click_first_row()
            web.athena_base_page.screenshot("When 點擊一筆遺失資料列")

        with allure.step("And 點擊[橘色筆]進行編輯"):
            web.athena_base_page.click_toolbar_with_icon("edit").sleep(2)
            web.athena_base_page.screenshot("And 點擊[橘色筆]進行編輯")

        with allure.step("And 點擊[橘色減號]進行刪除"):
            web.athena_base_page.click_toolbar_with_icon("remove").sleep(2)
            web.athena_base_page.screenshot("And 點擊[橘色減號]進行刪除")

        with allure.step("And 點擊[確定]"):
            web.tip_component.click_ok()
            web.athena_base_page.screenshot("And 點擊[確定]")

        with allure.step("Then 顯示[狀態]為<刪除>"):
            web.share_panel_component.close_panel("編輯失物")
            web.lost_management_page.search_lost_item(lost_item_code, "刪除").sleep(2)
            web.athena_base_page.screenshot("Then 顯示[狀態]為<刪除>")
            web.lost_management_page.assert_data(
                "狀態",
                web.lost_management_page.get_lost_item_data_from_page("statusDisplay"),
                "刪除",
            )

        with allure.step("And 驗證失物資料"):
            web.lost_management_page.click_first_row()
            web.athena_base_page.click_toolbar_with_icon("edit").sleep(2)
            web.athena_base_page.screenshot("And 驗證失物資料")

            web.athena_base_page.click_toolbar_item("照片", toolbar=2)
            web.athena_base_page.assert_data(
                "照片功能不可使用", web.tip_component.get_tip_text(), "領回和刪除不可執行照片上傳"
            )
            web.tip_component.click_ok()
            web.athena_base_page.assert_data(
                "刪除功能不可使用", web.lost_management_page.item_enabled("remove"), False
            )
            web.athena_base_page.assert_data(
                "儲存功能不可使用", web.lost_management_page.item_enabled("save"), False
            )

    @allure.story("查詢日期預設要帶滾房租日")
    def test_rent_day_in_search(self, logged_in_driver):
        pages = [
            LostManagementPage,
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            AthenaBasePage,
            ReservationPage,
        ]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        with allure.step("Given 使用者進入「失物管理」頁面"):
            rent_day = web.reservation_page.get_rent_day()
            rent_day = rent_day.replace("-", "/")
            web.header_component.expand_menu("接待").sleep(1)
            web.header_component.to_func_page("失物管理").sleep(1)
            web.athena_base_page.screenshot("Given 使用者進入「失物管理」頁面")

        with allure.step("When 檢查[查詢日期]"):
            rent_dat_in_lost = web.lost_management_page.get_rent_day()
            web.athena_base_page.screenshot("When 檢查[查詢日期]")

        with allure.step("Then 欄位預設帶入顯示滾房租日"):
            web.athena_base_page.screenshot("Then 欄位預設帶入顯示滾房租日")
            web.athena_base_page.assert_data("查詢日期為滾房租日期", rent_dat_in_lost, rent_day)
