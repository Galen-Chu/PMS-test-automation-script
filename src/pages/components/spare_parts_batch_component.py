from pages.base_page import BasePage
from locators.spare_parts_batch_locator import SparePartsBatchLocator


class SparePartsBatchComponent(BasePage):

    def __init__(self, driver):
        super().__init__(driver, SparePartsBatchLocator())

    def create_batch_spare(self, batch_spare_option):
        self.click(self.locator.batch_spare_dropdown)
        self.sleep(1)
        batch_spare_option_locator = self.formator_locator(
            self.locator.batch_spare_options, batch_spare_option
        )
        self.click(batch_spare_option_locator)
        input_batch_spare_locator = self.formator_locator(
            self.locator.input_batch_spare_by_label, "amount"
        )
        self.input(input_batch_spare_locator, "1")
        self.click(self.locator.btn_batch_spare)
        return self

    def click_checkbox_in_guest(self):
        self.click(self.locator.checkbox_guest)
        return self

    def click_save_batch_spare(self):
        self.click(self.locator.btn_save_batch_spare)
        return self

    def get_batch_spare_info(self, field):
        batch_spare_info_locator = self.formator_locator(
            self.locator.text_batch_spare_by_label, field
        )
        batch_spare_info = self.driver.find_element(*batch_spare_info_locator).text
        return batch_spare_info
