from pages.base_page import BasePage
from locators.checkin_locator import CheckinLocator


class CheckinPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver, CheckinLocator())

    def click_dialog_checkin(self):
        self.click(self.locator.btn_dialog_checkin)
        return self
