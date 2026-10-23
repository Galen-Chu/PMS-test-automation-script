from time import sleep
from pages.base_page import BasePage
from locators.housekeeping_account_locator import HousekeepingAccountLocator


class HousekeepingAccountPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver, HousekeepingAccountLocator())

    def add_housekeeping_account(self):
        self.click(self.locator.btn_add)
        return self

    def select_class(self, rspt_type, shift_code):
        dropdown_options = self.formator_locator(self.locator.dropdown_options, "rsptCode")
        self.click(dropdown_options)
        sleep(2)
        item_option = self.formator_locator(self.locator.item_option, rspt_type)
        self.click(item_option)

        dropdown_options = self.formator_locator(self.locator.dropdown_options, "shiftCode")
        self.click(dropdown_options)
        sleep(2)
        item_option = self.formator_locator(self.locator.item_option, shift_code)
        self.click(item_option)

        self.click(self.locator.confirm_button)
        return self

    def select_room_nos(self, room_no):
        self.click(self.locator.dropdown_room_nos)
        sleep(2)
        self.input(self.locator.input_room_nos, room_no)
        item_room_nos = self.formator_locator(self.locator.item_room_nos, room_no)
        self.click(item_room_nos)
        return self

    def add_housekeeping(self, small_type, product_nos):
        self.click(self.locator.btn_add_housekeeping)
        sleep(1)
        dropdown_type = self.formator_locator(self.locator.dropdown_type, "smallType")
        self.click(dropdown_type)
        sleep(1)
        item_type_option = self.formator_locator(self.locator.item_type_option, small_type)
        self.click(item_type_option)
        dropdown_type = self.formator_locator(self.locator.dropdown_type, "productNos")
        self.click(dropdown_type)
        sleep(1)
        item_type_option = self.formator_locator(self.locator.item_type_option, product_nos)
        self.click(item_type_option)
        self.click(self.locator.btn_save_setting)
        return self

    def save_housekeeping_setting(self):
        self.click(self.locator.btn_save)
        return self

    def close_housekeeping_setting(self):
        self.click(self.locator.btn_close)
        return self
