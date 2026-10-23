from pages.athena_base_page import AthenaBasePage
from locators.checkin_locator import CheckinLocator


class CheckinPage(AthenaBasePage):

    def __init__(self, driver):
        super().__init__(driver, CheckinLocator())

    def click_dialog_checkin(self):
        self.click(self.locator.btn_dialog_checkin)
        return self
