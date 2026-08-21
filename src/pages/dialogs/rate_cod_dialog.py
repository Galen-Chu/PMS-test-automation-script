from time import sleep
from pages.base_page import BasePage


class RateCodDialog(BasePage):

    def click_add_use_date(self):
        self.click(self.locator.btn_add_use_date)
        return self

    def add_new_use_date(self):
        self.click(self.locator.btn_add_new_use_date)
        return self

    def click_date_icon(self, date_icon):
        date_icon = self.formator_locator(self.locator.btn_date_icon, date_icon)
        self.click(date_icon)
        return self

    def select_date(self, year, month, day):
        year_locator = self.formator_locator(self.locator.date_cell_item, year)
        month_locator = self.formator_locator(self.locator.date_cell_item, month)
        dd_locator = self.formator_locator(self.locator.date_cell_item, day)
        self.click(self.locator.date_year_title)
        sleep(1)
        self.click(self.locator.date_year_title)
        sleep(1)
        self.click(year_locator)
        sleep(1)
        self.click(month_locator)
        sleep(1)
        self.click(dd_locator)
        sleep(1)
        return self

    def click_data_field_id(self, data_id):
        select = self.formator_locator(self.locator.btn_by_id, data_id)
        self.click(select)
        return self

    def click_data_field_id_down(self, data_id):
        select = self.formator_locator(self.locator.btn_by_id_down, data_id)
        self.click(select)
        return self

    def select_multiple_item(self, items: list[str]):
        for item in items:
            locator_item = self.formator_locator(self.locator.select_item, item)
            self.click(locator_item)
        return self

    def click_tab(self, name):
        locator_tab = self.formator_locator(self.locator.tab_name, name)
        self.click(locator_tab)
        return self

    def input_values_by_row(self, tab_name, row, values):
        td_locators = self.formator_locator(self.locator.td_price, (tab_name, row))
        input_locators = self.formator_locator(self.locator.input_price, (tab_name, row))
        for index in range(1, 3):
            elements = self.driver.find_elements(*td_locators)
            elements[index].click()
            sleep(1)
            input_element = self.driver.find_element(*input_locators)
            input_element.send_keys(values[index - 1])
        return self

    def close_panel(self):
        self.click(self.locator.btn_pnael_close)
        return self

    def click_localization_ratecod(self):
        self.click(self.locator.btn_localization_ratecod)
        return self

    def input_name_by_lang(self, lang, value):
        btn_edit = self.formator_locator(self.locator.btn_edit_lang, lang)
        input_lang = self.formator_locator(self.locator.input_lang_col, lang)
        btn_save_lang = self.formator_locator(self.locator.btn_save_lang, lang)
        self.click(btn_edit)
        self.input_with_clear(input_lang, value)
        self.click(btn_save_lang)
        return self

    def click_lang_confirm(self):
        self.click(self.locator.btn_lang_confirm)
        return self

    def click_grid_add(self):
        self.click(self.locator.btn_grid_add)
        return self

    def click_charge_type(self):
        self.click(self.locator.select_charge_type)
        return self

    def get_service_types(self):
        elements = self.driver.find_elements(*self.locator.item_service_types)
        return [element.get_attribute("innerText") for element in elements]

    def input_sale_duration(self, duration: list[str]):
        self.click(self.locator.icon_sell_from_date)
        index = 0
        for date in duration:
            range_type = "left" if index == 0 else "right"
            date_title = self.formator_locator(self.locator.date_range_year_title, range_type)
            year_locator = self.formator_locator(
                self.locator.date_range_cell_item, (range_type, date.split("/")[0])
            )
            month_locator = self.formator_locator(
                self.locator.date_range_cell_item, (range_type, date.split("/")[1])
            )
            dd_locator = self.formator_locator(
                self.locator.date_range_cell_item, (range_type, date.split("/")[2])
            )
            self.click(date_title)
            sleep(1)
            self.click(date_title)
            sleep(1)
            self.click(year_locator)
            sleep(1)
            self.click(month_locator)
            sleep(1)
            self.click(dd_locator)
            sleep(1)
            index += 1
        return self

    def has_cratecod_mn(self, name):
        locator_cratecod_mn = self.formator_locator(self.locator.text_cratecod_mn, name)
        return self.has_element(locator_cratecod_mn)

    def click_cratecod_mn(self, name):
        locator_cratecod = self.formator_locator(self.locator.text_cratecod_mn, name)
        self.click(locator_cratecod)
        return self

    def add_service_item(self):
        self.click(self.locator.btn_add_service_item)
        return self

    def click_dropdown_all(self):
        self.click(self.locator.btn_dropdown_all)
        return self

    def select_dropdown_list(self, item_name):
        item = self.formator_locator(self.locator.label_span_select_item, item_name)
        self.click(item)
        return self

    def has_disable_grid(self):
        return self.has_element(self.locator.grid_disabled)

    def item_enabled(self, item):
        locator_toolbar_item = self.formator_locator(self.locator.btn_toolbar_item_by_panel, item)
        return self.driver.find_element(*locator_toolbar_item).is_enabled()
