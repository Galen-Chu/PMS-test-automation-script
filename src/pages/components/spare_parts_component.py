from pages.athena_base_page import AthenaBasePage
from locators.spare_parts_locator import SparePartsLocator


class SparePartsComponent(AthenaBasePage):

    def __init__(self, driver):
        super().__init__(driver, SparePartsLocator())

    def check_spare_parts_exist(self):
        spare_parts_exist = self.driver.find_element(
            *self.locator.spare_parts_first_row
        ).get_attribute("style")
        if "height: 1px" in spare_parts_exist:
            return False
        return True

    def click_spare_parts_toolbar(self, toolbar):
        toolbar_locator = self.format_locator(self.locator.spare_parts_toolbar, toolbar)
        self.click(toolbar_locator)
        return self

    def click_add_spare_parts(self):
        self.click(self.locator.btn_add_spare_parts)
        return self

    def click_remove_spare_parts(self):
        self.click(self.locator.btn_remove_spare_parts)
        return self

    def click_spare_parts_row(self):
        self.click(self.locator.spare_parts_first_row)
        return self

    def create_spare_parts(self, spare_parts_option):
        spare_parts_dropdown = self.format_locator(
            self.locator.spare_parts_row_dropdown, "itemCode"
        )
        self.click(spare_parts_dropdown)
        spare_parts = self.format_locator(self.locator.spare_parts_options, spare_parts_option)
        self.click(spare_parts)
        return self

    def edit_spare_parts_end_date(self, field, month, day):
        date_dropdown = self.format_locator(self.locator.spare_parts_row_dropdown, field)
        self.click(date_dropdown)
        self.click(self.locator.calendar_title)
        self.input_with_clear(self.locator.input_year, "2024")
        month_locator = self.format_locator(self.locator.select_date, month)
        self.click(month_locator)
        day_locator = self.format_locator(self.locator.select_date, day)
        self.click(day_locator)
        return self

    def edit_spare_parts_amount(self, field, value):
        amount_locator = self.format_locator(self.locator.spare_parts_label, field)
        self.input_clear(amount_locator)
        self.input(amount_locator, value)
        return self

    def get_spare_parts_info(self, field):
        spare_parts_info = self.format_locator(self.locator.spare_parts_label, field)
        spare_parts_info = self.driver.find_element(*spare_parts_info).get_attribute("value")
        return spare_parts_info

    def get_spare_parts_table_info_by_date(self, date):
        table_info_list = []
        table_info_locator = self.format_locator(self.locator.spare_parts_table_by_date, date)
        table_info = self.driver.find_elements(*table_info_locator)
        for info in table_info:
            table_info_list.append(info.text)
        return table_info_list
