from time import sleep
from pages.athena_base_page import AthenaBasePage
from locators.company_panel_locator import CompanyPanelLocator


class CompanyPanelComponent(AthenaBasePage):

    def __init__(self, driver):
        super().__init__(driver, CompanyPanelLocator())

    def get_td_input_value(self, field):
        tmp_locator = self.formator_locator(self.locator.td_input_value, field)
        return self.driver.find_element(*tmp_locator).text

    def click_add_contract(self):
        self.click(self.locator.btn_add_contract)
        return self

    def click_add_special_contract(self):
        self.click(self.locator.btn_add_special_contract)
        return self

    def click_remove_special_contract(self):
        self.click(self.locator.btn_rm_special_contract)
        return self

    def select_special_rate_cod(self, rate_cod):
        self.click(self.locator.select_special_rate_cod)
        sleep(2)
        tmp_rate_locator = self.formator_locator(self.locator.item_special_rate_cod, rate_cod)
        self.click(tmp_rate_locator)
        self.click(self.locator.confirm_button)
        return self

    def click_remove_contract(self):
        self.click(self.locator.btn_remove_contract)
        return self

    def click_target_contract(self):
        self.click(self.locator.btn_target_contract)
        return self

    # pylint: disable=too-many-positional-arguments
    def setting_contract(self, contract_no, start_date, end_date, hotel_cod, con_rate_cod):
        self.input(self.locator.input_contract_no, contract_no)
        self.select_start_day(start_date.split("/")[-1], "Jan")
        self.select_end_day(end_date.split("/")[-1], "Jan")
        self.click(self.locator.select_hotel_cod)
        sleep(2)
        tmp_hotel_locator = self.formator_locator(self.locator.item_cod, hotel_cod)
        self.click(tmp_hotel_locator)
        sleep(2)
        self.click(self.locator.select_rate_cod)
        sleep(2)
        tmp_rate_locator = self.formator_locator(self.locator.item_cod, con_rate_cod)
        self.click(tmp_rate_locator)
        return self

    def click_save(self):
        self.click(self.locator.btn_save)
        return self

    def select_start_day(self, day, month):
        self.click(self.locator.input_contract_start_date)
        self.click(self.locator.calendar_title)
        self.input_with_clear(self.locator.calendar_year, "2024")
        locator_month = self.formator_locator(self.locator.calendar_mon, month)
        self.click(locator_month)
        locator_day = self.formator_locator(self.locator.calendar_day, day)
        self.click(locator_day)
        return self

    def select_end_day(self, day, month):
        self.click(self.locator.input_contract_end_date)
        self.click(self.locator.calendar_title)
        self.input_with_clear(self.locator.calendar_year, "2024")
        locator_month = self.formator_locator(self.locator.calendar_mon, month)
        self.click(locator_month)
        locator_day = self.formator_locator(self.locator.calendar_day, day)
        self.click(locator_day)
        return self
