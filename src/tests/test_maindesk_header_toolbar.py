import allure
import pytest
import names
from pages.base_page import BasePage
from pages.components.header_component import HeaderComponent
from pages.components.tip_component import TipComponent
from pages.components.share_panel_component import SharePanelComponent
from pages.components.todolist_edit_component import TodolistEditComponent
from pages.components.spare_parts_component import SparePartsComponent
from pages.maindesk_page import MaindeskPage
from pages.reservation_page import ReservationPage
from pages.dialogs.reservation_card_dialog import ReservationCardDialog
from tests.share_steps import ShareSteps
from tools.driver_helper import DriverHelper
from tools.random_helper import RandomHelper


@allure.feature("接待作業 - 綜合櫃檯")
class TestMaindeskHeaderToolbar:

    @allure.story("綜合櫃檯 - 新增一筆Walk In")
    def test_add_walkin(self):
        pages = [
            MaindeskPage,
            ReservationCardDialog,
            ReservationPage,
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            BasePage,
        ]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")

        with allure.step("Given 使用者進入「綜合櫃檯」頁面"):
            web.header_component.expand_menu("接待").sleep(1)
            web.header_component.to_func_page("綜合櫃檯").sleep(1)
            web.base_page.screenshot("Given 使用者進入「綜合櫃檯」頁面")

        with allure.step("When 選擇點擊欲安排入住變更狀態(類別)之房間"):
            web.maindesk_page.click_room_status_tag("VC").sleep(1)
            web.maindesk_page.click_floor("4F").sleep(1)
            room_number = web.maindesk_page.get_room_number()
            room_style = web.maindesk_page.get_room_style()
            web.maindesk_page.click_first_room().sleep(1)
            web.base_page.screenshot("When 選擇點擊欲安排入住變更狀態(類別)之房間")

        with allure.step("And 點擊[Walk In]"):
            web.maindesk_page.click_toolbar_button_roomdetail("Walk In").sleep(2)
            web.base_page.screenshot("And 點擊[Walk In]")

        with allure.step("And 填寫住客基本資料"):
            web.maindesk_page.click_edit_button("searchAltNam").sleep(2)
            first_name = names.get_first_name()
            last_name = names.get_last_name()
            web.reservation_page.create_guest(
                first_name, last_name, "Miss.", RandomHelper.generate_phone_mobile()
            )
            web.tip_component.click_ok().sleep(1)
            web.base_page.screenshot("And 填寫住客基本資料")

        with allure.step("And 點選房價代號"):
            web.maindesk_page.click_edit_button("searchRateCod").sleep(2)
            web.base_page.screenshot("And 點選房價代號")
            web.reservation_card_dialog.set_rate_code("現場訂房含早", 1).sleep(1)

        with allure.step("And 輸入預計入住天數"):
            web.maindesk_page.select_stay_days(2).sleep(1)
            web.base_page.screenshot("And 輸入預計入住天數")

        with allure.step("And 點擊[Check In]"):
            web.maindesk_page.click_toolbar_button_roomdetail("Check In").sleep(2)
            web.base_page.screenshot("And 點擊[Check In]")

        with allure.step("Then 顯示「儲存成功」提示"):
            ShareSteps.verify_save_success_tip(web)

        with allure.step("And 退出「櫃台入住」視窗"):
            web.share_panel_component.close_panel("櫃台入住").sleep(2)
            web.base_page.screenshot("And 退出「櫃台入住」視窗")

        with allure.step("Then 跳出房間細節視窗並進入訂房卡驗證內容"):
            web.maindesk_page.click_toolbar_button_roomdetail("訂房卡")
            web.base_page.screenshot("Then 跳出房間細節視窗並進入訂房卡驗證內容")

            web.base_page.assert_data(
                "狀態", web.reservation_card_dialog.get_text_in_tab("orderStatus"), "I: 今日到達"
            )
            web.base_page.assert_data(
                "房價代號", web.reservation_card_dialog.get_text_in_tab("rateCode"), "現場訂房含早"
            )
            web.base_page.assert_data(
                "計價房型", web.reservation_card_dialog.get_text_in_tab("useCode"), "STD: 標準客房1"
            )
            web.base_page.assert_data(
                "房租費用", web.reservation_card_dialog.get_text_in_tab("groupRentTotal"), "15,800"
            )
            web.base_page.close_panel()
            web.share_panel_component.close_panel("房間細節").sleep(2)

        with allure.step("And 驗證「綜合櫃台」頁面的房間內容"):
            web.maindesk_page.click_room_status_tag("VC").sleep(1)
            web.base_page.set_value_by_label("住客姓名", first_name + " " + last_name)
            web.base_page.search().sleep(1)
            web.base_page.screenshot("And 驗證「綜合櫃台」頁面的房間內容")

            web.base_page.assert_data(
                "住宿期間", web.maindesk_page.get_room_stay_days(), "01/05-01/07"
            )
            web.base_page.assert_data(
                "住客姓名", web.maindesk_page.get_room_guest_name(), first_name + " " + last_name
            )
            web.base_page.assert_data("使用房型", web.maindesk_page.get_room_style(), room_style)
            web.base_page.assert_data("房號", web.maindesk_page.get_room_number(), room_number)

    @allure.story("綜合櫃檯 - 新增關聯單號")
    @pytest.mark.xdist_group("test_maindesk_flow_a")
    @pytest.mark.dependency(name="test_add_link_nos_at_maindesk", scope="session")
    def test_add_link_nos_at_maindesk(self):
        pages = [
            MaindeskPage,
            ReservationCardDialog,
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            BasePage,
        ]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")

        with allure.step("Given 使用者進入「綜合櫃檯」頁面"):
            web.header_component.expand_menu("接待").sleep(1)
            web.header_component.to_func_page("綜合櫃檯").sleep(1)
            web.base_page.screenshot("Given 使用者進入「綜合櫃檯」頁面")

        with allure.step("When 選擇點擊已C/I之房間[方框]"):
            web.base_page.set_value_by_label("住客姓名", "Card Maindesk FLow A")
            web.base_page.search().sleep(1)
            web.maindesk_page.click_first_room().sleep(1)
            web.base_page.screenshot("When 選擇點擊已C/I之房間[方框]")

        with allure.step("And 於「房間細節」視窗點擊[關聯單號]"):
            web.maindesk_page.click_toolbar_button_roomdetail("關聯單號").sleep(1)
            web.base_page.screenshot("And 於「房間細節」視窗點擊[關聯單號]")

        with allure.step("And 點擊[綠色加號]新增關聯單號"):
            if web.reservation_card_dialog.get_link_nos_in_dialog():
                web.reservation_card_dialog.click_link_nos_remove()
                web.base_page.click_toolbar_with_icon("save").sleep(2)
                web.tip_component.click_ok()
            web.reservation_card_dialog.click_link_nos_add_button().sleep(1)
            web.base_page.screenshot("And 點擊[綠色加號]新增關聯單號")

        with allure.step("And 輸入欲查詢之[訂房卡號]、[房號]、[訂房名稱/團號]、[姓名]"):
            web.reservation_card_dialog.search_link_nos("00008236").sleep(1)
            web.base_page.screenshot("And 輸入欲查詢之[訂房卡號]")

        with allure.step("And 從查詢Table勾選欲建立關聯單號之訂房客"):
            web.reservation_card_dialog.check_link_nos().sleep(1)
            web.base_page.screenshot("And 從查詢Table勾選欲建立關聯單號之訂房客")

        with allure.step("And 點擊[確定]"):
            web.share_panel_component.click_panel_footer_btn("新增關聯單號", "確定").sleep(1)
            web.base_page.screenshot("And 點擊[確定]")

        with allure.step("And 點擊[橘色磁碟片]進行儲存"):
            web.base_page.click_toolbar_with_icon("save").sleep(1)
            web.base_page.screenshot("And 點擊[橘色磁碟片]進行儲存")

        with allure.step("Then 顯示'儲存成功'提示"):
            ShareSteps.verify_save_success_tip(web)
            web.share_panel_component.close_panel("關聯單號")

        with allure.step("And 驗證關聯單號資料"):
            web.maindesk_page.click_toolbar_button_roomdetail("關聯單號").sleep(1)
            web.base_page.screenshot("And 驗證關聯單號資料")
            web.base_page.assert_data(
                "關聯訂房卡資料",
                web.reservation_card_dialog.get_link_nos_row_data(2),
                [
                    "00008236",
                    "",
                    "Card Search Spare Parts",
                    "2024/01/05",
                    "2024/01/06",
                    "Card Search Spare Parts",
                ],
            )

    @allure.story("綜合櫃檯 - 改房價(計價房型)")
    @pytest.mark.xdist_group("test_maindesk_flow_a")
    @pytest.mark.dependency(
        name="test_change_room_type_at_maindesk",
        depends=["test_add_link_nos_at_maindesk"],
        scope="session",
    )
    def test_change_room_type_at_maindesk(self):
        pages = [
            MaindeskPage,
            ReservationCardDialog,
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            BasePage,
        ]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")

        with allure.step("Given 使用者從「綜合櫃檯」頁面進入「房間細節」視窗"):
            web.header_component.expand_menu("接待").sleep(1)
            web.header_component.to_func_page("綜合櫃檯").sleep(1)
            web.base_page.set_value_by_label("住客姓名", "Card Maindesk FLow A")
            web.base_page.search().sleep(1)
            web.maindesk_page.click_first_room().sleep(1)
            web.base_page.screenshot("Given 使用者從「綜合櫃檯」頁面進入「房間細節」視窗")

        with allure.step("When 點擊[改房價]"):
            web.maindesk_page.click_toolbar_button_roomdetail("改房價").sleep(2)
            web.base_page.screenshot("When 點擊[改房價]")

        with allure.step("And [計價房型]選擇"):
            current_room_type = web.maindesk_page.get_header_text("計價房型")
            if current_room_type == "STD":
                new_room_type = "DSU:豪華套房"
                rent = "8,900"
            else:
                new_room_type = "STD:標準客房1"
                rent = "7,900"
            web.maindesk_page.select_use_cod("計價房型", new_room_type).sleep(2)
            web.base_page.screenshot("And [計價房型]選擇")

        with allure.step("And 點擊[橘色磁碟片]進行儲存"):
            web.maindesk_page.click_save_rate_code_change()
            web.base_page.screenshot("And 點擊[橘色磁碟片]進行儲存")

        with allure.step("Then 顯示'儲存成功'提示"):
            ShareSteps.verify_save_success_tip(web)
            web.base_page.sleep(1)

        with allure.step("Then 跳出房間細節視窗並進入訂房卡驗證內容"):
            web.maindesk_page.click_toolbar_button_roomdetail("訂房卡")
            web.base_page.screenshot("Then 跳出房間細節視窗並進入訂房卡驗證內容")

            web.base_page.assert_data(
                "計價房型",
                web.reservation_card_dialog.get_text_in_tab("useCode").replace(" ", ""),
                new_room_type,
            )
            web.base_page.assert_data(
                "房租費用",
                web.reservation_card_dialog.get_text_in_tab("groupRentTotal").replace(" ", ""),
                rent,
            )
            web.base_page.close_panel()
            web.share_panel_component.close_panel("房間細節").sleep(2)

    @allure.story("綜合櫃檯 - 修改退房日")
    @pytest.mark.xdist_group("test_maindesk_flow_a")
    @pytest.mark.parametrize(
        "change_codate, date, codate, stay_period",
        [
            ("延長", "8", "2024/01/08 週一", "01/05-01/08"),
            ("縮短", "6", "2024/01/06 週六", "01/05-01/06"),
        ],
    )
    @pytest.mark.dependency(
        name="test_change_checkout_date_at_maindesk",
        depends=["test_change_room_type_at_maindesk"],
        scope="session",
    )
    def test_change_checkout_date_at_maindesk(self, change_codate, date, codate, stay_period):
        pages = [
            MaindeskPage,
            ReservationCardDialog,
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            BasePage,
        ]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")

        with allure.step("Given 使用者從「綜合櫃檯」頁面進入「房間細節」視窗"):
            web.header_component.expand_menu("接待").sleep(1)
            web.header_component.to_func_page("綜合櫃檯").sleep(1)
            web.base_page.set_value_by_label("住客姓名", "Card Maindesk FLow A")
            web.base_page.search().sleep(1)
            web.maindesk_page.click_first_room().sleep(1)
            web.base_page.screenshot("Given 使用者從「綜合櫃檯」頁面進入「房間細節」視窗")

        with allure.step("When 點擊[改退房日]"):
            web.maindesk_page.click_toolbar_button_roomdetail("改退房日").sleep(2)
            web.base_page.screenshot("When 點擊[改退房日]")

        with allure.step(f"And {change_codate}退房日"):
            web.maindesk_page.select_date_by_field("新退房日期", "2024", "一月", date).sleep(1)
            web.base_page.screenshot(f"And {change_codate}退房日")

        with allure.step("And 勾選房間"):
            web.maindesk_page.click_room_checkbox()
            web.base_page.screenshot("And 勾選房間")

        with allure.step("And 點擊[橘色磁碟片]進行儲存"):
            ShareSteps.click_btn_save(web)

        with allure.step("Then 顯示'修改退房日期成功'提示"):
            ShareSteps.verify_save_success_tip(web, "修改退房日期成功")
            ShareSteps.verify_save_success_tip(web, "請檢查房價")
            web.base_page.sleep(2)
            web.share_panel_component.close_panel("改退房日").sleep(2)

        with allure.step("Then 跳出房間細節視窗並進入訂房卡驗證內容"):
            web.maindesk_page.click_toolbar_button_roomdetail("訂房卡")
            web.base_page.screenshot("Then 跳出房間細節視窗並進入訂房卡驗證內容")

            room_type = web.reservation_card_dialog.get_text_in_tab("useCode")
            if change_codate == "延長":
                if "STD" in room_type:
                    rent = "23,700"
                else:
                    rent = "26,700"
            else:
                if "STD" in room_type:
                    rent = "7,900"
                else:
                    rent = "8,900"
            web.base_page.assert_data(
                "退房日期", web.reservation_card_dialog.get_text_in_tab("coDate"), codate
            )
            web.base_page.assert_data(
                "房租費用", web.reservation_card_dialog.get_text_in_tab("groupRentTotal"), rent
            )
            web.base_page.close_panel()
            web.share_panel_component.close_panel("房間細節").sleep(2)

        with allure.step("And 驗證「綜合櫃台」頁面的房間內容"):
            web.base_page.screenshot("And 驗證「綜合櫃台」頁面的房間內容")
            web.base_page.assert_data(
                "住宿期間", web.maindesk_page.get_room_stay_days(), stay_period
            )

    @allure.story("綜合櫃檯 - 改房價(房價)")
    @pytest.mark.xdist_group("test_maindesk_flow_a")
    @pytest.mark.dependency(
        name="test_change_room_price_at_maindesk",
        depends=["test_change_checkout_date_at_maindesk"],
        scope="session",
    )
    def test_change_room_price_at_maindesk(self):
        pages = [
            MaindeskPage,
            ReservationCardDialog,
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            BasePage,
        ]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")

        with allure.step("Given 使用者從「綜合櫃檯」頁面進入「房間細節」視窗"):
            web.header_component.expand_menu("接待").sleep(1)
            web.header_component.to_func_page("綜合櫃檯").sleep(1)
            web.base_page.set_value_by_label("住客姓名", "Card Maindesk FLow A")
            web.base_page.search().sleep(1)
            web.maindesk_page.click_first_room().sleep(1)
            web.base_page.screenshot("Given 使用者從「綜合櫃檯」頁面進入「房間細節」視窗")

        with allure.step("When 點擊[改房價]"):
            web.maindesk_page.click_toolbar_button_roomdetail("改房價").sleep(2)
            web.base_page.screenshot("When 點擊[改房價]")

        with allure.step("And [房價]輸入新金額"):
            rent = RandomHelper.random_number()
            web.maindesk_page.set_column_data("rent_amt", rent)
            web.base_page.screenshot("And [房價]輸入新金額")

        with allure.step("And 點擊[橘色磁碟片]進行儲存"):
            web.maindesk_page.click_save_rate_code_change()
            web.base_page.screenshot("And 點擊[橘色磁碟片]進行儲存")

        with allure.step("Then 顯示'儲存成功'提示"):
            ShareSteps.verify_save_success_tip(web)
            web.base_page.sleep(1)

        with allure.step("Then 跳出房間細節視窗並進入訂房卡驗證內容"):
            web.maindesk_page.click_toolbar_button_roomdetail("訂房卡")
            web.base_page.screenshot("Then 跳出房間細節視窗並進入訂房卡驗證內容")

            web.base_page.assert_data(
                "房租費用",
                web.reservation_card_dialog.get_text_in_tab("groupRentTotal"),
                f"{rent:,}",
            )
            web.base_page.close_panel()
            web.share_panel_component.close_panel("房間細節")

    @allure.story("綜合櫃檯 - 執行換房")
    @pytest.mark.xdist_group("test_maindesk_flow_b")
    @pytest.mark.parametrize("set_dirty, is_check", [(True, "保持勾選"), (False, "取消勾選")])
    @pytest.mark.dependency(name="test_change_room_set_dirty_at_maindesk", scope="session")
    def test_change_room_set_dirty_at_maindesk(self, set_dirty, is_check):
        pages = [
            MaindeskPage,
            ReservationCardDialog,
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            BasePage,
        ]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")

        with allure.step("Given 使用者從「綜合櫃檯」頁面進入「房間細節」視窗"):
            web.header_component.expand_menu("接待").sleep(1)
            web.header_component.to_func_page("綜合櫃檯").sleep(1)
            web.base_page.set_value_by_label("住客姓名", "Card Maindesk FLow B")
            web.base_page.search().sleep(1)
            original_room_number = web.maindesk_page.get_room_number()
            web.maindesk_page.click_first_room().sleep(1)
            web.base_page.screenshot("Given 使用者從「綜合櫃檯」頁面進入「房間細節」視窗")

        with allure.step("When 點擊[換房]"):
            web.maindesk_page.click_toolbar_button_roomdetail("換房").sleep(2)
            web.base_page.screenshot("When 點擊[換房]")

        with allure.step("And 輸入欲換房之房號"):
            if original_room_number == "205":
                target_room_number = "206"
            else:
                target_room_number = "205"
            web.base_page.clear_value_by_label("房號").sleep(1)
            web.base_page.set_value_by_label("房號", target_room_number)
            web.base_page.screenshot("And 輸入欲換房之房號")

        with allure.step(f"And {is_check}<換房後原房號設為髒房>"):
            if not set_dirty:
                web.maindesk_page.click_dirty_room_ck().sleep(1)
            web.base_page.screenshot(f"And {is_check}<換房後原房號設為髒房>")

        with allure.step("And 點擊[橘色磁碟片]進行儲存"):
            ShareSteps.click_btn_save(web)

        with allure.step("Then 顯示'換房成功'提示"):
            ShareSteps.verify_save_success_tip(web, "換房成功")

        with allure.step("And 跳出'是否執行改房價作業'提示"):
            web.tip_component.click_btn_by_text("取消").sleep(1)
            web.base_page.screenshot("And 跳出'是否執行改房價作業'提示")
            web.share_panel_component.close_panel("房間細節").sleep(2)

        with allure.step("And 驗證換房結果"):
            web.base_page.screenshot("And 驗證換房結果")
            web.base_page.assert_data(
                "新房號", web.maindesk_page.get_room_number(), target_room_number
            )

            # 回復原本房號的清掃狀態
            if set_dirty:
                web.base_page.clear()
                web.base_page.set_value_by_label("房號", original_room_number)
                web.base_page.search()
                web.maindesk_page.click_first_room().sleep(1)
                web.maindesk_page.click_toolbar_button_roomdetail("清掃房間").sleep(2)
                web.maindesk_page.click_toolbar_button_roomdetail("設定乾淨")
                web.tip_component.click_ok()

    @allure.story("綜合櫃檯 - 改房價(房價代號)")
    @pytest.mark.xdist_group("test_maindesk_flow_b")
    @pytest.mark.dependency(
        name="test_change_rate_code_at_maindesk",
        depends=["test_change_room_set_dirty_at_maindesk"],
        scope="session",
    )
    def test_change_rate_code_at_maindesk(self):
        pages = [
            MaindeskPage,
            ReservationCardDialog,
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            BasePage,
        ]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")

        with allure.step("Given 使用者從「綜合櫃檯」頁面進入「房間細節」視窗"):
            web.header_component.expand_menu("接待").sleep(1)
            web.header_component.to_func_page("綜合櫃檯").sleep(1)
            web.base_page.set_value_by_label("住客姓名", "Card Maindesk FLow B")
            web.base_page.search().sleep(1)
            web.maindesk_page.click_first_room().sleep(1)
            web.base_page.screenshot("Given 使用者從「綜合櫃檯」頁面進入「房間細節」視窗")

        with allure.step("When 點擊[改房價]"):
            web.maindesk_page.click_toolbar_button_roomdetail("改房價").sleep(2)
            web.base_page.screenshot("When 點擊[改房價]")

        with allure.step("And [房價代號]選擇"):
            rate_cod = web.maindesk_page.get_header_text("房價代號")
            web.maindesk_page.click_edit_button("ratecod_nam_button").sleep(2)
            if rate_cod == "NOBF":
                rate_cod = "現場訂房含早"
            else:
                rate_cod = "不含早"
            web.reservation_card_dialog.set_rate_code(rate_cod, 1).sleep(1)
            web.base_page.screenshot("And [房價代號]選擇")

        with allure.step("And 點擊[橘色磁碟片]進行儲存"):
            web.maindesk_page.click_save_rate_code_change()
            web.base_page.screenshot("And 點擊[橘色磁碟片]進行儲存")

        with allure.step("Then 顯示'儲存成功'提示"):
            ShareSteps.verify_save_success_tip(web)
            web.base_page.sleep(1)

        with allure.step("Then 跳出房間細節視窗並進入訂房卡驗證內容"):
            web.maindesk_page.click_toolbar_button_roomdetail("訂房卡")
            web.base_page.screenshot("Then 跳出房間細節視窗並進入訂房卡驗證內容")

            web.base_page.assert_data(
                "房價代號", web.reservation_card_dialog.get_text_in_tab("rateCode"), rate_cod
            )
            web.base_page.close_panel()
            web.share_panel_component.close_panel("房間細節").sleep(2)

    @allure.story("綜合櫃台 - 指定訂金綁定")
    @pytest.mark.xdist_group("test_maindesk_flow_b")
    @pytest.mark.dependency(
        name="test_assign_deposit_at_maindesk",
        depends=["test_change_rate_code_at_maindesk"],
        scope="session",
    )
    def test_assign_deposit_at_maindesk(self):
        pages = [
            MaindeskPage,
            ReservationCardDialog,
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            BasePage,
        ]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")

        with allure.step("Given 使用者從「綜合櫃檯」頁面進入「房間細節」視窗"):
            web.header_component.expand_menu("接待").sleep(1)
            web.header_component.to_func_page("綜合櫃檯").sleep(1)
            web.base_page.set_value_by_label("住客姓名", "Card Maindesk FLow B")
            web.base_page.search().sleep(1)
            web.maindesk_page.click_first_room().sleep(1)
            web.base_page.screenshot("Given 使用者從「綜合櫃檯」頁面進入「房間細節」視窗")

        with allure.step("When 點擊[指定訂金]"):
            web.maindesk_page.click_toolbar_button_roomdetail("指定訂金").sleep(2)
            web.base_page.screenshot("When 點擊[指定訂金]")

        with allure.step("And 填寫開班作業必填欄位"):
            ShareSteps.open_shift(web, "FO : 飯店櫃檯", "a", "autotest")
            web.base_page.screenshot("And 填寫開班作業必填欄位")

        with allure.step("And 選擇[訂金編號]"):
            deposit_nos = web.maindesk_page.get_specify_deposit_nos()
            if deposit_nos:
                web.maindesk_page.clear_specify_deposit()
                web.base_page.click_toolbar_with_icon("save").sleep(1)
                web.tip_component.click_ok().sleep(1)
                web.share_panel_component.close_panel("指定訂金").sleep(2)
                web.maindesk_page.click_toolbar_button_roomdetail("指定訂金").sleep(2)
            deposit_nos = "2204"
            web.maindesk_page.select_specify_deposit(deposit_nos).sleep(2)
            web.base_page.screenshot("And 選擇[訂金編號]")

        with allure.step("And 點擊[橘色磁碟片]進行儲存"):
            web.base_page.click_toolbar_with_icon("save").sleep(1)
            web.tip_component.click_ok().sleep(1)
            web.base_page.screenshot("And 點擊[橘色磁碟片]進行儲存")
            web.share_panel_component.close_panel("指定訂金").sleep(2)
            web.share_panel_component.close_panel("房間細節").sleep(2)

        with allure.step("And 訂金帳戶維護有正確資料"):
            web.header_component.expand_menu("出納").sleep(1)
            web.header_component.to_func_page("訂金帳戶維護").sleep(1)
            web.base_page.set_value_by_label("訂金編號", deposit_nos)
            web.base_page.search().sleep(1)
            web.base_page.screenshot("And 訂金帳戶維護有正確資料")

            web.base_page.assert_data(
                "訂金編號",
                web.base_page.get_field_text("deposit_mn_deposit_nos"),
                f"000000{deposit_nos}",
            )
            web.base_page.assert_data(
                "訂金狀態", web.base_page.get_field_text("deposit_mn_deposit_sta"), "N : 使用中"
            )
            web.base_page.assert_data(
                "單號", web.base_page.get_field_text("deposit_mn_link_nos") != "", True
            )

    @allure.story("綜合櫃台 - 新增櫃台備品")
    @pytest.mark.xdist_group("test_maindesk_flow_b")
    @pytest.mark.dependency(
        name="test_add_spare_parts_at_maindesk",
        depends=["test_assign_deposit_at_maindesk"],
        scope="session",
    )
    def test_add_spare_parts_at_maindesk(self):
        pages = [
            MaindeskPage,
            BasePage,
            SparePartsComponent,
            HeaderComponent,
            TipComponent,
            SharePanelComponent,
            TodolistEditComponent,
        ]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")

        with allure.step("Given 使用者從「綜合櫃檯」頁面進入「房間細節」視窗"):
            web.header_component.expand_menu("接待").sleep(1)
            web.header_component.to_func_page("綜合櫃檯").sleep(1)
            web.base_page.set_value_by_label("住客姓名", "Card Maindesk FLow B")
            web.base_page.search().sleep(1)
            web.maindesk_page.click_first_room().sleep(1)
            web.base_page.screenshot("Given 使用者從「綜合櫃檯」頁面進入「房間細節」視窗")

        with allure.step("When 點擊[櫃台備品]"):
            web.maindesk_page.click_toolbar_button_roomdetail("櫃台備品").sleep(2)
            web.base_page.screenshot("When 點擊[櫃台備品]")

        with allure.step("And 刪除舊櫃台備品"):
            while web.spare_parts_component.check_spare_parts_exist():
                web.spare_parts_component.click_remove_spare_parts()
                web.tip_component.click_ok()
            web.base_page.screenshot("And 刪除舊櫃台備品")

        with allure.step("And 新增櫃台備品並儲存"):
            web.spare_parts_component.click_add_spare_parts()
            web.spare_parts_component.create_spare_parts("熨斗")
            web.base_page.screenshot("And 新增櫃台備品並儲存")

        with allure.step("And 點擊[橘色磁碟片]進行儲存"):
            ShareSteps.click_btn_save(web)

        with allure.step("Then 顯示'儲存成功'提示"):
            ShareSteps.verify_save_success_tip(web, "儲存成功")
            web.base_page.sleep(1)
            web.share_panel_component.close_panel("櫃台備品")

        with allure.step("And 驗證櫃台備品資料"):
            web.maindesk_page.click_toolbar_button_roomdetail("櫃台備品").sleep(2)
            web.spare_parts_component.click_spare_parts_row()
            web.base_page.screenshot("And 驗證櫃台備品資料")
            info_list = [
                ("櫃台備品", "itemCode", "熨斗"),
                ("開始日期", "rentalStartDate", "2024/01/05"),
                ("結束日期", "checkoutDate", "2024/01/06"),
                ("數量", "amount", "1"),
                ("自動入帳", "appraiseIns", "N : 否"),
                ("入交辦", "todoInsert", "Y : 是"),
                ("處理部門", "todoDeptCode", "客務部-櫃台"),
                ("單價", "appraiseUnitAmount", "0"),
                ("單日小計", "appraiseItemAmount", "0"),
            ]
            for title, label, target in info_list:
                web.base_page.assert_data(
                    title, web.spare_parts_component.get_spare_parts_info(label), target
                )
            web.share_panel_component.close_panel("櫃台備品")

        with allure.step("And 驗證交辦事項"):
            web.maindesk_page.click_guest_function_roomdetail("todo_list").sleep(1)
            web.base_page.screenshot("And 驗證交辦事項")
            info_list = [
                ("處理狀態", "proc_sta", "N"),
                ("開始日期", "begin_dat", "2024/01/05"),
                ("結束日期", "end_dat", "2024/01/05"),
                ("處理部門", "dept_sna", "櫃台"),
                ("交辦內容", "todo_rmk", "熨斗 QTY:1"),
            ]
            for title, label, target in info_list:
                web.base_page.assert_data(
                    title, web.todolist_edit_component.get_todolist_info(label), target
                )

    @allure.story("綜合櫃台 - 設定指定公帳號")
    @pytest.mark.xdist_group("test_maindesk_flow_b")
    @pytest.mark.dependency(
        name="test_assign_public_account_at_maindesk",
        depends=["test_add_spare_parts_at_maindesk"],
        scope="session",
    )
    def test_assign_public_account_at_maindesk(self):
        pages = [MaindeskPage, BasePage, HeaderComponent, TipComponent, SharePanelComponent]
        web = DriverHelper.create_web_browser(pages, "pms", "reservation/PMS0110010")

        with allure.step("Given 使用者從「綜合櫃檯」頁面進入「房間細節」視窗"):
            web.header_component.expand_menu("接待").sleep(1)
            web.header_component.to_func_page("綜合櫃檯").sleep(1)
            web.base_page.set_value_by_label("住客姓名", "Card Maindesk FLow B")
            web.base_page.search().sleep(1)
            web.maindesk_page.click_first_room().sleep(1)
            web.base_page.screenshot("Given 使用者從「綜合櫃檯」頁面進入「房間細節」視窗")

        with allure.step("When 點擊[指定公帳號]"):
            room_exit = web.maindesk_page.is_master_room_exit()
            if room_exit:
                web.maindesk_page.click_toolbar_button_roomdetail("取消公帳號").sleep(1)
                web.tip_component.click_ok().sleep(1)
                web.tip_component.click_ok().sleep(1)
            web.maindesk_page.click_toolbar_button_roomdetail("指定公帳號").sleep(2)
            web.base_page.screenshot("When 點擊[指定公帳號]")

        with allure.step("And [公帳號]選擇"):
            web.maindesk_page.select_first_master_room("9").sleep(2)
            master_romm = web.maindesk_page.get_specify_master_room()
            web.base_page.screenshot("And [公帳號]選擇")

        with allure.step("And 點擊[橘色磁碟片]進行儲存"):
            web.base_page.click_toolbar_with_icon("save").sleep(1)
            web.base_page.screenshot("And 點擊[橘色磁碟片]進行儲存")

        with allure.step("Then 顯示'指定公帳號成功'提示"):
            ShareSteps.verify_save_success_tip(web, "指定公帳號成功")
            web.share_panel_component.close_panel("房間細節").sleep(2)

        with allure.step("And 房間細節顯示公帳號"):
            web.maindesk_page.click_first_room().sleep(1)
            web.base_page.screenshot("And 房間細節顯示公帳號")
            web.base_page.assert_data(
                "公帳號", web.maindesk_page.get_room_mn_text("公帳號"), master_romm
            )
