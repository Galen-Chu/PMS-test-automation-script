from selenium.webdriver.support.ui import WebDriverWait
from pages.athena_base_page import AthenaBasePage
from locators.group_management_locator import GroupManagementLocator


class GroupManagementPage(AthenaBasePage):

    def __init__(self, driver):
        super().__init__(driver, GroupManagementLocator())

    def search_by_master_nos(self, master_nos):
        self.input_with_clear(
            self.format_locator(self.locator.input_by_data_field_id, "master_nos"), master_nos
        )
        self.click(self.locator.btn_search)
        return self

    def click_group_row(self, master_nos):
        self.click(self.format_locator(self.locator.row_group, master_nos))
        return self

    def click_group_detail(self):
        self.click(self.format_locator(self.locator.button_by_text, "團體明細"))
        return self

    def click_change_co_date(self):
        self.click(self.format_locator(self.locator.button_by_text, "退房日期"))
        return self

    def select_new_co_date(self, day):
        self.click(self.format_locator(self.locator.input_by_data_field_id, "new_co_dat"))
        cell = self.format_locator(self.locator.cell_co_date, day)
        self.wait_visible(cell)
        self.click(cell)
        return self

    def click_save(self):
        self.click(self.format_locator(self.locator.btn_toolbar_with_icon, "save"))
        return self

    def get_eco_dat(self):
        return self.driver.find_element(*self.locator.text_eco_dat).text

    def wait_eco_dat_changed(self, before_value, timeout=10):
        # 改退房日 save 後 grid 刷新非同步；等值離開操作前舊值（刷新發生的訊號），
        # 不等期望值——值最終對不對由 assert 驗（real/expect 證據留在斷言層）
        WebDriverWait(self.driver, timeout).until(
            lambda d: d.find_element(*self.locator.text_eco_dat).text != before_value
        )

    def get_list_co_dat(self):
        return self.driver.find_element(*self.locator.text_list_co_dat).text

    def close_panel_by_title(self, title):
        self.click(self.format_locator(self.locator.btn_close_panel_by_title, title))
        return self

    # ----- 清子房間（#501）-----

    def has_ci_room(self, room_no):
        """已入住 tab 是否有指定房（#501 復原偵測 + Postcondition 移除驗證）。
        子房退房後從已入住 tab 移除 → find_elements 空。"""
        locator = self.format_locator(self.locator.checkbox_ci_sub_room, room_no)
        return len(self.driver.find_elements(*locator)) > 0

    def check_ci_sub_room(self, room_no):
        """勾選已入住 tab 指定子房（先查 checked，已勾則跳過避免取消）。"""
        locator = self.format_locator(self.locator.checkbox_ci_sub_room, room_no)
        if self.driver.find_element(*locator).get_attribute("checked") != "true":
            self.click(locator)
        return self

    def click_clean_sub_room(self):
        self.click(self.locator.btn_clean_sub_room)
        return self

    def check_err_dialog_ck(self):
        """勾選錯誤提示 dialog 內子房（先查 checked；dialog 只列錯誤子房，不用指定房號）。"""
        locator = self.locator.checkbox_err_dialog_ck
        if self.driver.find_element(*locator).get_attribute("checked") != "true":
            self.click(locator)
        return self

    def click_err_dialog_confirm(self):
        self.click(self.locator.btn_err_dialog_confirm)
        return self
