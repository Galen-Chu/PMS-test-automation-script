from pages.base_page import BasePage
from locators.service_item_locator import ServiceItemLocator


class ServiceItemComponent(BasePage):

    def __init__(self, driver):
        super().__init__(driver, ServiceItemLocator())

    def click_service_dropdown(self, label_name):
        tmp_locator = self.formator_locator(self.locator.service_dropdown, label_name)
        self.click(tmp_locator)
        return self

    def select_dropdown_list(self, value):
        tmp_locator = self.formator_locator(self.locator.service_dropdown_list, value)
        self.click(tmp_locator)
        return self

    def input_service_column(self, column_name, value):
        tmp_locator = self.formator_locator(self.locator.input_service_columns, column_name)
        self.input_with_clear(tmp_locator, value)
        return self

    def input_days_setting(self, days):
        self.input_with_clear(self.locator.days_setting_column, days)
        return self

    def click_input_column(self, column_name):
        tmp_locator = self.formator_locator(self.locator.input_service_columns, column_name)
        self.click(tmp_locator)
        return self

    def click_start_date(self, day):
        tmp_locator = self.formator_locator(self.locator.start_date_datetable, day)
        self.click(tmp_locator)
        return self

    def click_end_date(self, day):
        tmp_locator = self.formator_locator(self.locator.end_date_datetable, day)
        self.click(tmp_locator)
        return self

    def click_confirm_days_setting(self):
        self.click(self.locator.btn_confirm_days_setting)
        return self

    def click_weekday_dropdown_column(self):
        self.click(self.locator.weekday_dropdown)
        return self

    def select_weekday_dropdown_list(self, weekday):
        tmp_locator = self.formator_locator(self.locator.weekday_dropdown_list, weekday)
        self.click(tmp_locator)
        return self

    def unitprice_disable(self):
        tmp_locator = self.formator_locator(self.locator.input_service_columns, "單價")
        return self.driver.find_element(*tmp_locator).get_attribute("aria-readonly")
