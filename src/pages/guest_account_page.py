from time import sleep
from selenium.webdriver.common.by import By
from pages.athena_base_page import AthenaBasePage
from locators.guest_account_locator import GuestAccountLocator


class GuestAccountPage(AthenaBasePage):

    def __init__(self, driver):
        super().__init__(driver, GuestAccountLocator())

    def set_condition_value(self, field, value):
        locator_input = self.formator_locator(self.locator.input_condition, field)
        self.input(locator_input, value)
        return self

    def click_guest_maintain(self):
        self.click(self.locator.btn_guest_maintain)
        return self

    def click_credit(self):
        self.click(self.locator.btn_credit)
        return self

    def select_consumption_code(self, value):
        self.click(self.locator.select_consumption)
        sleep(3)
        locator_select_option = self.formator_locator(self.locator.select_option, value)
        self.click(locator_select_option)
        return self

    def set_amount(self, value):
        self.input(self.locator.input_amount, value)
        return self

    def get_guest_maintain_info(self, field):
        locator_guest_info = self.formator_locator(self.locator.label_deposit, field)
        return self.driver.find_element(*locator_guest_info).get_attribute("value")

    def get_deposit_info(self, field):
        locator_deposit_info = self.formator_locator(self.locator.td_deposit_info, field)
        return self.driver.find_element(*locator_deposit_info).text

    def click_item_detail(self):
        self.click(self.locator.btn_item_detail)
        return self

    def get_input_values(self, label):
        text_input_values = self.formator_locator(self.locator.text_input_values, label)
        elements = self.driver.find_elements(*text_input_values)
        input_value = "".join([str(element.text) for element in elements])
        return input_value

    def get_input_value(self, label):
        text_input_value = self.formator_locator(self.locator.text_input_value, label)
        return self.driver.find_element(*text_input_value).text

    def get_row_item(self, row, label):
        row_item = self.formator_locator(self.locator.row_item, (row, label))
        return self.driver.find_element(*row_item).text

    def add_pay_type(self):
        self.click(self.locator.btn_add_checkout_type)
        return self

    def click_checkout_more(self):
        self.click(self.locator.btn_checkout_more)
        return self

    def get_table_column_values(self, th_name):
        row_in_table = self.formator_locator(self.locator.row_in_table, th_name)
        th_position = self.formator_locator(self.locator.th_position, th_name)

        rows = self.driver.find_elements(*row_in_table)
        position = len(self.driver.find_elements(*th_position))
        return [row.find_elements(By.XPATH, "td")[position].text.strip() for row in rows]

    def get_uni_cod(self):
        return self.driver.find_element(*self.locator.text_uni_cod).get_attribute("value")
