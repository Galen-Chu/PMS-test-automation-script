import allure
import pytest
from pages.athena_base_page import AthenaBasePage
from pages.co_list_page import CoListPage
from pages.components.header_component import HeaderComponent
from pages.components.tip_component import TipComponent
from pages.components.share_panel_component import SharePanelComponent
from tools.driver_helper import DriverHelper
from tools.test_data_helper import get_test_data
from tests.share_steps import ShareSteps


@allure.feature("出納作業 - C/O清單")
class TestCoList:

    @allure.story("C/O清單 - PM房轉帳到子房間")
    @pytest.mark.xdist_group("test_co_list_flow")
    @pytest.mark.dependency(name="test_transfer_from_pm_to_sub_room", scope="session")
    def test_transfer_from_pm_to_sub_room(self, logged_in_driver):
        # pylint: disable=too-many-locals  # acct_nos diff 需 before/after source/target set+amount
        data = get_test_data("test_co_list_flow", "transfer_to_pm")
        card_name = data["card_name"]
        room = data["room"]
        enter_item = data["enter_item"]
        enter_folio = data["enter_folio"]
        pm_room = data["pm_room"]
        pm_folio = data["pm_folio"]

        pages = [CoListPage, HeaderComponent, TipComponent, SharePanelComponent, AthenaBasePage]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        with allure.step("Given 使用者進入「C/O清單」頁面"):
            web.header_component.expand_menu("出納").sleep(1)
            web.header_component.to_func_page("C/O 清單").sleep(1)
            web.athena_base_page.screenshot("Given 使用者進入「C/O清單」頁面")

        with allure.step("Given 檢視目標帳夾款項（轉帳前）"):
            web.co_list_page.search_by_room_no(pm_room).sleep(1)
            web.co_list_page.click_card_row(pm_room).sleep(1)
            web.co_list_page.click_open_guest_account().sleep(1)
            if web.co_list_page.has_element(web.co_list_page.locator.dialog_shift):
                ShareSteps.open_shift(web, "FO : 飯店櫃檯", "a", "autotest")
                web.co_list_page.sleep(1)
            # 冪等清帳：歷輪轉入累積會踩消費 grid 分頁（>50 筆），before/after 讀取
            # 對稱性破（transfer_from_pm 8/25 全跑炸點）——起點恆乾淨使分頁不發生
            ShareSteps.ensure_folio_clean(web, pm_folio)
            target_before = web.co_list_page.get_folio_acct_nos(pm_folio)
            target_amount_before = web.co_list_page.get_folio_tab_amount(pm_folio)
            web.co_list_page.close_guest_account_dialog().sleep(1)
            web.athena_base_page.screenshot("Given 檢視目標帳夾款項（轉帳前）")

        with allure.step("Given 點擊欲進行設定之資料列"):
            web.co_list_page.search_by_guest_name(card_name).sleep(1)
            web.co_list_page.click_card_row(room).sleep(1)
            web.athena_base_page.screenshot("Given 點擊欲進行設定之資料列")

        with allure.step("Given 點擊[住客帳維護]"):
            web.co_list_page.click_open_guest_account().sleep(1)
            # 未開班時自動彈開班 dialog（session 級；實測新 session 多需重開）
            if web.co_list_page.has_element(web.co_list_page.locator.dialog_shift):
                ShareSteps.open_shift(web, "FO : 飯店櫃檯", "a", "autotest")
                web.co_list_page.sleep(1)
            ShareSteps.ensure_account_open(web)
            # 冪等清帳（同目標段理由）：來源殘留會使條件式入帳跳過 + 分頁風險
            ShareSteps.ensure_folio_clean(web, enter_folio)
            web.athena_base_page.screenshot("Given 點擊[住客帳維護]")

        with allure.step("Given 條件式入帳並讀取來源帳夾（轉帳前）"):
            # 條件式入帳：folio 有「正消費」就不入——判斷排除訂金（訂金使
            # get_folio_acct_nos 恆非空，誤判有帳跳過入帳致轉帳無標的；
            # ensure_folio_clean 清光正消費後訂金誤判必現，343 #463 同款教訓）；
            # acct_nos diff 追蹤轉出筆（取代金額守恆）
            consumable = web.co_list_page.get_folio_consumable_acct_nos(enter_folio)
            source_before = web.co_list_page.get_folio_acct_nos(enter_folio)
            if not consumable:
                web.co_list_page.enter_consumption(enter_item, enter_folio).sleep(1)
                source_before = web.co_list_page.get_folio_acct_nos(enter_folio)
            source_amount_before = web.co_list_page.get_folio_tab_amount(enter_folio)
            web.athena_base_page.screenshot("Given 條件式入帳並讀取來源帳夾（轉帳前）")

        with allure.step("When 點擊[轉帳]"):
            web.co_list_page.click_open_transfer_item().sleep(1)
            web.athena_base_page.screenshot("When 點擊[轉帳]")

        with allure.step("And 「轉帳項目選擇」視窗勾選消費資料列"):
            web.co_list_page.check_transfer_item_first().sleep(0.5)
            web.athena_base_page.screenshot("And 「轉帳項目選擇」視窗勾選消費資料列")

        with allure.step("And 點擊[轉帳]"):
            web.co_list_page.click_open_transfer_folio().sleep(1)
            web.athena_base_page.screenshot("And 點擊[轉帳]")

        with allure.step("And 「轉帳帳夾選擇」視窗勾選[相同訂房卡]"):
            web.co_list_page.click_transfer_target_type("相同訂房卡").sleep(0.5)
            web.athena_base_page.screenshot("And 「轉帳帳夾選擇」視窗勾選[相同訂房卡]")

        with allure.step("And 點擊住客資料列"):
            web.co_list_page.click_transfer_target_room(pm_room).sleep(1)
            web.athena_base_page.screenshot("And 點擊住客資料列")

        with allure.step("And 點擊帳夾資料列"):
            web.co_list_page.click_transfer_target_folio(pm_folio).sleep(0.5)
            web.athena_base_page.screenshot("And 點擊帳夾資料列")

        with allure.step("And 點擊[轉帳]"):
            web.co_list_page.click_confirm_transfer().sleep(1)
            web.athena_base_page.screenshot("And 點擊[轉帳]")

        with allure.step("Then 顯示轉帳成功!提示"):
            web.athena_base_page.wait_visible(web.tip_component.locator.btn_alert_ok)
            tip_text = web.tip_component.get_tip_text()
            web.athena_base_page.assert_data("轉帳提示", tip_text, "轉帳成功!")
            web.athena_base_page.screenshot("Then 顯示轉帳成功!提示")
            web.tip_component.click_ok().sleep(1)
            # 清理：轉帳項目選擇 dialog 不自動關，關掉 folio tab 才會刷新
            web.co_list_page.close_transfer_item_dialog().sleep(1)

        with allure.step("Then 來源帳夾消費款項已轉出"):
            source_after = web.co_list_page.get_folio_acct_nos(enter_folio)
            source_amount_after = web.co_list_page.get_folio_tab_amount(enter_folio)
            web.athena_base_page.screenshot("Then 來源帳夾消費款項已轉出")

        with allure.step("Then 目標帳夾頁籤新增轉入之消費款項"):
            web.co_list_page.close_guest_account_dialog().sleep(1)
            web.co_list_page.search_by_room_no(pm_room).sleep(1)
            web.co_list_page.click_card_row(pm_room).sleep(1)
            web.co_list_page.click_open_guest_account().sleep(1)
            target_after = web.co_list_page.get_folio_acct_nos(pm_folio)
            target_amount_after = web.co_list_page.get_folio_tab_amount(pm_folio)
            # 轉帳跨帳戶產生新 acct_nos（不保留來源號）：驗數量各 1 + 金額守恆
            web.athena_base_page.assert_data("來源移出一筆", len(source_before - source_after), 1)
            web.athena_base_page.assert_data("目標移入一筆", len(target_after - target_before), 1)
            web.athena_base_page.assert_data(
                "轉帳金額守恆",
                source_amount_before - source_amount_after,
                target_amount_after - target_amount_before,
            )
            web.athena_base_page.screenshot("Then 目標帳夾頁籤新增轉入之消費款項")

    @allure.story("C/O清單 - 轉帳到PM房")
    @pytest.mark.xdist_group("test_co_list_flow")
    @pytest.mark.dependency(name="test_transfer_to_pm_room", scope="session")
    def test_transfer_to_pm_room(self, logged_in_driver):
        # pylint: disable=too-many-locals  # transfer amount verify needs before/transfer/after
        data = get_test_data("test_co_list_flow", "transfer_from_sub")
        card_name = data["card_name"]
        room = data["room"]
        enter_item = data["enter_item"]
        enter_folio = data["enter_folio"]
        transfer_folio = data["transfer_folio"]
        pm_room = data["pm_room"]
        pm_folio = data["pm_folio"]

        pages = [CoListPage, HeaderComponent, TipComponent, SharePanelComponent, AthenaBasePage]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        with allure.step("Given 使用者進入「C/O清單」頁面"):
            web.header_component.expand_menu("出納").sleep(1)
            web.header_component.to_func_page("C/O 清單").sleep(1)
            web.athena_base_page.screenshot("Given 使用者進入「C/O清單」頁面")

        with allure.step("Given 檢視目標帳夾款項（轉帳前）"):
            web.co_list_page.search_by_room_no(pm_room).sleep(1)
            web.co_list_page.click_card_row(pm_room).sleep(1)
            web.co_list_page.click_open_guest_account().sleep(1)
            # 首次開住客帳維護偵測開班（session 級，開過後續不彈）
            if web.co_list_page.has_element(web.co_list_page.locator.dialog_shift):
                ShareSteps.open_shift(web, "FO : 飯店櫃檯", "a", "autotest")
                web.co_list_page.sleep(1)
            # 目標端冪等：同組 checkout 族會把 9015 結帳關帳，轉帳入帳要求開帳狀態
            ShareSteps.ensure_account_open(web)
            # 冪等清帳：歷輪轉入累積會踩消費 grid 分頁（>50 筆）——起點恆乾淨使
            # 分頁不發生（同 transfer_from_pm_to_sub_room 理由）
            ShareSteps.ensure_folio_clean(web, pm_folio)
            target_before = web.co_list_page.get_folio_acct_nos(pm_folio)
            target_amount_before = web.co_list_page.get_folio_tab_amount(pm_folio)
            web.co_list_page.close_guest_account_dialog().sleep(1)
            web.athena_base_page.screenshot("Given 檢視目標帳夾款項（轉帳前）")

        with allure.step("Given 點擊欲進行設定之資料列"):
            web.co_list_page.search_by_guest_name(card_name).sleep(1)
            web.co_list_page.click_card_row(room).sleep(1)
            web.athena_base_page.screenshot("Given 點擊欲進行設定之資料列")

        with allure.step("Given 點擊[住客帳維護]"):
            web.co_list_page.click_open_guest_account().sleep(1)
            # 開班為 session 級，目標帳戶段已開則不彈（保留偵測為防禦）
            if web.co_list_page.has_element(web.co_list_page.locator.dialog_shift):
                ShareSteps.open_shift(web, "FO : 飯店櫃檯", "a", "autotest")
                web.co_list_page.sleep(1)
            ShareSteps.ensure_account_open(web)
            # 冪等清帳（同目標段理由）：325 為轉帳來源累積制卡
            ShareSteps.ensure_folio_clean(web, enter_folio)
            web.athena_base_page.screenshot("Given 點擊[住客帳維護]")

        with allure.step("Given 條件式入帳並讀取來源帳夾（轉帳前）"):
            # 條件式入帳：folio 有「正消費」就不入——判斷排除訂金（訂金使
            # get_folio_acct_nos 恆非空，誤判有帳跳過入帳致轉帳無標的；
            # ensure_folio_clean 清光正消費後訂金誤判必現，343 #463 同款教訓）；
            # acct_nos diff 追蹤轉出筆（取代金額守恆）
            consumable = web.co_list_page.get_folio_consumable_acct_nos(enter_folio)
            source_before = web.co_list_page.get_folio_acct_nos(enter_folio)
            if not consumable:
                web.co_list_page.enter_consumption(enter_item, enter_folio).sleep(1)
                source_before = web.co_list_page.get_folio_acct_nos(enter_folio)
            source_amount_before = web.co_list_page.get_folio_tab_amount(enter_folio)
            web.athena_base_page.screenshot("Given 條件式入帳並讀取來源帳夾（轉帳前）")

        with allure.step("When 點擊[轉帳]"):
            web.co_list_page.click_open_transfer_item().sleep(1)
            web.athena_base_page.screenshot("When 點擊[轉帳]")

        with allure.step("And 「轉帳項目選擇」視窗勾選消費資料列"):
            # 住客房（多 folio）需先選帳夾 grid 才載入消費；PM房（單 folio）預設帶入免選
            web.co_list_page.select_transfer_item_folio(transfer_folio).sleep(0.5)
            web.co_list_page.check_transfer_item_first().sleep(0.5)
            web.athena_base_page.screenshot("And 「轉帳項目選擇」視窗勾選消費資料列")

        with allure.step("And 點擊[轉帳]"):
            web.co_list_page.click_open_transfer_folio().sleep(1)
            web.athena_base_page.screenshot("And 點擊[轉帳]")

        with allure.step("And 「轉帳帳夾選擇」視窗勾選[相同訂房卡]"):
            web.co_list_page.click_transfer_target_type("相同訂房卡").sleep(0.5)
            web.athena_base_page.screenshot("And 「轉帳帳夾選擇」視窗勾選[相同訂房卡]")

        with allure.step("And 點擊住客資料列"):
            web.co_list_page.click_transfer_target_room(pm_room).sleep(1)
            web.athena_base_page.screenshot("And 點擊住客資料列")

        with allure.step("And 點擊帳夾資料列"):
            web.co_list_page.click_transfer_target_folio(pm_folio).sleep(0.5)
            web.athena_base_page.screenshot("And 點擊帳夾資料列")

        with allure.step("And 點擊[轉帳]"):
            web.co_list_page.click_confirm_transfer().sleep(1)
            web.athena_base_page.screenshot("And 點擊[轉帳]")

        with allure.step("Then 顯示轉帳成功!提示"):
            web.athena_base_page.wait_visible(web.tip_component.locator.btn_alert_ok)
            tip_text = web.tip_component.get_tip_text()
            web.athena_base_page.assert_data("轉帳提示", tip_text, "轉帳成功!")
            web.athena_base_page.screenshot("Then 顯示轉帳成功!提示")
            web.tip_component.click_ok().sleep(1)
            # 清理：轉帳項目選擇 dialog 不自動關，關掉 folio tab 才會刷新
            web.co_list_page.close_transfer_item_dialog().sleep(1)

        with allure.step("Then 來源帳夾消費款項已轉出"):
            source_after = web.co_list_page.get_folio_acct_nos(enter_folio)
            source_amount_after = web.co_list_page.get_folio_tab_amount(enter_folio)
            web.athena_base_page.screenshot("Then 來源帳夾消費款項已轉出")

        with allure.step("Then 目標帳夾頁籤新增轉入之消費款項"):
            web.co_list_page.close_guest_account_dialog().sleep(1)
            web.co_list_page.search_by_room_no(pm_room).sleep(1)
            web.co_list_page.click_card_row(pm_room).sleep(1)
            web.co_list_page.click_open_guest_account().sleep(1)
            target_after = web.co_list_page.get_folio_acct_nos(pm_folio)
            target_amount_after = web.co_list_page.get_folio_tab_amount(pm_folio)
            # 轉帳跨帳戶產生新 acct_nos（不保留來源號）：驗數量各 1 + 金額守恆
            web.athena_base_page.assert_data("來源移出一筆", len(source_before - source_after), 1)
            web.athena_base_page.assert_data("目標移入一筆", len(target_after - target_before), 1)
            web.athena_base_page.assert_data(
                "轉帳金額守恆",
                source_amount_before - source_amount_after,
                target_amount_after - target_amount_before,
            )
            web.athena_base_page.screenshot("Then 目標帳夾頁籤新增轉入之消費款項")

    @allure.story("C/O清單 - 轉帳到其他房號")
    @pytest.mark.xdist_group("test_co_list_flow")
    @pytest.mark.dependency(name="test_transfer_to_other_room", scope="session")
    def test_transfer_to_other_room(self, logged_in_driver):
        # pylint: disable=too-many-locals  # transfer amount verify needs before/transfer/after
        data = get_test_data("test_co_list_flow", "transfer_to_other_room")
        card_name = data["card_name"]
        room = data["room"]
        enter_item = data["enter_item"]
        enter_folio = data["enter_folio"]
        transfer_folio = data["transfer_folio"]
        target_type = data["target_type"]
        pm_room = data["pm_room"]
        pm_folio = data["pm_folio"]

        pages = [CoListPage, HeaderComponent, TipComponent, SharePanelComponent, AthenaBasePage]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        with allure.step("Given 使用者進入「C/O清單」頁面"):
            web.header_component.expand_menu("出納").sleep(1)
            web.header_component.to_func_page("C/O 清單").sleep(1)
            web.athena_base_page.screenshot("Given 使用者進入「C/O清單」頁面")

        with allure.step("Given 檢視目標帳夾款項（轉帳前）"):
            web.co_list_page.search_by_room_no(pm_room).sleep(1)
            web.co_list_page.click_card_row(pm_room).sleep(1)
            web.co_list_page.click_open_guest_account().sleep(1)
            # 首次開住客帳維護偵測開班（session 級，開過後續不彈）
            if web.co_list_page.has_element(web.co_list_page.locator.dialog_shift):
                ShareSteps.open_shift(web, "FO : 飯店櫃檯", "a", "autotest")
                web.co_list_page.sleep(1)
            # 冪等清帳：歷輪轉入累積會踩消費 grid 分頁（>50 筆）——起點恆乾淨使
            # 分頁不發生（同 transfer_from_pm_to_sub_room 理由）
            ShareSteps.ensure_folio_clean(web, pm_folio)
            target_before = web.co_list_page.get_folio_acct_nos(pm_folio)
            target_amount_before = web.co_list_page.get_folio_tab_amount(pm_folio)
            web.co_list_page.close_guest_account_dialog().sleep(1)
            web.athena_base_page.screenshot("Given 檢視目標帳夾款項（轉帳前）")

        with allure.step("Given 點擊欲進行設定之資料列"):
            web.co_list_page.search_by_guest_name(card_name).sleep(1)
            web.co_list_page.click_card_row(room).sleep(1)
            web.athena_base_page.screenshot("Given 點擊欲進行設定之資料列")

        with allure.step("Given 點擊[住客帳維護]"):
            web.co_list_page.click_open_guest_account().sleep(1)
            # 開班為 session 級，目標帳戶段已開則不彈（保留偵測為防禦）
            if web.co_list_page.has_element(web.co_list_page.locator.dialog_shift):
                ShareSteps.open_shift(web, "FO : 飯店櫃檯", "a", "autotest")
                web.co_list_page.sleep(1)
            # 冪等清帳（同目標段理由）：325 為轉帳來源累積制卡
            ShareSteps.ensure_folio_clean(web, enter_folio)
            web.athena_base_page.screenshot("Given 點擊[住客帳維護]")

        with allure.step("Given 條件式入帳並讀取來源帳夾（轉帳前）"):
            # 條件式入帳：folio 有「正消費」就不入——判斷排除訂金（訂金使
            # get_folio_acct_nos 恆非空，誤判有帳跳過入帳致轉帳無標的；
            # ensure_folio_clean 清光正消費後訂金誤判必現，343 #463 同款教訓）；
            # acct_nos diff 追蹤轉出筆（取代金額守恆）
            consumable = web.co_list_page.get_folio_consumable_acct_nos(enter_folio)
            source_before = web.co_list_page.get_folio_acct_nos(enter_folio)
            if not consumable:
                web.co_list_page.enter_consumption(enter_item, enter_folio).sleep(1)
                source_before = web.co_list_page.get_folio_acct_nos(enter_folio)
            source_amount_before = web.co_list_page.get_folio_tab_amount(enter_folio)
            web.athena_base_page.screenshot("Given 條件式入帳並讀取來源帳夾（轉帳前）")

        with allure.step("When 點擊[轉帳]"):
            web.co_list_page.click_open_transfer_item().sleep(1)
            web.athena_base_page.screenshot("When 點擊[轉帳]")

        with allure.step("And 「轉帳項目選擇」視窗勾選消費資料列"):
            # 住客房（多 folio）需先選帳夾 grid 才載入消費；PM房（單 folio）預設帶入免選
            web.co_list_page.select_transfer_item_folio(transfer_folio).sleep(0.5)
            web.co_list_page.check_transfer_item_first().sleep(0.5)
            web.athena_base_page.screenshot("And 「轉帳項目選擇」視窗勾選消費資料列")

        with allure.step("And 點擊[轉帳]"):
            web.co_list_page.click_open_transfer_folio().sleep(1)
            web.athena_base_page.screenshot("And 點擊[轉帳]")

        with allure.step("And 「轉帳帳夾選擇」視窗勾選[全部房號]"):
            web.co_list_page.click_transfer_target_type(target_type).sleep(0.5)
            web.athena_base_page.screenshot("And 「轉帳帳夾選擇」視窗勾選[全部房號]")

        with allure.step("And 點擊住客資料列"):
            web.co_list_page.click_transfer_target_room(pm_room).sleep(1)
            web.athena_base_page.screenshot("And 點擊住客資料列")

        with allure.step("And 點擊帳夾資料列"):
            web.co_list_page.click_transfer_target_folio(pm_folio).sleep(0.5)
            web.athena_base_page.screenshot("And 點擊帳夾資料列")

        with allure.step("And 點擊[轉帳]"):
            web.co_list_page.click_confirm_transfer().sleep(1)
            web.athena_base_page.screenshot("And 點擊[轉帳]")

        with allure.step("Then 顯示轉帳成功!提示"):
            web.athena_base_page.wait_visible(web.tip_component.locator.btn_alert_ok)
            tip_text = web.tip_component.get_tip_text()
            web.athena_base_page.assert_data("轉帳提示", tip_text, "轉帳成功!")
            web.athena_base_page.screenshot("Then 顯示轉帳成功!提示")
            web.tip_component.click_ok().sleep(1)
            # 清理：轉帳項目選擇 dialog 不自動關，關掉 folio tab 才會刷新
            web.co_list_page.close_transfer_item_dialog().sleep(1)

        with allure.step("Then 來源帳夾消費款項已轉出"):
            source_after = web.co_list_page.get_folio_acct_nos(enter_folio)
            source_amount_after = web.co_list_page.get_folio_tab_amount(enter_folio)
            web.athena_base_page.screenshot("Then 來源帳夾消費款項已轉出")

        with allure.step("Then 目標帳夾頁籤新增轉入之消費款項"):
            web.co_list_page.close_guest_account_dialog().sleep(1)
            web.co_list_page.search_by_room_no(pm_room).sleep(1)
            web.co_list_page.click_card_row(pm_room).sleep(1)
            web.co_list_page.click_open_guest_account().sleep(1)
            target_after = web.co_list_page.get_folio_acct_nos(pm_folio)
            target_amount_after = web.co_list_page.get_folio_tab_amount(pm_folio)
            # 轉帳跨帳戶產生新 acct_nos（不保留來源號）：驗數量各 1 + 金額守恆
            web.athena_base_page.assert_data("來源移出一筆", len(source_before - source_after), 1)
            web.athena_base_page.assert_data("目標移入一筆", len(target_after - target_before), 1)
            web.athena_base_page.assert_data(
                "轉帳金額守恆",
                source_amount_before - source_amount_after,
                target_amount_after - target_amount_before,
            )
            web.athena_base_page.screenshot("Then 目標帳夾頁籤新增轉入之消費款項")

    @allure.story("C/O清單 - 轉帳到現金帳")
    @pytest.mark.xdist_group("test_co_list_flow")
    @pytest.mark.dependency(name="test_transfer_to_cash", scope="session")
    def test_transfer_to_cash(self, logged_in_driver):
        # pylint: disable=too-many-locals  # transfer amount verify needs before/transfer/after
        data = get_test_data("test_co_list_flow", "transfer_to_cash")
        card_name = data["card_name"]
        room = data["room"]
        enter_item = data["enter_item"]
        enter_folio = data["enter_folio"]
        transfer_folio = data["transfer_folio"]
        target_type = data["target_type"]
        room_filter = data["room_filter"]
        pm_room = data["pm_room"]
        pm_folio = data["pm_folio"]

        pages = [CoListPage, HeaderComponent, TipComponent, SharePanelComponent, AthenaBasePage]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        with allure.step("Given 使用者進入「C/O清單」頁面"):
            web.header_component.expand_menu("出納").sleep(1)
            web.header_component.to_func_page("C/O 清單").sleep(1)
            web.athena_base_page.screenshot("Given 使用者進入「C/O清單」頁面")

        with allure.step("Given 檢視目標帳夾款項（轉帳前）"):
            web.co_list_page.search_by_room_no(pm_room).sleep(1)
            web.co_list_page.click_card_row(pm_room).sleep(1)
            web.co_list_page.click_open_guest_account().sleep(1)
            # 首次開住客帳維護偵測開班（session 級，開過後續不彈）
            if web.co_list_page.has_element(web.co_list_page.locator.dialog_shift):
                ShareSteps.open_shift(web, "FO : 飯店櫃檯", "a", "autotest")
                web.co_list_page.sleep(1)
            # 冪等清帳：歷輪轉入累積會踩消費 grid 分頁（>50 筆）——起點恆乾淨使
            # 分頁不發生（同 transfer_from_pm_to_sub_room 理由；現金帳註銷行為同住客帳）
            ShareSteps.ensure_folio_clean(web, pm_folio)
            target_before = web.co_list_page.get_folio_acct_nos(pm_folio)
            target_amount_before = web.co_list_page.get_folio_tab_amount(pm_folio)
            web.co_list_page.close_guest_account_dialog().sleep(1)
            web.athena_base_page.screenshot("Given 檢視目標帳夾款項（轉帳前）")

        with allure.step("Given 點擊欲進行設定之資料列"):
            web.co_list_page.search_by_guest_name(card_name).sleep(1)
            web.co_list_page.click_card_row(room).sleep(1)
            web.athena_base_page.screenshot("Given 點擊欲進行設定之資料列")

        with allure.step("Given 點擊[住客帳維護]"):
            web.co_list_page.click_open_guest_account().sleep(1)
            # 開班為 session 級，目標帳戶段已開則不彈（保留偵測為防禦）
            if web.co_list_page.has_element(web.co_list_page.locator.dialog_shift):
                ShareSteps.open_shift(web, "FO : 飯店櫃檯", "a", "autotest")
                web.co_list_page.sleep(1)
            # 冪等清帳（同目標段理由）：325 為轉帳來源累積制卡
            ShareSteps.ensure_folio_clean(web, enter_folio)
            web.athena_base_page.screenshot("Given 點擊[住客帳維護]")

        with allure.step("Given 條件式入帳並讀取來源帳夾（轉帳前）"):
            # 條件式入帳：folio 有「正消費」就不入——判斷排除訂金（訂金使
            # get_folio_acct_nos 恆非空，誤判有帳跳過入帳致轉帳無標的；
            # ensure_folio_clean 清光正消費後訂金誤判必現，343 #463 同款教訓）；
            # acct_nos diff 追蹤轉出筆（取代金額守恆）
            consumable = web.co_list_page.get_folio_consumable_acct_nos(enter_folio)
            source_before = web.co_list_page.get_folio_acct_nos(enter_folio)
            if not consumable:
                web.co_list_page.enter_consumption(enter_item, enter_folio).sleep(1)
                source_before = web.co_list_page.get_folio_acct_nos(enter_folio)
            source_amount_before = web.co_list_page.get_folio_tab_amount(enter_folio)
            web.athena_base_page.screenshot("Given 條件式入帳並讀取來源帳夾（轉帳前）")

        with allure.step("When 點擊[轉帳]"):
            web.co_list_page.click_open_transfer_item().sleep(1)
            web.athena_base_page.screenshot("When 點擊[轉帳]")

        with allure.step("And 「轉帳項目選擇」視窗勾選消費資料列"):
            # 住客房（多 folio）需先選帳夾 grid 才載入消費；PM房（單 folio）預設帶入免選
            web.co_list_page.select_transfer_item_folio(transfer_folio).sleep(0.5)
            web.co_list_page.check_transfer_item_first().sleep(0.5)
            web.athena_base_page.screenshot("And 「轉帳項目選擇」視窗勾選消費資料列")

        with allure.step("And 點擊[轉帳]"):
            web.co_list_page.click_open_transfer_folio().sleep(1)
            web.athena_base_page.screenshot("And 點擊[轉帳]")

        with allure.step("And 「轉帳帳夾選擇」視窗勾選[選擇房號]"):
            web.co_list_page.click_transfer_target_type(target_type).sleep(0.5)
            web.athena_base_page.screenshot("And 「轉帳帳夾選擇」視窗勾選[選擇房號]")

        with allure.step("And 房號輸入C，Enter"):
            # 選擇房號 radio 後 type 即時過濾 grid（C 開頭 = 現金帳），不需 Enter
            web.co_list_page.type_transfer_room_filter(room_filter).sleep(0.5)
            web.athena_base_page.screenshot("And 房號輸入C，Enter")

        with allure.step("And 點擊住客資料列"):
            web.co_list_page.click_transfer_target_room(pm_room).sleep(1)
            web.athena_base_page.screenshot("And 點擊住客資料列")

        with allure.step("And 點擊帳夾資料列"):
            web.co_list_page.click_transfer_target_folio(pm_folio).sleep(0.5)
            web.athena_base_page.screenshot("And 點擊帳夾資料列")

        with allure.step("And 點擊[轉帳]"):
            web.co_list_page.click_confirm_transfer().sleep(1)
            web.athena_base_page.screenshot("And 點擊[轉帳]")

        with allure.step("Then 顯示轉帳成功!提示"):
            web.athena_base_page.wait_visible(web.tip_component.locator.btn_alert_ok)
            tip_text = web.tip_component.get_tip_text()
            web.athena_base_page.assert_data("轉帳提示", tip_text, "轉帳成功!")
            web.athena_base_page.screenshot("Then 顯示轉帳成功!提示")
            web.tip_component.click_ok().sleep(1)
            # 清理：轉帳項目選擇 dialog 不自動關，關掉 folio tab 才會刷新
            web.co_list_page.close_transfer_item_dialog().sleep(1)

        with allure.step("Then 來源帳夾消費款項已轉出"):
            source_after = web.co_list_page.get_folio_acct_nos(enter_folio)
            source_amount_after = web.co_list_page.get_folio_tab_amount(enter_folio)
            web.athena_base_page.screenshot("Then 來源帳夾消費款項已轉出")

        with allure.step("Then 目標帳夾頁籤新增轉入之消費款項"):
            web.co_list_page.close_guest_account_dialog().sleep(1)
            web.co_list_page.search_by_room_no(pm_room).sleep(1)
            web.co_list_page.click_card_row(pm_room).sleep(1)
            web.co_list_page.click_open_guest_account().sleep(1)
            target_after = web.co_list_page.get_folio_acct_nos(pm_folio)
            target_amount_after = web.co_list_page.get_folio_tab_amount(pm_folio)
            # 轉帳跨帳戶產生新 acct_nos（不保留來源號）：驗數量各 1 + 金額守恆
            web.athena_base_page.assert_data("來源移出一筆", len(source_before - source_after), 1)
            web.athena_base_page.assert_data("目標移入一筆", len(target_after - target_before), 1)
            web.athena_base_page.assert_data(
                "轉帳金額守恆",
                source_amount_before - source_amount_after,
                target_amount_after - target_amount_before,
            )
            web.athena_base_page.screenshot("Then 目標帳夾頁籤新增轉入之消費款項")

    @allure.story("C/O清單 - 綁訂訂金")
    @pytest.mark.xdist_group("test_co_list_flow")
    @pytest.mark.dependency(name="test_bind_deposit", scope="session")
    def test_bind_deposit(self, logged_in_driver):
        data = get_test_data("test_co_list_flow", "bind_deposit")
        card_name = data["card_name"]
        room = data["room"]
        deposit_name = data["deposit_name"]
        deposit_folio = data["deposit_folio"]
        deposit_amount = data["deposit_amount"]

        pages = [CoListPage, HeaderComponent, TipComponent, SharePanelComponent, AthenaBasePage]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        with allure.step("Given 使用者進入「C/O清單」頁面"):
            web.header_component.expand_menu("出納").sleep(1)
            web.header_component.to_func_page("C/O 清單").sleep(1)
            web.athena_base_page.screenshot("Given 使用者進入「C/O清單」頁面")

        with allure.step("Given 點擊欲進行設定之資料列"):
            web.co_list_page.search_by_guest_name(card_name).sleep(1)
            web.co_list_page.click_card_row(room).sleep(1)
            web.athena_base_page.screenshot("Given 點擊欲進行設定之資料列")

        with allure.step("Given 點擊[住客帳維護]"):
            web.co_list_page.click_open_guest_account().sleep(1)
            if web.co_list_page.has_element(web.co_list_page.locator.dialog_shift):
                ShareSteps.open_shift(web, "FO : 飯店櫃檯", "a", "autotest")
                web.co_list_page.sleep(1)
            ShareSteps.ensure_account_open(web)
            web.athena_base_page.screenshot("Given 點擊[住客帳維護]")

        with allure.step("Given 復原：清除已綁訂金（同訂金重複綁報資料無異動）"):
            web.co_list_page.click_open_assign_deposit().sleep(1)
            if web.co_list_page.has_assigned_deposit():
                web.co_list_page.clear_deposit_nos()
                web.co_list_page.click_save_assign_deposit().sleep(1)
                web.athena_base_page.wait_visible(web.tip_component.locator.btn_alert_ok)
                web.tip_component.click_ok().sleep(1)
            web.co_list_page.close_assign_deposit_dialog().sleep(1)
            web.athena_base_page.screenshot("Given 復原：清除已綁訂金（同訂金重複綁報資料無異動）")

        with allure.step("Given 檢視帳夾款項（綁定前）"):
            folio_no = deposit_folio.split(":")[0]
            amount_before = web.co_list_page.get_folio_tab_amount(folio_no)
            web.athena_base_page.screenshot("Given 檢視帳夾款項（綁定前）")

        with allure.step("When 點擊[指定訂金]"):
            web.co_list_page.click_open_assign_deposit().sleep(1)
            web.athena_base_page.screenshot("When 點擊[指定訂金]")

        with allure.step("And [訂金編號]選擇"):
            web.co_list_page.select_deposit(deposit_name).sleep(0.5)
            web.athena_base_page.screenshot("And [訂金編號]選擇")

        with allure.step("And [使用訂金的帳夾]選擇"):
            web.co_list_page.select_deposit_folio(deposit_folio).sleep(0.5)
            web.athena_base_page.screenshot("And [使用訂金的帳夾]選擇")

        with allure.step("And 點擊[橘色磁碟片]進行儲存"):
            web.co_list_page.click_save_assign_deposit().sleep(1)
            web.athena_base_page.screenshot("And 點擊[橘色磁碟片]進行儲存")

        with allure.step("Then 顯示儲存成功提示"):
            web.athena_base_page.wait_visible(web.tip_component.locator.btn_alert_ok)
            tip_text = web.tip_component.get_tip_text()
            web.athena_base_page.assert_data("儲存提示", tip_text, "儲存成功")
            web.athena_base_page.screenshot("Then 顯示儲存成功提示")
            web.tip_component.click_ok().sleep(1)

        with allure.step("Then 帳夾頁簽新增訂金資料列"):
            # 指定訂金 dialog save 後 folio tab 不即時刷新，需關 dialog 才刷新
            web.co_list_page.close_assign_deposit_dialog().sleep(1)
            amount_after = web.co_list_page.get_folio_tab_amount(folio_no)
            web.athena_base_page.assert_data(
                "訂金扣抵金額", amount_before - amount_after, deposit_amount
            )
            web.athena_base_page.screenshot("Then 帳夾頁簽新增訂金資料列")

    @allure.story("C/O清單 - 單筆金額拆帳")
    @pytest.mark.xdist_group("test_co_list_flow")
    @pytest.mark.dependency(name="test_split_amount", scope="session")
    def test_split_amount(self, logged_in_driver):
        # pylint: disable=too-many-locals  # acct_nos diff 需 folio before/after set+amount
        data = get_test_data("test_co_list_flow", "split_amount")
        card_name = data["card_name"]
        room = data["room"]
        enter_item = data["enter_item"]
        enter_folio = data["enter_folio"]
        split_method = data["split_method"]
        split_value = data["split_value"]

        pages = [CoListPage, HeaderComponent, TipComponent, SharePanelComponent, AthenaBasePage]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        with allure.step("Given 使用者進入「C/O清單」頁面"):
            web.header_component.expand_menu("出納").sleep(1)
            web.header_component.to_func_page("C/O 清單").sleep(1)
            web.athena_base_page.screenshot("Given 使用者進入「C/O清單」頁面")

        with allure.step("Given 點擊欲進行設定之資料列"):
            web.co_list_page.search_by_guest_name(card_name).sleep(1)
            web.co_list_page.click_card_row(room).sleep(1)
            web.athena_base_page.screenshot("Given 點擊欲進行設定之資料列")

        with allure.step("When 點擊[住客帳維護]"):
            web.co_list_page.click_open_guest_account().sleep(1)
            if web.co_list_page.has_element(web.co_list_page.locator.dialog_shift):
                ShareSteps.open_shift(web, "FO : 飯店櫃檯", "a", "autotest")
                web.co_list_page.sleep(1)
            ShareSteps.ensure_account_open(web)
            # 冪等清帳：註銷歷輪殘留消費，起點恆為「本次入帳那筆」（累積制卡
            # 殘留會佔據 grid 使 click_consumption_last 選錯標的——8/24 全跑炸點）
            ShareSteps.ensure_folio_clean(web)
            web.athena_base_page.screenshot("When 點擊[住客帳維護]")

        with allure.step("Given 入帳一筆消費作為拆帳標的"):
            # split 保留入帳（非條件式）：split_value 依賴標的金額（1000 拆 500），
            # 條件式會拆到未知金額殘留筆使 split_value 不適用。acct_nos diff 驗證拆帳。
            web.co_list_page.enter_consumption(enter_item, enter_folio).sleep(1)
            folio_before = web.co_list_page.get_folio_acct_nos(enter_folio)
            amount_before = web.co_list_page.get_folio_tab_amount(enter_folio)
            web.athena_base_page.screenshot("Given 入帳一筆消費作為拆帳標的")

        with allure.step("And 點擊欲進行設定之消費項目資料列"):
            # 格式對齊：select option 顯示 "1001 : 房租"（含空白），grid item_nam
            # 欄顯示 "1001:房租"（無空白），比對 grid 值需去掉空白
            item_name = enter_item.replace(" : ", ":")
            web.co_list_page.click_consumption_last(item_name).sleep(0.5)
            web.athena_base_page.screenshot("And 點擊欲進行設定之消費項目資料列")

        with allure.step("When 點擊[單筆拆帳]"):
            web.co_list_page.click_split().sleep(1)
            web.athena_base_page.screenshot("When 點擊[單筆拆帳]")

        with allure.step("And [拆分方式]選擇 AMOUNT:金額"):
            web.co_list_page.select_split_method(split_method).sleep(0.5)
            web.athena_base_page.screenshot("And [拆分方式]選擇 AMOUNT:金額")

        with allure.step("And 拆分目標輸入金額"):
            web.co_list_page.input_split_value(split_value).sleep(0.5)
            web.athena_base_page.screenshot("And 拆分目標輸入金額")

        with allure.step("Then 點擊[確定]"):
            web.co_list_page.click_split_confirm().sleep(1)
            web.athena_base_page.screenshot("Then 點擊[確定]")

        with allure.step("Then 消費項目依拆分方式調整"):
            # acct_nos diff：拆帳 = 原筆消失（1）+ 兩新筆（2）；folio 金額守恆
            folio_after = web.co_list_page.get_folio_acct_nos(enter_folio)
            amount_after = web.co_list_page.get_folio_tab_amount(enter_folio)
            split_out = folio_before - folio_after
            split_in = folio_after - folio_before
            web.athena_base_page.assert_data("拆帳原筆消失一筆", len(split_out), 1)
            web.athena_base_page.assert_data("拆帳新增兩筆", len(split_in), 2)
            web.athena_base_page.assert_data("拆帳金額守恆", amount_after, amount_before)
            web.athena_base_page.screenshot("Then 消費項目依拆分方式調整")

    @allure.story("C/O清單 - 明細移動帳夾")
    @pytest.mark.xdist_group("test_co_list_flow")
    @pytest.mark.dependency(name="test_move_folio", scope="session")
    def test_move_folio(self, logged_in_driver):
        # pylint: disable=too-many-locals  # acct_nos diff 需 folio1/2 before/after set
        data = get_test_data("test_co_list_flow", "move_folio")
        card_name = data["card_name"]
        room = data["room"]
        enter_item = data["enter_item"]
        enter_folio = data["enter_folio"]
        target_folio = data["target_folio"]

        pages = [CoListPage, HeaderComponent, TipComponent, SharePanelComponent, AthenaBasePage]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        with allure.step("Given 使用者進入「C/O清單」頁面"):
            web.header_component.expand_menu("出納").sleep(1)
            web.header_component.to_func_page("C/O 清單").sleep(1)
            web.athena_base_page.screenshot("Given 使用者進入「C/O清單」頁面")

        with allure.step("Given 點擊欲進行設定之資料列"):
            web.co_list_page.search_by_guest_name(card_name).sleep(1)
            web.co_list_page.click_card_row(room).sleep(1)
            web.athena_base_page.screenshot("Given 點擊欲進行設定之資料列")

        with allure.step("When 點擊[住客帳維護]"):
            web.co_list_page.click_open_guest_account().sleep(1)
            if web.co_list_page.has_element(web.co_list_page.locator.dialog_shift):
                ShareSteps.open_shift(web, "FO : 飯店櫃檯", "a", "autotest")
                web.co_list_page.sleep(1)
            ShareSteps.ensure_account_open(web)
            # 冪等清帳：註銷歷輪殘留，起點恆乾淨（同 split_amount setup 理由）
            ShareSteps.ensure_folio_clean(web)
            web.athena_base_page.screenshot("When 點擊[住客帳維護]")

        with allure.step("Given 條件式入帳並讀取帳夾消費（移動前）"):
            # 條件式入帳：folio 有「正消費」就不入——判斷排除訂金（ensure_folio_clean
            # 清光後訂金使 get_folio_acct_nos 恆非空，誤判跳過入帳致帳夾管理無可移
            # 項，同 transfer 四案修法）；acct_nos diff 取代金額守恆
            consumable = web.co_list_page.get_folio_consumable_acct_nos(enter_folio)
            folio1_before = web.co_list_page.get_folio_acct_nos(enter_folio)
            if not consumable:
                web.co_list_page.enter_consumption(enter_item, enter_folio).sleep(1)
                folio1_before = web.co_list_page.get_folio_acct_nos(enter_folio)
            # target folio 可能不存在（首次移動前無 folio2 tab），無 tab 視為空 set
            folio2_before = (
                web.co_list_page.get_folio_acct_nos(target_folio)
                if web.co_list_page.has_folio_tab(target_folio)
                else set()
            )
            # 帳夾管理顯示「當前 folio tab」消費，開啟前須停在來源 folio 才能移動其消費
            web.co_list_page.switch_folio_tab(enter_folio)
            web.athena_base_page.screenshot("Given 條件式入帳並讀取帳夾消費（移動前）")

        with allure.step("When 點擊[帳夾管理]"):
            web.co_list_page.click_open_folio_management().sleep(1)
            web.athena_base_page.screenshot("When 點擊[帳夾管理]")

        with allure.step("And 勾選消費款項Table之資料列"):
            # 勾任一筆（第一筆），不定位特定消費；事後 acct_nos diff 精確追蹤移動哪一筆
            web.co_list_page.check_folio_mgmt_consumption_first().sleep(0.5)
            web.athena_base_page.screenshot("And 勾選消費款項Table之資料列")

        with allure.step("And 點擊帳夾Table之資料列"):
            web.co_list_page.select_folio_in_table(target_folio).sleep(0.5)
            web.athena_base_page.screenshot("And 點擊帳夾Table之資料列")

        with allure.step("And 點擊[移動]"):
            web.co_list_page.click_folio_move().sleep(0.5)
            web.athena_base_page.screenshot("And 點擊[移動]")

        with allure.step("And 點擊[橘色磁碟片]"):
            web.co_list_page.click_folio_save().sleep(1)
            web.athena_base_page.screenshot("And 點擊[橘色磁碟片]")

        with allure.step("Then 顯示儲存成功提示"):
            web.athena_base_page.wait_visible(web.tip_component.locator.btn_alert_ok)
            tip_text = web.tip_component.get_tip_text()
            web.athena_base_page.assert_data("儲存提示", tip_text, "儲存成功")
            web.athena_base_page.screenshot("Then 顯示儲存成功提示")
            web.tip_component.click_ok().sleep(1)

        with allure.step("Then 帳夾頁簽之消費款項調整"):
            # 帳夾管理 save 後 folio tab 不即時刷新，需關 dialog 才刷新
            web.co_list_page.close_folio_management().sleep(1)
            folio1_after = web.co_list_page.get_folio_acct_nos(enter_folio)
            folio2_after = web.co_list_page.get_folio_acct_nos(target_folio)
            # acct_nos diff：folio1 移出的 acct_nos 必須 == folio2 移入的（同一筆，流水號不變）
            moved_out = folio1_before - folio1_after
            moved_in = folio2_after - folio2_before
            web.athena_base_page.assert_data("來源帳夾移出一筆", len(moved_out), 1)
            web.athena_base_page.assert_data("移出與移入為同一筆acct_nos", moved_out, moved_in)
            web.athena_base_page.screenshot("Then 帳夾頁簽之消費款項調整")

    @allure.story("C/O清單 - 結帳的付款方式")
    @pytest.mark.xdist_group("test_co_list_pay")
    @pytest.mark.dependency(name="test_checkout_pay_method", scope="session")
    @pytest.mark.parametrize(
        "data_key",
        [
            "checkout_cash",
            "checkout_visa",
            "checkout_master",
            "checkout_sign",
            "checkout_multi_credit",
        ],
    )
    def test_checkout_pay_method(self, logged_in_driver, data_key):
        # pylint: disable=too-many-branches  # 結帳多階段 alert + 信用卡分支
        data = get_test_data("test_co_list_pay", data_key)
        card_name = data["card_name"]
        room = data["room"]
        payments = data["payments"]
        pay_amount = data.get("pay_amount")

        pages = [CoListPage, HeaderComponent, TipComponent, SharePanelComponent, AthenaBasePage]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        with allure.step("Given 使用者進入「C/O清單」頁面"):
            web.header_component.expand_menu("出納").sleep(1)
            web.header_component.to_func_page("C/O 清單").sleep(1)
            web.athena_base_page.screenshot("Given 使用者進入「C/O清單」頁面")

        with allure.step("Given 點擊欲進行設定之資料列"):
            web.co_list_page.search_by_guest_name(card_name).sleep(1)
            web.co_list_page.click_card_row(room).sleep(1)
            web.athena_base_page.screenshot("Given 點擊欲進行設定之資料列")

        with allure.step("Given 點擊[住客帳維護]"):
            web.co_list_page.click_open_guest_account().sleep(1)
            if web.co_list_page.has_element(web.co_list_page.locator.dialog_shift):
                ShareSteps.open_shift(web, "FO : 飯店櫃檯", "a", "autotest")
                web.co_list_page.sleep(1)
            web.athena_base_page.screenshot("Given 點擊[住客帳維護]")

        with allure.step("Given 復原：確保開帳狀態（K 關帳則開帳）"):
            # 結帳終點 K:關帳（不退房），重跑前需開帳。toggle 後連續兩 alert（是否開帳/開帳成功）
            if not web.co_list_page.is_account_open():
                web.co_list_page.click_toggle_account().sleep(1)
                web.athena_base_page.wait_visible(web.tip_component.locator.btn_alert_ok)
                web.tip_component.click_ok().sleep(1)
                web.athena_base_page.wait_visible(web.tip_component.locator.btn_alert_ok)
                web.tip_component.click_ok().sleep(1)
            web.athena_base_page.screenshot("Given 復原：確保開帳狀態（K 關帳則開帳）")

        with allure.step("Given 復原：確保 folio 有帳務（結帳清空則入帳）"):
            # 結帳後 folio 帳務清空（未收 0），需入帳一筆作為結帳標的
            if web.co_list_page.get_folio_tab_amount("1") == 0:
                web.co_list_page.enter_consumption("1001 : 房租", "1").sleep(1)
            web.athena_base_page.screenshot("Given 復原：確保 folio 有帳務（結帳清空則入帳）")

        with allure.step("When 點擊[結帳]"):
            web.co_list_page.click_checkout_toolbar().sleep(1)
            web.athena_base_page.screenshot("When 點擊[結帳]")

        with allure.step("And 顯示「是否要關帳?」提示，點擊[確定]"):
            # 條件式文案（有預估款「尚有未入的預估款，是否要關帳?」），關帳一併入帳
            web.athena_base_page.wait_visible(web.tip_component.locator.btn_alert_ok)
            web.tip_component.click_ok().sleep(1)
            web.athena_base_page.screenshot("And 顯示「是否要關帳?」提示，點擊[確定]")
            # 「關帳成功」alert
            web.athena_base_page.wait_visible(web.tip_component.locator.btn_alert_ok)
            web.tip_component.click_ok().sleep(1)

        with allure.step("And 新增付款方式"):
            # payments 迴圈：單筆=1 筆、多筆=N 筆，統一邏輯（單筆是多筆的特例）
            # pay_amount 多筆才 type（單筆 pay_amt 自動帶入應收免 type）
            for pay in payments:
                web.co_list_page.click_add_payment().sleep(0.5)
                web.co_list_page.select_payment_method(pay["pay_code"]).sleep(0.5)
                if pay.get("credit_nos"):
                    web.co_list_page.input_credit_card(
                        pay["credit_nos"], pay["expira_mm"], pay["expira_yyyy"]
                    ).sleep(0.5)
                elif pay.get("company_name"):
                    web.co_list_page.input_sign_company(pay["company_name"]).sleep(0.5)
                if pay_amount:
                    web.co_list_page.input_pay_amt(pay_amount).sleep(0.3)
                web.co_list_page.click_save_payment().sleep(0.5)
            web.athena_base_page.screenshot("And 新增付款方式")

        with allure.step("And 點擊[結帳]"):
            # 結帳 dialog 內 checkout，實測直接跳發票載具（跳過 Gherkin「是否要結帳?」alert）
            web.co_list_page.click_checkout_dialog().sleep(1)
            web.athena_base_page.screenshot("And 點擊[結帳]")

        with allure.step("Then 顯示「發票載具」視窗，點擊[確定]"):
            web.co_list_page.click_invoice_confirm().sleep(1)
            web.athena_base_page.wait_visible(web.tip_component.locator.btn_alert_ok)
            web.athena_base_page.screenshot("Then 顯示「發票載具」視窗，點擊[確定]")
            web.tip_component.click_ok().sleep(1)

        with allure.step("Then 顯示「結帳成功，是否列印帳單?」提示，關閉列印帳單 dialog"):
            # 實測為列印帳單 dialog（非 yes/no alert），關閉=取消列印
            web.co_list_page.close_print_bill_dialog().sleep(1)
            web.athena_base_page.screenshot(
                "Then 顯示「結帳成功，是否列印帳單?」提示，關閉列印帳單 dialog"
            )

        with allure.step("Then 顯示「是否退房?」提示，點擊[取消]（不退房）"):
            web.athena_base_page.wait_visible(web.co_list_page.locator.btn_cancel_messagebox)
            # 退房確認是 el-message-box（多 <p>），用 messagebox text 抓整段
            msg_text = web.co_list_page.get_messagebox_text()
            web.athena_base_page.assert_data("退房提示", "是否退房" in msg_text, True)
            web.athena_base_page.screenshot("Then 顯示「是否退房?」提示，點擊[取消]（不退房）")
            web.co_list_page.click_cancel_messagebox().sleep(1)

    @allure.story("C/O清單 - 結帳付款方式(沖訂金)")
    @pytest.mark.xdist_group("test_co_list_pay")
    @pytest.mark.dependency(name="test_checkout_pay_deposit", scope="session")
    def test_checkout_pay_deposit(self, logged_in_driver):
        # 00 沖訂金與前 4 變體流程不同：setup 建訂金 + 結帳 dialog 自動帶入 00（非手動 select）
        data = get_test_data("test_co_list_pay", "checkout_deposit")
        card_name = data["card_name"]
        room = data["room"]
        deposit_pay_code = data["deposit_pay_code"]
        deposit_amount = data["deposit_amount"]

        pages = [CoListPage, HeaderComponent, TipComponent, SharePanelComponent, AthenaBasePage]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        with allure.step("Given 使用者進入「C/O清單」頁面"):
            web.header_component.expand_menu("出納").sleep(1)
            web.header_component.to_func_page("C/O 清單").sleep(1)
            web.athena_base_page.screenshot("Given 使用者進入「C/O清單」頁面")

        with allure.step("Given 點擊欲進行設定之資料列"):
            web.co_list_page.search_by_guest_name(card_name).sleep(1)
            web.co_list_page.click_card_row(room).sleep(1)
            web.athena_base_page.screenshot("Given 點擊欲進行設定之資料列")

        with allure.step("Given 點擊[住客帳維護]"):
            web.co_list_page.click_open_guest_account().sleep(1)
            if web.co_list_page.has_element(web.co_list_page.locator.dialog_shift):
                ShareSteps.open_shift(web, "FO : 飯店櫃檯", "a", "autotest")
                web.co_list_page.sleep(1)
            web.athena_base_page.screenshot("Given 點擊[住客帳維護]")

        with allure.step("Given 復原：確保開帳狀態（K 關帳則開帳）"):
            # 入帳需 O:開帳（K 狀態擋「目前非開帳狀態」），故開帳復原須在入帳前
            if not web.co_list_page.is_account_open():
                web.co_list_page.click_toggle_account().sleep(1)
                web.athena_base_page.wait_visible(web.tip_component.locator.btn_alert_ok)
                web.tip_component.click_ok().sleep(1)
                web.athena_base_page.wait_visible(web.tip_component.locator.btn_alert_ok)
                web.tip_component.click_ok().sleep(1)
            web.athena_base_page.screenshot("Given 復原：確保開帳狀態（K 關帳則開帳）")

        with allure.step("Given 復原：確保 folio 有帳務（結帳清空則入帳）"):
            if web.co_list_page.get_folio_tab_amount("1") == 0:
                web.co_list_page.enter_consumption("1001 : 房租", "1").sleep(1)
            web.athena_base_page.screenshot("Given 復原：確保 folio 有帳務（結帳清空則入帳）")

        with allure.step("Given 復原：取消指定既有訂金（訂金編號欄空，入口才開「新增」dialog）"):
            # 訂金結帳後資料保留（被指定狀態 C:已結清），click 入口會走「修改」非「新增」。
            # 須先取消指定（重用 #488 clear_deposit_nos）讓訂金編號欄空，才能新增另一筆
            web.co_list_page.click_open_assign_deposit().sleep(1)
            if web.co_list_page.has_assigned_deposit():
                web.co_list_page.clear_deposit_nos()
                web.co_list_page.click_save_assign_deposit().sleep(1)
                web.athena_base_page.wait_visible(web.tip_component.locator.btn_alert_ok)
                web.tip_component.click_ok().sleep(1)
            web.co_list_page.close_assign_deposit_dialog().sleep(1)
            web.athena_base_page.screenshot(
                "Given 復原：取消指定既有訂金（訂金編號欄空，入口才開「新增」dialog）"
            )

        with allure.step("Given 新增訂金（帳戶有訂金餘額才能 00 沖訂金結帳）"):
            # 訂金被沖後餘額 0（編號還在但無法再沖），每次 setup 新增確保餘額 > 0
            web.co_list_page.open_deposit_dialog().sleep(1)
            web.co_list_page.select_deposit_dt_pay_way(deposit_pay_code).sleep(0.5)
            web.co_list_page.input_deposit_dt_use_amt(deposit_amount).sleep(0.5)
            web.co_list_page.save_deposit().sleep(1)
            web.athena_base_page.wait_visible(web.tip_component.locator.btn_alert_ok)
            web.tip_component.click_ok().sleep(1)
            web.athena_base_page.screenshot("Given 新增訂金（帳戶有訂金餘額才能 00 沖訂金結帳）")

        with allure.step("When 點擊[結帳]"):
            web.co_list_page.click_checkout_toolbar().sleep(1)
            web.athena_base_page.screenshot("When 點擊[結帳]")

        with allure.step("And 顯示「是否要關帳?」提示，點擊[確定]"):
            web.athena_base_page.wait_visible(web.tip_component.locator.btn_alert_ok)
            web.tip_component.click_ok().sleep(1)
            web.athena_base_page.screenshot("And 顯示「是否要關帳?」提示，點擊[確定]")
            web.athena_base_page.wait_visible(web.tip_component.locator.btn_alert_ok)
            web.tip_component.click_ok().sleep(1)

        with allure.step("Then 結帳 dialog 自動帶入「00:沖訂金」付款方式"):
            # 00 沖訂金：帳戶有訂金 + folio 有消費 → 結帳 dialog 自動帶入 00（td pay_way text）
            pay_way = web.co_list_page.get_pay_way()
            web.athena_base_page.assert_data("付款方式自動帶入沖訂金", "沖訂金" in pay_way, True)
            web.athena_base_page.screenshot("Then 結帳 dialog 自動帶入「00:沖訂金」付款方式")

        with allure.step("And 點擊[結帳]（dialog 內 checkout）"):
            web.co_list_page.click_checkout_dialog().sleep(1)
            web.athena_base_page.screenshot("And 點擊[結帳]（dialog 內 checkout）")

        with allure.step("Then 顯示「發票載具」視窗，點擊[確定]"):
            web.co_list_page.click_invoice_confirm().sleep(1)
            web.athena_base_page.wait_visible(web.tip_component.locator.btn_alert_ok)
            web.athena_base_page.screenshot("Then 顯示「發票載具」視窗，點擊[確定]")
            web.tip_component.click_ok().sleep(1)

        with allure.step("Then 顯示「結帳成功，是否列印帳單?」提示，關閉列印帳單 dialog"):
            web.co_list_page.close_print_bill_dialog().sleep(1)
            web.athena_base_page.screenshot(
                "Then 顯示「結帳成功，是否列印帳單?」提示，關閉列印帳單 dialog"
            )

        with allure.step("Then 顯示「是否退房?」提示，點擊[取消]（不退房）"):
            web.athena_base_page.wait_visible(web.co_list_page.locator.btn_cancel_messagebox)
            msg_text = web.co_list_page.get_messagebox_text()
            web.athena_base_page.assert_data("退房提示", "是否退房" in msg_text, True)
            web.athena_base_page.screenshot("Then 顯示「是否退房?」提示，點擊[取消]（不退房）")
            web.co_list_page.click_cancel_messagebox().sleep(1)

    @allure.story("C/O清單 - 發票開立(單張)")
    @pytest.mark.xdist_group("test_co_list_invoice1")
    @pytest.mark.dependency(name="test_checkout_invoice", scope="session")
    @pytest.mark.parametrize(
        "data_key",
        [
            "checkout_invoice_none",
            "checkout_invoice_ubn",
            "checkout_invoice_carrier",
            "checkout_invoice_love",
        ],
    )
    def test_checkout_invoice(self, logged_in_driver, data_key):
        # pylint: disable=too-many-branches  # 4 變體發票載具填入分支 + 結帳多階段 alert
        data = get_test_data("test_co_list_invoice1", data_key)
        card_name = data["card_name"]
        room = data["room"]
        invoice_type = data["invoice_type"]
        pay_code = data["pay_code"]

        pages = [CoListPage, HeaderComponent, TipComponent, SharePanelComponent, AthenaBasePage]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        with allure.step("Given 使用者進入「C/O清單」頁面"):
            web.header_component.expand_menu("出納").sleep(1)
            web.header_component.to_func_page("C/O 清單").sleep(1)
            web.athena_base_page.screenshot("Given 使用者進入「C/O清單」頁面")

        with allure.step("Given 點擊欲進行設定之資料列"):
            web.co_list_page.search_by_guest_name(card_name).sleep(1)
            web.co_list_page.click_card_row(room).sleep(1)
            web.athena_base_page.screenshot("Given 點擊欲進行設定之資料列")

        with allure.step("Given 點擊[住客帳維護]"):
            web.co_list_page.click_open_guest_account().sleep(1)
            if web.co_list_page.has_element(web.co_list_page.locator.dialog_shift):
                ShareSteps.open_shift(web, "FO : 飯店櫃檯", "a", "autotest")
                web.co_list_page.sleep(1)
            web.athena_base_page.screenshot("Given 點擊[住客帳維護]")

        with allure.step("Given 復原：確保開帳狀態（K 關帳則開帳）"):
            if not web.co_list_page.is_account_open():
                web.co_list_page.click_toggle_account().sleep(1)
                web.athena_base_page.wait_visible(web.tip_component.locator.btn_alert_ok)
                web.tip_component.click_ok().sleep(1)
                web.athena_base_page.wait_visible(web.tip_component.locator.btn_alert_ok)
                web.tip_component.click_ok().sleep(1)
            web.athena_base_page.screenshot("Given 復原：確保開帳狀態（K 關帳則開帳）")

        with allure.step("Given 復原：確保 folio 有帳務（結帳清空則入帳）"):
            if web.co_list_page.get_folio_tab_amount("1") == 0:
                web.co_list_page.enter_consumption("1001 : 房租", "1").sleep(1)
            web.athena_base_page.screenshot("Given 復原：確保 folio 有帳務（結帳清空則入帳）")

        with allure.step("When 結帳並依變體填入發票載具"):
            # settle_account: 關帳→現金付款→checkout→發票載具填入→確定→列印帳單關閉（結帳框架共用）
            ShareSteps.settle_account(web, pay_code, invoice_type, data)
            web.athena_base_page.screenshot("When 結帳並依變體填入發票載具")

        with allure.step("Then 顯示「是否退房?」提示，點擊[取消]（不退房）"):
            web.athena_base_page.wait_visible(web.co_list_page.locator.btn_cancel_messagebox)
            msg_text = web.co_list_page.get_messagebox_text()
            web.athena_base_page.assert_data("退房提示", "是否退房" in msg_text, True)
            web.athena_base_page.screenshot("Then 顯示「是否退房?」提示，點擊[取消]（不退房）")
            web.co_list_page.click_cancel_messagebox().sleep(1)

        with allure.step("Postcondition 進入「發票明細」視窗驗證開立內容"):
            web.co_list_page.open_checkedout_dialog().sleep(1)
            web.co_list_page.select_latest_checkout_row().sleep(0.5)
            web.co_list_page.click_invoice_detail().sleep(1)
            detail = web.co_list_page.get_invoice_detail()
            web.athena_base_page.assert_data("發票號碼非空", bool(detail["發票號碼"]), True)
            web.athena_base_page.assert_data("發票金額非空", bool(detail["發票金額"]), True)
            web.athena_base_page.screenshot("Postcondition 進入「發票明細」視窗驗證開立內容")

        with allure.step("Postcondition 驗證發票類型欄位"):
            if invoice_type == "none":
                web.athena_base_page.assert_data("統一編號為空", detail["統一編號"], "")
                web.athena_base_page.assert_data("未捐贈", detail["是否捐贈"], "N")
            elif invoice_type == "ubn":
                web.athena_base_page.assert_data("統一編號", detail["統一編號"], data["ubn"])
            elif invoice_type == "carrier":
                web.athena_base_page.assert_data(
                    "載具類別", detail["載具類別"], data["carrier_type"]
                )
                web.athena_base_page.assert_data("載具顯碼", detail["載具顯碼"], data["carrier_id"])
                web.athena_base_page.assert_data("載具隱碼", detail["載具隱碼"], data["carrier_id"])
            elif invoice_type == "love":
                web.athena_base_page.assert_data("捐贈", detail["是否捐贈"], "Y")
                web.athena_base_page.assert_data("愛心碼", detail["愛心碼"], data["love_code"])
            web.athena_base_page.screenshot("Postcondition 驗證發票類型欄位")
            web.co_list_page.close_invoice_detail().sleep(0.5)

    @allure.story("C/O清單 - 發票開立(多張)")
    @pytest.mark.xdist_group("test_co_list_invoiceN")
    @pytest.mark.dependency(name="test_checkout_invoice_multi", scope="session")
    @pytest.mark.parametrize("data_key", ["multi_equal", "multi_unequal", "multi_diff_attrs"])
    def test_checkout_invoice_multi(self, logged_in_driver, data_key):
        # pylint: disable=too-many-locals  # 3 變體逐張設定 + Postcondition 多欄位
        data = get_test_data("test_co_list_invoiceN", data_key)
        card_name = data["card_name"]
        room = data["room"]
        invoice_count = data["invoice_count"]
        is_divided = data["is_divided"]
        copies = data["copies"]
        pay_code = data["pay_code"]

        pages = [CoListPage, HeaderComponent, TipComponent, SharePanelComponent, AthenaBasePage]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        with allure.step("Given 使用者進入「C/O清單」頁面"):
            web.header_component.expand_menu("出納").sleep(1)
            web.header_component.to_func_page("C/O 清單").sleep(1)
            web.athena_base_page.screenshot("Given 使用者進入「C/O清單」頁面")

        with allure.step("Given 點擊欲進行設定之資料列"):
            web.co_list_page.search_by_guest_name(card_name).sleep(1)
            web.co_list_page.click_card_row(room).sleep(1)
            web.athena_base_page.screenshot("Given 點擊欲進行設定之資料列")

        with allure.step("Given 點擊[住客帳維護]"):
            web.co_list_page.click_open_guest_account().sleep(1)
            if web.co_list_page.has_element(web.co_list_page.locator.dialog_shift):
                ShareSteps.open_shift(web, "FO : 飯店櫃檯", "a", "autotest")
                web.co_list_page.sleep(1)
            web.athena_base_page.screenshot("Given 點擊[住客帳維護]")

        with allure.step("Given 復原：確保開帳狀態（K 關帳則開帳）"):
            if not web.co_list_page.is_account_open():
                web.co_list_page.click_toggle_account().sleep(1)
                web.athena_base_page.wait_visible(web.tip_component.locator.btn_alert_ok)
                web.tip_component.click_ok().sleep(1)
                web.athena_base_page.wait_visible(web.tip_component.locator.btn_alert_ok)
                web.tip_component.click_ok().sleep(1)
            web.athena_base_page.screenshot("Given 復原：確保開帳狀態（K 關帳則開帳）")

        with allure.step("Given 復原：確保 folio 有帳務（結帳清空則入帳）"):
            if web.co_list_page.get_folio_tab_amount("1") == 0:
                web.co_list_page.enter_consumption("1001 : 房租", "1").sleep(1)
            web.athena_base_page.screenshot("Given 復原：確保 folio 有帳務（結帳清空則入帳）")

        with allure.step("When 點擊[結帳]"):
            web.co_list_page.click_checkout_toolbar().sleep(1)
            web.athena_base_page.screenshot("When 點擊[結帳]")

        with allure.step("And 顯示「是否要關帳?」提示，點擊[確定]"):
            web.athena_base_page.wait_visible(web.tip_component.locator.btn_alert_ok)
            web.tip_component.click_ok().sleep(1)
            web.athena_base_page.screenshot("And 顯示「是否要關帳?」提示，點擊[確定]")
            web.athena_base_page.wait_visible(web.tip_component.locator.btn_alert_ok)
            web.tip_component.click_ok().sleep(1)

        with allure.step("And 新增付款方式"):
            web.co_list_page.click_add_payment().sleep(0.5)
            web.co_list_page.select_payment_method(pay_code).sleep(0.5)
            web.co_list_page.click_save_payment().sleep(0.5)
            web.athena_base_page.screenshot("And 新增付款方式")

        with allure.step("And 點擊[分發票]"):
            # 直接開設定 dialog（Gherkin『是否要結帳?』alert 不準，分發票無此 alert）
            web.co_list_page.click_invoice().sleep(1)
            web.athena_base_page.screenshot("And 點擊[分發票]")

        with allure.step("When 設定發票張數"):
            web.co_list_page.input_uniinv_count(invoice_count).sleep(0.5)
            if is_divided:
                web.co_list_page.check_is_divided_equally().sleep(0.3)
            web.co_list_page.click_check_invoice_num().sleep(1)
            web.athena_base_page.screenshot("When 設定發票張數")

        with allure.step("And 逐張設定發票屬性與金額"):
            for idx, copy in enumerate(copies, start=1):
                web.co_list_page.select_invoice_copy(idx).sleep(0.3)
                web.co_list_page.fill_split_invoice(copy["invoice_type"], copy).sleep(0.3)
                if not is_divided and "unit_price" in copy:
                    web.co_list_page.input_unit_price(copy["unit_price"]).sleep(0.3)
            web.athena_base_page.screenshot("And 逐張設定發票屬性與金額")

        with allure.step("And 點擊[橘色磁碟片]儲存"):
            web.co_list_page.click_save_invoice_split().sleep(1)
            web.athena_base_page.screenshot("And 點擊[橘色磁碟片]儲存")

        with allure.step("Then 顯示「確認附屬程式」提示，點擊[確定]"):
            web.athena_base_page.wait_visible(web.tip_component.locator.btn_alert_ok)
            web.tip_component.click_ok().sleep(2)
            web.athena_base_page.screenshot("Then 顯示「確認附屬程式」提示，點擊[確定]")

        with allure.step("Then 關閉列印帳單 dialog"):
            web.co_list_page.close_print_bill_dialog().sleep(1)
            web.athena_base_page.screenshot("Then 關閉列印帳單 dialog")

        with allure.step("Then 顯示「是否退房?」提示，點擊[取消]（不退房）"):
            web.athena_base_page.wait_visible(web.co_list_page.locator.btn_cancel_messagebox)
            msg_text = web.co_list_page.get_messagebox_text()
            web.athena_base_page.assert_data("退房提示", "是否退房" in msg_text, True)
            web.athena_base_page.screenshot("Then 顯示「是否退房?」提示，點擊[取消]（不退房）")
            web.co_list_page.click_cancel_messagebox().sleep(1)

        with allure.step("Postcondition 進入「發票明細」視窗驗證所有發票內容"):
            web.co_list_page.open_checkedout_dialog().sleep(1)
            web.co_list_page.select_latest_checkout_row().sleep(0.5)
            web.co_list_page.click_invoice_detail().sleep(1)
            for idx, copy in enumerate(copies):
                web.co_list_page.select_invoice_detail_row(idx).sleep(0.3)
                detail = web.co_list_page.get_invoice_detail()
                web.athena_base_page.assert_data(
                    f"發票{idx+1}號碼非空", bool(detail["發票號碼"]), True
                )
                web.athena_base_page.assert_data(
                    f"發票{idx+1}金額", detail["發票金額"], str(copy["expected_amount"])
                )
                itype = copy["invoice_type"]
                if itype == "none":
                    web.athena_base_page.assert_data(f"發票{idx+1}統編空", detail["統一編號"], "")
                    web.athena_base_page.assert_data(f"發票{idx+1}未捐贈", detail["是否捐贈"], "N")
                elif itype == "ubn":
                    web.athena_base_page.assert_data(
                        f"發票{idx+1}統編", detail["統一編號"], copy["ubn"]
                    )
                elif itype == "carrier":
                    web.athena_base_page.assert_data(
                        f"發票{idx+1}載具類別", detail["載具類別"], copy["carrier_type"]
                    )
                    web.athena_base_page.assert_data(
                        f"發票{idx+1}載具顯碼", detail["載具顯碼"], copy["carrier_id"]
                    )
                elif itype == "love":
                    web.athena_base_page.assert_data(f"發票{idx+1}捐贈", detail["是否捐贈"], "Y")
                    web.athena_base_page.assert_data(
                        f"發票{idx+1}愛心碼", detail["愛心碼"], copy["love_code"]
                    )
            web.athena_base_page.screenshot("Postcondition 進入「發票明細」視窗驗證所有發票內容")
            web.co_list_page.close_invoice_detail().sleep(0.5)

    @allure.story("C/O清單 - 退房完成後，已退房的資料要顯示在Check Out的分頁裡")
    @pytest.mark.xdist_group("test_co_list_restore")
    @pytest.mark.dependency(name="test_checkout_complete", scope="session")
    def test_checkout_complete(self, logged_in_driver):
        data = get_test_data("test_co_list_restore", "checkout_complete")
        card_name = data["card_name"]
        room = data["room"]

        pages = [CoListPage, HeaderComponent, TipComponent, SharePanelComponent, AthenaBasePage]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        with allure.step("Given 使用者進入「C/O清單」頁面"):
            web.header_component.expand_menu("出納").sleep(1)
            web.header_component.to_func_page("C/O 清單").sleep(1)
            web.athena_base_page.screenshot("Given 使用者進入「C/O清單」頁面")

        with allure.step("Given 復原：確保卡在 In house（前輪中斷殘留 Check Out 則退房還原）"):
            ShareSteps.restore_room_to_inhouse(web, room)
            # restore 結束停在 Check Out tab，還原成功後須切回 In house 才搜得到卡
            web.co_list_page.click_inhouse_tab().sleep(1)
            web.athena_base_page.screenshot(
                "Given 復原：確保卡在 In house（前輪中斷殘留 Check Out 則退房還原）"
            )

        with allure.step("Given 點擊欲進行設定之資料列"):
            web.co_list_page.search_by_guest_name(card_name).sleep(1)
            web.co_list_page.click_card_row(room).sleep(1)
            web.athena_base_page.screenshot("Given 點擊欲進行設定之資料列")

        with allure.step("Given 點擊[住客帳維護]"):
            web.co_list_page.click_open_guest_account().sleep(1)
            if web.co_list_page.has_element(web.co_list_page.locator.dialog_shift):
                ShareSteps.open_shift(web, "FO : 飯店櫃檯", "a", "autotest")
                web.co_list_page.sleep(1)
            web.athena_base_page.screenshot("Given 點擊[住客帳維護]")

        with allure.step("Given 復原：確保開帳狀態（K 關帳則開帳）"):
            ShareSteps.ensure_account_open(web)
            web.athena_base_page.screenshot("Given 復原：確保開帳狀態（K 關帳則開帳）")

        with allure.step("Given 復原：確保 folio 有帳務（結帳清空則入帳）"):
            if web.co_list_page.get_folio_tab_amount("1") == 0:
                web.co_list_page.enter_consumption("1001 : 房租", "1").sleep(1)
            web.athena_base_page.screenshot("Given 復原：確保 folio 有帳務（結帳清空則入帳）")

        with allure.step("When 結帳"):
            ShareSteps.settle_account(web, "10", "none")
            web.athena_base_page.screenshot("When 結帳")

        with allure.step("And 確認退房訊息點擊[確定]"):
            web.athena_base_page.wait_visible(web.co_list_page.locator.btn_cancel_messagebox)
            msg_text = web.co_list_page.get_messagebox_text()
            web.athena_base_page.assert_data("退房提示", "是否退房" in msg_text, True)
            web.athena_base_page.screenshot("And 確認退房訊息點擊[確定]")
            web.co_list_page.click_confirm_messagebox().sleep(1)

        with allure.step("Then 顯示「退房完成」提示"):
            web.athena_base_page.wait_visible(web.tip_component.locator.btn_alert_ok)
            web.athena_base_page.screenshot("Then 顯示「退房完成」提示")
            web.tip_component.click_ok().sleep(1)

        with allure.step("And 關閉視窗"):
            web.co_list_page.close_guest_account_dialog().sleep(1)
            web.athena_base_page.screenshot("And 關閉視窗")

        with allure.step("Then 「C/O清單」Check Out 頁籤顯示資料列"):
            web.co_list_page.click_checkout_tab().sleep(1)
            web.athena_base_page.assert_data(
                "Check Out 顯示退房資料", web.co_list_page.has_card_row(room), True
            )
            web.athena_base_page.screenshot("Then 「C/O清單」Check Out 頁籤顯示資料列")

    @allure.story("C/O清單 - 執行退房還原")
    @pytest.mark.xdist_group("test_co_list_restore")
    @pytest.mark.dependency(name="test_restore_checkout", scope="session")
    def test_restore_checkout(self, logged_in_driver):
        data = get_test_data("test_co_list_restore", "restore_checkout")
        card_name = data["card_name"]
        room = data["room"]

        pages = [CoListPage, HeaderComponent, TipComponent, SharePanelComponent, AthenaBasePage]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        with allure.step("Given 使用者進入「C/O清單」頁面"):
            web.header_component.expand_menu("出納").sleep(1)
            web.header_component.to_func_page("C/O 清單").sleep(1)
            web.athena_base_page.screenshot("Given 使用者進入「C/O清單」頁面")

        with allure.step("Given 確保已退房到 Check Out（冪等 setup）"):
            ShareSteps.ensure_checkout_state(web, card_name, room)
            web.athena_base_page.screenshot("Given 確保已退房到 Check Out（冪等 setup）")

        with allure.step("When 點擊[退房還原]"):
            web.co_list_page.click_restore_checkout().sleep(1)
            web.athena_base_page.screenshot("When 點擊[退房還原]")

        with allure.step("And 顯示「確定要執行退房還原嗎?」提示，點擊[確定]"):
            web.athena_base_page.wait_visible(web.tip_component.locator.btn_alert_ok)
            web.athena_base_page.assert_data(
                "退房還原確認", "退房還原" in web.tip_component.get_tip_text(), True
            )
            web.athena_base_page.screenshot("And 顯示「確定要執行退房還原嗎?」提示，點擊[確定]")
            web.tip_component.click_ok().sleep(1)

        with allure.step("Then 顯示「儲存成功」提示"):
            web.athena_base_page.wait_visible(web.tip_component.locator.btn_alert_ok)
            web.athena_base_page.assert_data(
                "儲存成功", web.tip_component.get_tip_text(), "儲存成功"
            )
            web.athena_base_page.screenshot("Then 顯示「儲存成功」提示")
            web.tip_component.click_ok().sleep(1)

        with allure.step("Then 該筆資料出現在 In House 分頁"):
            web.co_list_page.click_inhouse_tab().sleep(1)
            web.athena_base_page.assert_data(
                "In House 顯示還原資料", web.co_list_page.has_card_row(room), True
            )
            web.athena_base_page.screenshot("Then 該筆資料出現在 In House 分頁")

    @allure.story("已結帳 - 執行結帳還原")
    @pytest.mark.xdist_group("test_co_list_restore")
    @pytest.mark.dependency(name="test_cancel_checkout", scope="session")
    def test_cancel_checkout(self, logged_in_driver):
        data = get_test_data("test_co_list_restore", "cancel_checkout")
        card_name = data["card_name"]
        room = data["room"]

        pages = [CoListPage, HeaderComponent, TipComponent, SharePanelComponent, AthenaBasePage]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        with allure.step("Given 使用者進入「C/O清單」頁面"):
            web.header_component.expand_menu("出納").sleep(1)
            web.header_component.to_func_page("C/O 清單").sleep(1)
            web.athena_base_page.screenshot("Given 使用者進入「C/O清單」頁面")

        with allure.step("Given 確保已退房到 Check Out（冪等 setup）"):
            ShareSteps.ensure_checkout_state(web, card_name, room)
            web.athena_base_page.screenshot("Given 確保已退房到 Check Out（冪等 setup）")

        with allure.step("When 點擊[已結帳]"):
            web.co_list_page.click_checkedout_toolbar().sleep(1)
            if web.co_list_page.has_element(web.co_list_page.locator.dialog_shift):
                ShareSteps.open_shift(web, "FO : 飯店櫃檯", "a", "autotest")
                web.co_list_page.sleep(1)
            web.athena_base_page.screenshot("When 點擊[已結帳]")

        with allure.step("And 選當班結帳 row"):
            web.co_list_page.select_latest_checkout_row().sleep(0.5)
            web.athena_base_page.screenshot("And 選當班結帳 row")

        with allure.step("And 點擊[結帳還原]"):
            web.co_list_page.click_cancel_checkout_record().sleep(1)
            web.athena_base_page.screenshot("And 點擊[結帳還原]")

        with allure.step("And 顯示「確定要執行結帳還原功能嗎?」提示，點擊[確定]"):
            web.athena_base_page.wait_visible(web.tip_component.locator.btn_alert_ok)
            web.athena_base_page.assert_data(
                "結帳還原確認", "結帳還原" in web.tip_component.get_tip_text(), True
            )
            web.athena_base_page.screenshot("And 顯示「確定要執行結帳還原功能嗎?」提示，點擊[確定]")
            web.tip_component.click_ok().sleep(1)

        with allure.step("Then 顯示「結帳還原成功」提示"):
            web.athena_base_page.wait_visible(web.tip_component.locator.btn_alert_ok)
            web.athena_base_page.assert_data(
                "結帳還原成功", web.tip_component.get_tip_text(), "結帳還原成功"
            )
            web.athena_base_page.screenshot("Then 顯示「結帳還原成功」提示")
            web.tip_component.click_ok().sleep(1)

        with allure.step("And 關閉已結帳視窗"):
            web.co_list_page.close_checkedout_dialog().sleep(1)
            web.athena_base_page.screenshot("And 關閉已結帳視窗")

        with allure.step("Then 該筆資料出現在 In House 分頁"):
            web.co_list_page.click_inhouse_tab().sleep(1)
            web.athena_base_page.assert_data(
                "In House 顯示還原資料", web.co_list_page.has_card_row(room), True
            )
            web.athena_base_page.screenshot("Then 該筆資料出現在 In House 分頁")

    @allure.story("已結帳 - 更改付款方式")
    @pytest.mark.xdist_group("test_co_list_restore")
    @pytest.mark.dependency(name="test_edit_payment", scope="session")
    @pytest.mark.parametrize("data_key", ["edit_visa", "edit_multi", "edit_sign", "edit_deposit"])
    def test_edit_payment(self, logged_in_driver, data_key):
        data = get_test_data("test_co_list_restore", data_key)
        card_name = data["card_name"]
        room = data["room"]
        payments = data["payments"]
        pay_amount = data.get("pay_amount")

        pages = [CoListPage, HeaderComponent, TipComponent, SharePanelComponent, AthenaBasePage]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        with allure.step("Given 使用者進入「C/O清單」頁面"):
            web.header_component.expand_menu("出納").sleep(1)
            web.header_component.to_func_page("C/O 清單").sleep(1)
            web.athena_base_page.screenshot("Given 使用者進入「C/O清單」頁面")

        with allure.step("Given 確保已退房到 Check Out（冪等 setup）"):
            ShareSteps.ensure_checkout_state(web, card_name, room)
            web.athena_base_page.screenshot("Given 確保已退房到 Check Out（冪等 setup）")

        with allure.step("When 點擊[已結帳]"):
            web.co_list_page.click_checkedout_toolbar().sleep(1)
            if web.co_list_page.has_element(web.co_list_page.locator.dialog_shift):
                ShareSteps.open_shift(web, "FO : 飯店櫃檯", "a", "autotest")
                web.co_list_page.sleep(1)
            web.athena_base_page.screenshot("When 點擊[已結帳]")

        with allure.step("And 選當班結帳 row"):
            web.co_list_page.select_latest_checkout_row().sleep(0.5)
            web.athena_base_page.screenshot("And 選當班結帳 row")

        with allure.step("And 點擊[更改付款方式]"):
            web.co_list_page.click_edit_payment().sleep(1)
            web.athena_base_page.screenshot("And 點擊[更改付款方式]")

        with allure.step("And 顯示「更改付款方式」視窗，點擊[清除付款]"):
            web.co_list_page.click_clear_payment().sleep(1)
            web.athena_base_page.screenshot("And 顯示「更改付款方式」視窗，點擊[清除付款]")

        with allure.step("And 選擇[付款方式]"):
            # payments 迴圈：單筆=1 筆、多筆=N 筆，統一邏輯（同 #496 結帳付款）
            # pay_amount 多筆才 type（單筆 pay_amt 自動帶應收全額免 type）
            for pay in payments:
                web.co_list_page.click_add_payment().sleep(0.5)
                web.co_list_page.select_payment_method(pay["pay_code"]).sleep(0.5)
                if pay.get("credit_nos"):
                    web.co_list_page.input_credit_card(
                        pay["credit_nos"], pay["expira_mm"], pay["expira_yyyy"]
                    ).sleep(0.5)
                elif pay.get("company_name"):
                    web.co_list_page.input_sign_company(pay["company_name"]).sleep(0.5)
                elif pay.get("deposit_name"):
                    web.co_list_page.select_deposit_in_payment(pay["deposit_name"]).sleep(0.5)
                if pay_amount:
                    web.co_list_page.input_pay_amt(pay_amount).sleep(0.3)
                web.co_list_page.click_save_payment().sleep(0.5)
            web.athena_base_page.screenshot("And 選擇[付款方式]")

        with allure.step("And 點擊[橘色磁碟片]進行儲存"):
            web.co_list_page.click_do_save().sleep(1)
            web.athena_base_page.screenshot("And 點擊[橘色磁碟片]進行儲存")

        with allure.step("Then 顯示「儲存成功」提示"):
            web.athena_base_page.wait_visible(web.tip_component.locator.btn_alert_ok)
            web.athena_base_page.assert_data(
                "儲存成功", web.tip_component.get_tip_text(), "儲存成功"
            )
            web.athena_base_page.screenshot("Then 顯示「儲存成功」提示")
            web.tip_component.click_ok().sleep(1)

        with allure.step("Then 重新選取該筆，確認付款方式已變更"):
            # doSave 後 grid 刷新 row 跳走，重選最新筆（序號不變）；Table #32 顯示新付款方式
            web.co_list_page.select_latest_checkout_row().sleep(0.5)
            pay_codes = web.co_list_page.get_checkout_pay_methods()
            for pay in payments:
                web.athena_base_page.assert_data(
                    "付款方式 " + pay["pay_code"] + " 已變更", pay["pay_code"] in pay_codes, True
                )
            web.athena_base_page.screenshot("Then 確認付款方式已變更")

        with allure.step("And 關閉已結帳視窗"):
            web.co_list_page.close_checkedout_dialog().sleep(1)
            web.athena_base_page.screenshot("And 關閉已結帳視窗")

    @allure.story("已結帳 - 重開發票")
    @pytest.mark.xdist_group("test_co_list_reinvoice")
    @pytest.mark.dependency(name="test_reinvoice_checkout", scope="session")
    @pytest.mark.parametrize(
        "data_key",
        [
            "reinvoice_none",
            "reinvoice_ubn",
            "reinvoice_carrier",
            "reinvoice_love",
        ],
    )
    def test_reinvoice_checkout(self, logged_in_driver, data_key):
        data = get_test_data("test_co_list_reinvoice", data_key)
        room = data["room"]
        invoice_type = data["invoice_type"]

        pages = [CoListPage, HeaderComponent, TipComponent, SharePanelComponent, AthenaBasePage]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        with allure.step("Given 使用者進入「C/O清單」頁面"):
            web.header_component.expand_menu("出納").sleep(1)
            web.header_component.to_func_page("C/O 清單").sleep(1)
            web.athena_base_page.screenshot("Given 使用者進入「C/O清單」頁面")

        with allure.step("Given 確保 In house + 已結帳（未退房，重開發票前置）"):
            # 入口 B（住客帳單筆已結帳總額旁 [...]）不限退房；331 設計 In house + 當班結帳記錄
            ShareSteps.ensure_checkedout_inhouse(web, room)
            web.athena_base_page.screenshot("Given 確保 In house + 已結帳（未退房，重開發票前置）")

        with allure.step("When 開啟已結帳視窗"):
            web.co_list_page.open_checkedout_dialog().sleep(1)
            web.athena_base_page.screenshot("When 開啟已結帳視窗")

        with allure.step("And 選當班結帳 row，記錄重開前發票號"):
            web.co_list_page.select_latest_checkout_row().sleep(0.5)
            invoice_no_before = web.co_list_page.get_checkout_invoice_no()
            web.athena_base_page.screenshot("And 選當班結帳 row，記錄重開前發票號")

        with allure.step("And 點擊[重開發票]"):
            web.co_list_page.click_reinvoice().sleep(1)
            web.athena_base_page.screenshot("And 點擊[重開發票]")

        with allure.step("And 顯示「是否確定要重開發票」提示，點擊[確定]"):
            web.athena_base_page.wait_visible(web.tip_component.locator.btn_alert_ok)
            web.athena_base_page.assert_data(
                "重開發票確認", "是否確定要重開發票" in web.tip_component.get_tip_text(), True
            )
            web.athena_base_page.screenshot("And 顯示「是否確定要重開發票」提示，點擊[確定]")
            web.tip_component.click_ok().sleep(1)

        with allure.step("And 顯示發票載具視窗，依變體填入"):
            web.co_list_page.fill_invoice(invoice_type, data).sleep(0.5)
            web.athena_base_page.screenshot("And 顯示發票載具視窗，依變體填入")

        with allure.step("And 點擊發票載具[確定]"):
            web.co_list_page.click_invoice_confirm().sleep(1)
            web.athena_base_page.wait_visible(web.tip_component.locator.btn_alert_ok)
            web.tip_component.click_ok().sleep(1)
            web.athena_base_page.screenshot("And 點擊發票載具[確定]")

        with allure.step("Then 已結帳視窗發票號碼變更為新發票號"):
            # 重開發票不跳列印帳單（與結帳流程差異），直接回已結帳 dialog 刷新發票號
            web.co_list_page.select_latest_checkout_row().sleep(0.5)
            invoice_no_after = web.co_list_page.get_checkout_invoice_no()
            web.athena_base_page.assert_data("重開前發票號", invoice_no_before, invoice_no_before)
            web.athena_base_page.assert_data("重開後發票號", invoice_no_after, invoice_no_after)
            web.athena_base_page.assert_data(
                f"發票號碼已變更（{invoice_no_before} → {invoice_no_after}）",
                invoice_no_after != invoice_no_before,
                True,
            )
            web.athena_base_page.screenshot("Then 已結帳視窗發票號碼變更為新發票號")

        with allure.step("Postcondition 發票明細視窗顯示新發票號"):
            web.co_list_page.click_invoice_detail().sleep(1)
            detail = web.co_list_page.get_invoice_detail()
            web.athena_base_page.assert_data(
                "發票明細新發票號", detail["發票號碼"], invoice_no_after
            )
            web.athena_base_page.screenshot("Postcondition 發票明細視窗顯示新發票號")
            web.co_list_page.close_invoice_detail().sleep(1)

        with allure.step("And 關閉已結帳視窗"):
            web.co_list_page.close_checkedout_dialog().sleep(1)
            web.athena_base_page.screenshot("And 關閉已結帳視窗")
