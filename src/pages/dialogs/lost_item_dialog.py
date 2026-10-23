from time import sleep
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage
from locators.lost_item_locator import LostItemLocator


class LostItemDialog(BasePage):

    def __init__(self, driver):
        super().__init__(driver, LostItemLocator())

    def select_status_in_dialog(self, status):
        sleep(2)
        self.click(self.locator.status_dropdown)
        status_locator = self.formator_locator(self.locator.status_options, status)
        self.click(status_locator)
        return self

    def input_claim_note(self, value):
        self.input(self.locator.claim_note_field, value)
        return self

    def select_date(self, date_field, year, month, day):
        date_field_locator = self.formator_locator(self.locator.date_by_field, date_field)
        self.click(date_field_locator)
        self.click(self.locator.btn_date)
        locator_year = self.formator_locator(self.locator.date_year, year)
        self.click(locator_year)
        locator_mon = self.formator_locator(self.locator.date_mon, month)
        self.click(locator_mon)
        locator_day = self.formator_locator(self.locator.date_day, day)
        self.click(locator_day)
        return self

    def input_loser_name(self):
        self.click(self.locator.loser_name_dropdown)
        self.input(self.locator.loser_name_field, Keys.ENTER)
        sleep(1)
        self.click(self.locator.loser_name_options)
        return self

    def item_enabled(self, item):
        locator_toolbar_item = self.formator_locator(self.locator.btn_toolbar_with_icon, item)
        return self.driver.find_element(*locator_toolbar_item).is_enabled()

    def date_field_enabled(self, date):
        date_field = self.formator_locator(self.locator.date_by_field, date)
        return self.driver.find_element(*date_field).is_enabled()

    def loser_name_field_enabled(self):
        return self.driver.find_element(*self.locator.loser_name_field).is_enabled()

    def label_enabled(self, field):
        field_locator = self.formator_locator(self.locator.input_by_label, field)
        return self.driver.find_element(*field_locator).is_enabled()

    def get_lost_item_data_from_dialog(self, data):
        data_locator = self.formator_locator(self.locator.text_data_in_dialog, data)
        lost_item_data = self.driver.find_element(*data_locator).text
        return lost_item_data

    def get_field_value_in_dialog(self, field):
        field_locator = self.formator_locator(self.locator.input_by_label, field)
        field_element = self.driver.find_element(*field_locator)
        field_text = field_element.get_attribute("value")
        return field_text
