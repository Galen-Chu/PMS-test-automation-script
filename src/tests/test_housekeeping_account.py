import allure
import pytest
from pages.athena_base_page import AthenaBasePage
from pages.co_list_page import CoListPage
from pages.components.header_component import HeaderComponent
from pages.components.share_panel_component import SharePanelComponent
from pages.components.tip_component import TipComponent
from pages.guest_account_page import GuestAccountPage
from pages.housekeeping_account_page import HousekeepingAccountPage
from pages.room_control_page import RoomControlPage
from tests.share_steps import ShareSteps
from tools.driver_helper import DriverHelper
from tools.test_data_helper import get_group_data, get_test_data

RECALC_TIP = "更動洗衣折扣率"


@allure.feature("房控管理")
class TestHousekeepingAccount:

    @allure.story("新增房務入帳")
    @pytest.mark.xdist_group("test_housekeeping_account")
    @pytest.mark.dependency(name="test_add_housekeeping_account", scope="session")
    @pytest.mark.parametrize(
        "data_key",
        [
            pytest.param("minibar_disc", id="MiniBar有折扣率"),
            pytest.param("laundry_disc", id="Laundry有折扣率"),
            pytest.param("both_zero", id="MiniBar零折扣率+Laundry零折扣率（清空儲存）"),
            pytest.param("minibar_disc_l0", id="MiniBar有折扣率+Laundry零折扣率"),
            pytest.param("m0_laundry_disc", id="MiniBar零折扣率+Laundry有折扣率"),
            pytest.param("both_disc", id="MiniBar有折扣率+Laundry有折扣率"),
        ],
    )
    def test_add_housekeeping_account(self, logged_in_driver, data_key):
        common = get_group_data("test_housekeeping_account")
        data = get_test_data("test_housekeeping_account", data_key)
        room = common["room"]

        pages = [
            AthenaBasePage,
            CoListPage,
            GuestAccountPage,
            HeaderComponent,
            HousekeepingAccountPage,
            RoomControlPage,
            SharePanelComponent,
            TipComponent,
        ]
        web = DriverHelper.get_logged_in_browser(pages, "reservation/PMS0110010")

        # 入帳前快照 folio1 acct_nos：累積制卡不復原，Postcondition 以 diff 鎖定本次新增筆
        with allure.step("Given 記錄帳夾1入帳前消費（對帳基準）"):
            web.header_component.expand_menu("出納").sleep(1)
            web.header_component.to_func_page("住客帳維護").sleep(1)
            web.guest_account_page.search_room(room).sleep(1)
            web.guest_account_page.click_card_row(room).sleep(0.5)
            web.guest_account_page.click_guest_maintain().sleep(1)
            if web.athena_base_page.has_element(web.guest_account_page.locator.dialog_shift):
                ShareSteps.open_shift(web, "FO : 飯店櫃檯", "a", "autotest")
                web.athena_base_page.sleep(1)
            acct_nos_before = web.co_list_page.get_folio_acct_nos("1")
            web.guest_account_page.close_single_dialog().sleep(1)
            web.athena_base_page.screenshot("Given 記錄帳夾1入帳前消費（對帳基準）")

        with allure.step("Given 使用者進入「房控管理」頁面"):
            web.header_component.expand_menu("房務").sleep(1)
            web.header_component.to_func_page("房控管理").sleep(1)
            web.athena_base_page.screenshot("Given 使用者進入「房控管理」頁面")

        with allure.step("And 選擇點擊欲進行房務入帳之房間方框，顯示「功能選項」視窗"):
            # 37x 房卡不在樓層 tab lazy render 範圍，須搜尋區房號 filter
            web.room_control_page.search_room_filter(room).sleep(1)
            web.room_control_page.choose_room(room).sleep(0.5)
            web.athena_base_page.screenshot(
                "And 選擇點擊欲進行房務入帳之房間方框，顯示「功能選項」視窗"
            )

        with allure.step("When 點擊[房務入帳]，顯示「房務帳資料編輯」視窗"):
            web.room_control_page.click_housekeeping_account().sleep(1)
            # 房控開班與出納開班互不相通，未開班時跳「選擇班別」dialog
            if web.athena_base_page.has_element(web.housekeeping_account_page.locator.dialog_shift):
                web.housekeeping_account_page.select_class("FO", "a").sleep(1)
            web.athena_base_page.screenshot("When 點擊[房務入帳]，顯示「房務帳資料編輯」視窗")

        with allure.step("And 點擊下方Table之[綠色加號]新增消費項目"):
            web.housekeeping_account_page.click(
                web.housekeeping_account_page.locator.btn_add_housekeeping
            )
            web.athena_base_page.sleep(1)
            web.athena_base_page.screenshot("And 點擊下方Table之[綠色加號]新增消費項目")

        with allure.step(f"And 點擊[小分類代號]欄位選擇{data['small_type']}"):
            web.housekeeping_account_page.select_row_type("smallType", data["small_type"])
            web.athena_base_page.screenshot(f"And 點擊[小分類代號]欄位選擇{data['small_type']}")

        with allure.step(f"And 點擊[消費代號]欄位選擇{data['product']}"):
            web.housekeeping_account_page.select_row_type("productNos", data["product"])
            web.athena_base_page.screenshot(f"And 點擊[消費代號]欄位選擇{data['product']}")

        if data.get("clear_rates"):
            with allure.step("And 清空MiniBar折扣率與Laundry折扣率欄位（留白）"):
                web.housekeeping_account_page.clear_discount_rate("minibar")
                web.housekeeping_account_page.clear_discount_rate("laundry")
                web.athena_base_page.sleep(0.5)
                web.athena_base_page.screenshot("And 清空MiniBar折扣率與Laundry折扣率欄位（留白）")

        if data["minibar_rate"] > 0:
            with allure.step(f"And 如需變更，填寫MiniBar折扣率{data['minibar_rate']}%，預設為0%"):
                web.housekeeping_account_page.set_discount_rate("minibar", data["minibar_rate"])
                web.athena_base_page.sleep(0.5)
                web.athena_base_page.screenshot(
                    f"And 如需變更，填寫MiniBar折扣率{data['minibar_rate']}%，預設為0%"
                )

            with allure.step('And 顯示"更動洗衣折扣率, 明細會重新計算, 是否執行"提示'):
                tip_text = web.tip_component.get_tip_text()
                web.athena_base_page.assert_data("重算提示", RECALC_TIP in tip_text, True)
                web.athena_base_page.screenshot(
                    'And 顯示"更動洗衣折扣率, 明細會重新計算, 是否執行"提示'
                )

            with allure.step("And 點擊[確定]"):
                web.tip_component.click_ok().sleep(1)
                web.athena_base_page.screenshot("And 點擊[確定]")

        if data["laundry_rate"] > 0:
            with allure.step(f"And 如需變更，填寫Laundry折扣率{data['laundry_rate']}%，預設為0%"):
                web.housekeeping_account_page.set_discount_rate("laundry", data["laundry_rate"])
                web.athena_base_page.sleep(0.5)
                web.athena_base_page.screenshot(
                    f"And 如需變更，填寫Laundry折扣率{data['laundry_rate']}%，預設為0%"
                )

            with allure.step('And 顯示"更動洗衣折扣率, 明細會重新計算, 是否執行"提示'):
                tip_text = web.tip_component.get_tip_text()
                web.athena_base_page.assert_data("重算提示", RECALC_TIP in tip_text, True)
                web.athena_base_page.screenshot(
                    'And 顯示"更動洗衣折扣率, 明細會重新計算, 是否執行"提示'
                )

            with allure.step("And 點擊[確定]"):
                web.tip_component.click_ok().sleep(1)
                web.athena_base_page.screenshot("And 點擊[確定]")

        with allure.step("And 點擊[橘色磁碟片]進行儲存"):
            # row 重算欄位須在存檔前讀（save 後 row commit、編輯態 input 即消失）
            row_values = {
                field: web.housekeeping_account_page.get_row_field(field)
                for field in (
                    "discRate",
                    "discAmount",
                    "specialAmount",
                    "specialServ",
                    "totalAmount",
                )
            }
            web.housekeeping_account_page.save_housekeeping_setting()
            web.athena_base_page.sleep(1)
            web.athena_base_page.screenshot("And 點擊[橘色磁碟片]進行儲存")

        with allure.step('Then 顯示"儲存成功"提示'):
            tip_text = web.tip_component.get_tip_text()
            web.athena_base_page.assert_data("儲存成功提示", "儲存成功" in tip_text, True)
            web.athena_base_page.screenshot('Then 顯示"儲存成功"提示')
            web.tip_component.click_ok().sleep(1)

        with allure.step("Then 「合計」欄位顯示總計數值"):
            # row 重算欄位對帳（公式：disc=單價×qty×率、小計=單價×qty−disc、服務費=單價×10% 不折）
            web.athena_base_page.assert_data(
                "折扣額", float(row_values["discAmount"]), float(data["expected_disc"])
            )
            web.athena_base_page.assert_data(
                "小計", float(row_values["specialAmount"]), float(data["expected_subtotal"])
            )
            web.athena_base_page.assert_data(
                "服務費", float(row_values["specialServ"]), float(data["expected_service"])
            )
            web.athena_base_page.assert_data(
                "入帳總額", float(row_values["totalAmount"]), float(data["expected_total"])
            )
            # total 合計：本次 dialog 新增累計（重開歸零），存檔後才同步
            web.athena_base_page.assert_data(
                "合計欄位",
                float(web.housekeeping_account_page.get_total()),
                float(data["expected_total"]),
            )
            # keyNos：存檔後帶入的房務入帳編號（如 HK33）
            web.athena_base_page.assert_data(
                "房務入帳編號", web.housekeeping_account_page.get_key_nos().startswith("HK"), True
            )
            if data.get("clear_rates"):
                # 清空留白儲存：系統存檔時自動歸 0（不擋存、無重算 alert）
                web.athena_base_page.assert_data(
                    "清空折扣率存檔後歸零",
                    web.housekeeping_account_page.get_discount_rate("minibar"),
                    "0",
                )
            web.athena_base_page.screenshot("Then 「合計」欄位顯示總計數值")

        with allure.step("Postcondition 關閉「房務帳資料編輯」視窗"):
            # dialog 與功能選項 panel 須連續關閉（隔操作後 close icon 轉 hidden 擋全頁）
            web.room_control_page.close_housekeeping_dialogs().sleep(1)
            web.athena_base_page.screenshot("Postcondition 關閉「房務帳資料編輯」視窗")

        with allure.step("Postcondition 帳夾1顯示房務入帳之消費項目資料條"):
            web.header_component.expand_menu("出納").sleep(1)
            web.header_component.to_func_page("住客帳維護").sleep(1)
            web.guest_account_page.search_room(room).sleep(1)
            web.guest_account_page.click_card_row(room).sleep(0.5)
            web.guest_account_page.click_guest_maintain().sleep(1)
            if web.athena_base_page.has_element(web.guest_account_page.locator.dialog_shift):
                ShareSteps.open_shift(web, "FO : 飯店櫃檯", "a", "autotest")
                web.athena_base_page.sleep(1)
            # acct_nos diff 鎖定本次新增（累積制卡「驗有資料」會撞歷史筆），再對 item_nam 與金額
            acct_nos_after = web.co_list_page.get_folio_acct_nos("1")
            new_acct_nos = acct_nos_after - acct_nos_before
            items = web.co_list_page.get_folio_items_by_acct_nos("1", new_acct_nos)
            web.athena_base_page.assert_data("新增消費筆數", len(items), 2)
            web.athena_base_page.assert_data(
                "新增消費項目", sorted(nam for nam, _ in items), data["expected_folio_items"]
            )
            web.athena_base_page.assert_data(
                "新增消費金額總和", sum(tot for _, tot in items), data["expected_total"]
            )
            web.athena_base_page.screenshot("Postcondition 帳夾1顯示房務入帳之消費項目資料條")
