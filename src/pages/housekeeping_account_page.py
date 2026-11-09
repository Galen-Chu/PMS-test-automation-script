from pages.athena_base_page import AthenaBasePage
from locators.housekeeping_account_locator import HousekeepingAccountLocator


class HousekeepingAccountPage(AthenaBasePage):

    def __init__(self, driver):
        super().__init__(driver, HousekeepingAccountLocator())

    def add_housekeeping_account(self):
        self.click(self.locator.btn_add)
        return self

    def select_class(self, rspt_type, shift_code):
        dropdown_options = self.format_locator(self.locator.dropdown_options, "rsptCode")
        self.click(dropdown_options)
        item_option = self.format_locator(self.locator.item_option, rspt_type)
        self.wait_visible(item_option)
        self.click(item_option)

        dropdown_options = self.format_locator(self.locator.dropdown_options, "shiftCode")
        self.click(dropdown_options)
        item_option = self.format_locator(self.locator.item_option, shift_code)
        self.wait_visible(item_option)
        self.click(item_option)

        self.click(self.locator.confirm_button)
        return self

    def select_room_nos(self, room_no):
        self.click(self.locator.dropdown_room_nos)
        self.wait_visible(self.locator.input_room_nos)
        self.input(self.locator.input_room_nos, room_no)
        item_room_nos = self.format_locator(self.locator.item_room_nos, room_no)
        self.click(item_room_nos)
        return self

    def add_housekeeping(self, small_type, product_nos):
        self.click(self.locator.btn_add_housekeeping)
        dropdown_type = self.format_locator(self.locator.dropdown_type, "smallType")
        self.wait_visible(dropdown_type)
        self.click(dropdown_type)
        item_type_option = self.format_locator(self.locator.item_type_option, small_type)
        self.wait_visible(item_type_option)
        self.click(item_type_option)
        dropdown_type = self.format_locator(self.locator.dropdown_type, "productNos")
        self.click(dropdown_type)
        item_type_option = self.format_locator(self.locator.item_type_option, product_nos)
        self.wait_visible(item_type_option)
        self.click(item_type_option)
        self.click(self.locator.btn_save_setting)
        return self

    def save_housekeeping_setting(self):
        self.click(self.locator.btn_save)
        return self

    def close_housekeeping_setting(self):
        self.click(self.locator.btn_close)
        return self

    def clear_discount_rate(self, rate_type):
        """清空折扣率欄位留白（Ctrl+A+Backspace，不可 element.clear()——破壞 ej2）。

        清空後送 Enter 不觸發重算 alert（0→空不算 change），存檔時系統自動歸 0。
        """
        locator = (
            self.locator.input_minibar_rate
            if rate_type == "minibar"
            else self.locator.input_laundry_rate
        )
        element = self.driver.find_element(*locator)
        element.send_keys(Keys.CONTROL, "a")
        element.send_keys(Keys.BACKSPACE)
        return self

    def get_discount_rate(self, rate_type):
        """讀 dialog 折扣率欄位值（清空儲存變體驗系統存檔後歸 0）。"""
        locator = (
            self.locator.input_minibar_rate
            if rate_type == "minibar"
            else self.locator.input_laundry_rate
        )
        return self.driver.find_element(*locator).get_attribute("value")

    def get_key_nos(self):
        """讀存檔後帶入的房務入帳編號（如 HK33）。"""
        return self.driver.find_element(*self.locator.input_key_nos).get_attribute("value")

    def get_row_field(self, field):
        """讀編輯態 row 欄位值（discRate/discAmount/specialAmount/specialServ/totalAmount）。"""
        locator = self.format_locator(self.locator.input_row_field, field)
        return self.driver.find_element(*locator).get_attribute("value")

    def get_total(self):
        """讀 dialog 合計（本次 dialog 新增累計，重開歸零；存檔後才同步重算值）。"""
        return self.driver.find_element(*self.locator.input_total).get_attribute("value")

    def select_row_type(self, field, value):
        """開 row 欄位 DDL（smallType/productNos）並點選項（data-value 如 H002/M001）。
        productNos 選項依 smallType 過濾（H001→L 系列、H002→M 系列）。"""
        dropdown = self.format_locator(self.locator.dropdown_type, field)
        self.click(dropdown)
        sleep(1)
        item = self.format_locator(self.locator.item_type_option, value)
        self.click(item)
        return self

    def set_discount_rate(self, rate_type, rate):
        """填 dialog 折扣率（minibar/laundry）並送 Enter commit。

        type 完不觸發事件，須 Enter 才跳出「更動洗衣折扣率, 明細會重新計算」alert；
        文案固定為「洗衣」即使填的是 minibarDiscRate。
        """
        locator = (
            self.locator.input_minibar_rate
            if rate_type == "minibar"
            else self.locator.input_laundry_rate
        )
        # NumericTextBox 不可用 element.clear()（破壞 ej2 綁定，ENTER 不再觸發重算 alert）
        self.input_clear(locator)
        self.input(locator, str(rate))
        self.driver.find_element(*locator).send_keys(Keys.ENTER)
        return self
