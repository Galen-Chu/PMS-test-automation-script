from time import sleep
from pages.base_page import BasePage


class SharePanelComponent(BasePage):

    def click_panel_footer_btn(self, title, btn_name):
        locator_panel_confirm = self.formator_locator(
            self.locator.panel_footer_btn, (title, btn_name)
        )
        self.click(locator_panel_confirm)
        return self

    def click_panel_save(self, title):
        locator_panel_save = self.formator_locator(self.locator.panel_save, title)
        self.click(locator_panel_save)
        return self

    def select_by_panel(self, title, value):
        locator_panel_select = self.formator_locator(self.locator.panel_select, title)
        self.click(locator_panel_select)
        sleep(1)
        locator_select_option = self.formator_locator(self.locator.select_option, value)
        self.click(locator_select_option)
        return self

    def close_panel(self, title=None):
        if title:
            locator_panel_close = self.formator_locator(self.locator.btn_pnael_close, title)
            self.click(locator_panel_close)
        else:
            super().close_panel()
        return self

    def click_panel_function(self, title):
        locator_panel_function = self.formator_locator(self.locator.btn_panel_function, title)
        self.click(locator_panel_function)
        return self

    # ---- 提醒視窗 -----
    def get_remind_panel_content(self, remind_type):
        # 取得提醒彈窗中的提醒內容
        tmp_locator = self.formator_locator(self.locator.panel_remind_content, remind_type)
        tmp_elements = self.driver.find_elements(*tmp_locator)
        if tmp_elements:
            return tmp_elements[0].get_attribute("value")
        return False

    # ---- 開班 panel ----
    def select_by_label(self, label, value):
        locator_label_select = self.formator_locator(self.locator.label_select, label)
        self.click(locator_label_select)
        sleep(1)
        locator_select_option = self.formator_locator(self.locator.select_option, value)
        self.click(locator_select_option)
        return self

    def select_by_label_span(self, label, value):
        locator_label_select = self.formator_locator(self.locator.label_span_select, label)
        self.click(locator_label_select)
        sleep(1)
        locator_select_option = self.formator_locator(self.locator.label_span_select_item, value)
        self.click(locator_select_option)
        return self

    def select_by_label_span_3(self, label, value):
        locator_label_select = self.formator_locator(self.locator.label_span_select_3, label)
        self.click(locator_label_select)
        sleep(3)
        locator_select_option = self.formator_locator(self.locator.label_span_select_item_3, value)
        self.click(locator_select_option)
        return self

    def input_by_label_3(self, label, value):
        locator_label_input = self.formator_locator(self.locator.label_input_3, label)
        self.input(locator_label_input, value)
        return self

    def input_by_label_2(self, label, value):
        locator_label_input = self.formator_locator(self.locator.label_input_2, label)
        self.input(locator_label_input, value)
        return self

    def input_by_label(self, label, value):
        locator_label_input = self.formator_locator(self.locator.label_input, label)
        self.input(locator_label_input, value)
        return self

    def input_duration_by_label(self, label, duration: list[str]):
        locator_label_duration = self.formator_locator(self.locator.label_duration, label)
        elements = self.driver.find_elements(*locator_label_duration)
        index = 0
        for element in elements:
            element.clear()
            self.driver.execute_script(f"arguments[0].value = '{duration[index]}';", element)
            self.driver.execute_script(
                "arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", element
            )
            index += 1
        return self

    def get_value_by_label(self, label):
        locator_label_input = self.formator_locator(self.locator.label_input, label)
        return self.driver.find_element(*locator_label_input).get_attribute("value")

    def get_value_by_label_2(self, label):
        locator_label_input = self.formator_locator(self.locator.label_input_2, label)
        return self.driver.find_element(*locator_label_input).get_attribute("value")

    def get_value_by_label_3(self, label):
        locator_label_input = self.formator_locator(self.locator.label_input_3, label)
        return self.driver.find_element(*locator_label_input).get_attribute("value")

    def get_value_by_label_span(self, label):
        locator_label_input = self.formator_locator(self.locator.label_span_select_value, label)
        return self.driver.find_element(*locator_label_input).get_attribute("value")

    def get_value_by_label_span_3(self, label):
        locator_label_input = self.formator_locator(self.locator.label_span_select_value_3, label)
        return self.driver.find_element(*locator_label_input).text

    def get_is_enabled_by_label(self, label):
        locator_label_input = self.formator_locator(self.locator.label_input, label)
        return self.driver.find_element(*locator_label_input).is_enabled()

    def get_is_enabled_by_label_3(self, label):
        locator_label_input = self.formator_locator(self.locator.label_input_3, label)
        return self.driver.find_element(*locator_label_input).is_enabled()

    def get_is_enabled_by_checkbox(self, label):
        label_checkbox = self.formator_locator(self.locator.label_checkbox, label)
        return self.driver.find_element(*label_checkbox).is_enabled()

    def click_label_checkbox(self, label):
        label_checkbox = self.formator_locator(self.locator.label_checkbox, label)
        self.click(label_checkbox)
        return self

    # ---- 開班 panel END ----

    # ---- 使用期間 panel ----
    def click_panel_add(self, title):
        locator_panel_add = self.formator_locator(self.locator.panel_add, title)
        self.click(locator_panel_add)
        return self

    def click_column_by_header(self, header):
        locator_column = self.formator_locator(
            self.locator.input_column_by_header, (header, header)
        )
        self.click(locator_column)
        return self

    def select_multiple_item(self, items: list[str]):
        for item in items:
            locator_item = self.formator_locator(self.locator.drop_down_item, item)
            self.click(locator_item)
        return self

    def click_detail_tab(self, name):
        locator_tab = self.formator_locator(self.locator.detail_tab_name, name)
        self.click(locator_tab)
        return self

    def click_label_name(self, label):
        locator_label = self.formator_locator(self.locator.label_name, label)
        self.click(locator_label)
        return self

    def input_name_by_lang(self, lang, value):
        locator_input = self.formator_locator(self.locator.label_input_by_lang, lang)
        self.input(locator_input, value)
        return self

    def click_confirm(self):
        self.click(self.locator.btn_confirm)
        return self

    def has_cratecod_mn(self, value):
        locator_cratecod = self.formator_locator(self.locator.text_cratecod_mn, value)
        return self.has_element(locator_cratecod)

    def click_cratecod_mn(self, value):
        locator_cratecod = self.formator_locator(self.locator.text_cratecod_mn, value)
        self.click(locator_cratecod)
        return self
