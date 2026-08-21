from time import sleep
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CheckInListPage(BasePage):

    def expand_filter(self):
        """展開下拉篩選欄位"""
        self.click(self.locator.btn_dropdown)
        return self

    def select_checkin_status(self, status):
        """選擇住客狀態篩選（如 'N:未入住'、'Y:已入住'、'all:全部'）"""
        self.click(self.locator.col_checkin_status)
        sleep(0.5)
        locator = self.formator_locator(self.locator.option_checkin_status, status)
        self.click(locator)
        return self

    def search_room(self, room_no):
        """輸入房號並搜尋"""
        self.input_with_clear(self.locator.input_room_nos, room_no)
        self.click(self.locator.btn_search)
        return self

    def click_room_row(self, room_no):
        """點選 Grid 中指定房號的資料列"""
        locator = self.formator_locator(self.locator.cell_room_nos, room_no)
        self.click(locator)
        return self

    def click_check_in(self):
        """點擊操作列「入住」按鈕，開啟 Check In Dialog"""
        self.click(self.locator.btn_check_in)
        return self

    def verify_checkbox_checked(self):
        """確認 NotCiPanel checkbox 已自動勾選"""
        element = self.driver.find_element(*self.locator.checkbox_not_ci)
        return element.get_attribute("checked") == "true"

    def click_do_check_in(self):
        """點擊 Dialog 內「入住」按鈕(r_1011)，執行入住"""
        self.click(self.locator.btn_do_check_in)
        return self

    def close_make_card_dialog(self):
        """關閉製卡 Dialog"""
        self.click(self.locator.btn_close_make_card_dialog)
        return self

    def close_check_in_dialog(self):
        """關閉 Check In Dialog（取消入住後 panel-title scope 的 close 可能 hidden）"""
        element = self.driver.find_element(*self.locator.btn_close_check_in_dialog)
        if element.is_displayed():
            element.click()
        else:
            # 取消入住後 close 按鈕 hidden，遍歷找第一個 visible 的 panel-tool-close
            close_locator = (By.XPATH, "//a[contains(@class,'panel-tool-close')]")
            elements = self.driver.find_elements(*close_locator)
            for el in elements:
                if el.is_displayed():
                    el.click()
                    break
        return self

    def get_order_status(self, room_no):
        """取得指定房號的 orderStatus 欄位文字"""
        locator = self.formator_locator(self.locator.text_order_status_by_room, room_no)
        return self.driver.find_element(*locator).text

    # ----- 取消入住流程 -----

    def click_cancel_check_in(self):
        """點擊操作列「取消入住」按鈕，開啟取消入住 Dialog"""
        self.click(self.locator.btn_cancel_check_in)
        return self

    def cancel_check_in(self):
        """執行取消入住完整流程（勾選 → r_1021 → 取消兩個 checkbox → 確定）"""
        # 勾選 checkbox
        element = self.driver.find_element(*self.locator.checkbox_cancel_ci)
        if element.get_attribute("checked") != "true":
            self.click(self.locator.checkbox_cancel_ci)
        # 點擊取消入住按鈕
        self.click(self.locator.btn_do_cancel_check_in)
        sleep(0.5)
        # 取消勾選「一併取消排房」（預設 checked，需取消）
        self._uncheck_label(self.locator.label_cancel_assign)
        # 取消勾選「房間改成髒房」（預設 checked，需取消）
        self._uncheck_label(self.locator.label_dirty_room)
        # 確定（多個同名按鈕，遍歷找 visible 的）
        self._click_visible_confirm()
        return self

    def _uncheck_label(self, locator):
        """取消勾選 Element UI checkbox（label click toggle），已取消則跳過"""
        element = self.driver.find_element(*locator)
        if "is-checked" in (element.get_attribute("class") or ""):
            self.click(locator)

    def _click_visible_confirm(self):
        """點擊可見的「確定」按鈕（頁面有多個同名 hidden 按鈕）"""
        elements = self.driver.find_elements(*self.locator.btn_confirm)
        for el in elements:
            if el.is_displayed():
                el.click()
                return
        raise RuntimeError("找不到可見的「確定」按鈕")
