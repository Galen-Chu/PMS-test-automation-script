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
