from time import sleep
from pages.base_page import BasePage
from locators.header_locator import HeaderLocator


class HeaderComponent(BasePage):

    def __init__(self, driver):
        super().__init__(driver, HeaderLocator())

    def expand_menu(self, func_name):
        tmp_locator = self.formator_locator(self.locator.btn_menu_item, func_name)
        self.click(tmp_locator)
        sleep(1)
        return self

    def to_func_page(self, func_name):
        tmp_locator = self.formator_locator(self.locator.btn_dropdown_item, func_name)
        self.click(tmp_locator)
        return self
