from pages.dialogs.lost_item_dialog import LostItemDialog
from locators.lost_management_locator import LostManagementLocator


class LostManagementPage(LostItemDialog):

    def __init__(self, driver):
        super().__init__(driver)
        self.locator = LostManagementLocator()

    def click_first_row(self, row=0):
        locator_by_row = self.formator_locator(self.locator.text_data_in_page, (row, "code"))
        self.click(locator_by_row)

    def click_check_box_by_row(self, row):
        locator_by_row = self.formator_locator(self.locator.text_data_in_page, (row, "ck"))
        self.click(locator_by_row)
        return self

    def select_status_from_page(self, status):
        close_btn = self.driver.find_element(*self.locator.status_close)
        self.driver.execute_script("arguments[0].click();", close_btn)
        self.select("狀態", status)
        return self

    def search_lost_item(self, lost_item_data, status):
        self.clear()
        search_locator = self.formator_locator(self.locator.input_condition, "失物編號")
        self.input_with_clear(search_locator, lost_item_data)
        self.select_status_from_page(status)
        self.search()
        return self

    def get_lost_item_data_from_page(self, data, row=0):
        data_locator = self.formator_locator(self.locator.text_data_in_page, (row, data))
        lost_item_data = self.driver.find_element(*data_locator).text
        return lost_item_data

    def get_rent_day(self):
        rent_day_element = self.driver.find_element(*self.locator.rent_day)
        rent_day = rent_day_element.get_attribute("value")
        return rent_day
