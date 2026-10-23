from pages.athena_base_page import AthenaBasePage
from locators.home_locator import HomeLocator


class HomePage(AthenaBasePage):

    def __init__(self, driver):
        super().__init__(driver, HomeLocator())

    def to_pms_page(self):
        self.click(self.locator.btn_pms)
        return self
