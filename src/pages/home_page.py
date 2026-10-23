from pages.base_page import BasePage
from locators.home_locator import HomeLocator


class HomePage(BasePage):

    def __init__(self, driver):
        super().__init__(driver, HomeLocator())

    def to_pms_page(self):
        self.click(self.locator.btn_pms)
        return self
