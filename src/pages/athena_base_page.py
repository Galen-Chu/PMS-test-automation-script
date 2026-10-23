from pages.base_page import BasePage


class AthenaBasePage(BasePage):
    """PMS(Athena) 專屬頁面基礎類別：工具列、ikey、下拉選單、日曆等共用 widget。

    泛用的 Selenium 操作（點擊、輸入、等待、斷言）在 BasePage；
    所有 PMS 頁面、元件與對話框繼承此類別。
    """

    # ----- Athena Base -----
    def expand_search_condition(self):
        self.click(self.locator.btn_condition)
        return self

    def select(self, field, value):
        locator_select_dropdown = self.formator_locator(self.locator.select_dropdown, field)
        self.click(locator_select_dropdown)
        locator_select_option = self.formator_locator(self.locator.select_option, value)
        self.wait_visible(locator_select_option)
        self.click(locator_select_option)
        return self

    def search(self):
        self.click(self.locator.btn_search)
        return self

    def has_toolbar_item(self, item, panel=None):
        if panel:
            locator_toolbar_item = self.formator_locator(
                self.locator.btn_toolbar_item_by_panel, (panel, item)
            )
        else:
            locator_toolbar_item = self.formator_locator(self.locator.btn_toolbar_item, item)
        return self.has_element(locator_toolbar_item)

    def toolbar_item_enabled(self, item, panel=None):
        if panel:
            locator_toolbar_item = self.formator_locator(
                self.locator.btn_toolbar_item_by_panel, (panel, item)
            )
        else:
            locator_toolbar_item = self.formator_locator(self.locator.btn_toolbar_item, item)
        return self.driver.find_element(*locator_toolbar_item).is_enabled()

    def click_toolbar_item(self, item, panel=None, toolbar=1):
        """toolbar=1: 標準 toolbar-list；toolbar=2: 最後一顆符合文字的按鈕（對話框/面板內工具列）"""
        if panel:
            locator_toolbar_item = self.formator_locator(
                self.locator.btn_toolbar_item_by_panel, (panel, item)
            )
        elif toolbar == 2:
            locator_toolbar_item = self.formator_locator(self.locator.btn_toolbar_item_2, item)
        else:
            locator_toolbar_item = self.formator_locator(self.locator.btn_toolbar_item, item)
        self.click(locator_toolbar_item)
        return self

    def click_toolbar_with_icon(self, icon, panel=None):
        if panel:
            locator_toolbar_item = self.formator_locator(
                self.locator.btn_toolbar_with_icon_by_panel, (panel, icon)
            )
        else:
            locator_toolbar_item = self.formator_locator(self.locator.btn_toolbar_with_icon, icon)
        self.click(locator_toolbar_item)
        return self

    def set_value_by_label(self, label, value):
        locator_input = self.formator_locator(self.locator.input_by_label, label)
        self.input(locator_input, value)
        return self

    def clear_value_by_label(self, label):
        locator_input = self.formator_locator(self.locator.input_by_label, label)
        self.input_clear(locator_input)
        return self

    def set_value_by_id(self, element_id, value):
        locator_input = self.formator_locator(self.locator.input_by_id, element_id)
        self.input_with_clear(locator_input, value)
        return self

    def set_value_by_data_field_id(self, data_field_id, value):
        locator_input = self.formator_locator(self.locator.input_by_data_field_id, data_field_id)
        self.input_with_clear(locator_input, value)
        return self

    def set_dropdown_filter(self, filter_text):
        self.input(self.locator.input_dropdown_filter, filter_text)
        return self

    def click_target_ikey(self, ikey, grid=1):
        """grid=1/2: ikey 欄位的兩種 DOM 型態；grid=3: cust_mn_show_cod 欄位"""
        if grid == 2:
            ikey_locator = self.locator.text_ikey_2
        elif grid == 3:
            ikey_locator = self.locator.text_ikey_3
        else:
            ikey_locator = self.locator.text_ikey
        locator_ikey = self.formator_locator(ikey_locator, ikey)
        self.click(locator_ikey)
        return self

    def click_by_data_field(self, data_field_id):
        tmp_locator = self.formator_locator(self.locator.col_by_data_field_id, data_field_id)
        self.click(tmp_locator)
        return self

    def get_by_data_field(self, data_field_id):
        tmp_locator = self.formator_locator(self.locator.col_by_data_field_id, data_field_id)
        return self.driver.find_element(*tmp_locator).text

    def has_target_ikey(self, ikey):
        locator_ikey = self.formator_locator(self.locator.text_ikey, ikey)
        return self.has_element(locator_ikey)

    def click_target_rate_cod(self, ikey):
        locator_ikey = self.formator_locator(self.locator.text_rate_cod, ikey)
        self.click(locator_ikey)
        return self

    def close_panel(self):
        self.click(self.locator.btn_close)
        return self

    def has_target_rate_cod(self, ikey):
        locator_ikey = self.formator_locator(self.locator.text_rate_cod, ikey)
        return self.has_element(locator_ikey)

    def get_displaying_items_count(self):
        count = self.driver.find_element(*self.locator.text_table_items_count).text
        return count.split("of ")[1].split(" items")[0]

    def get_field_text(self, field):
        tmp_locator = self.formator_locator(self.locator.text_by_field, field)
        return self.driver.find_element(*tmp_locator).text

    def get_dropdown_input_value(self, field):
        tmp_locator = self.formator_locator(self.locator.text_by_dropdown_input_value, field)
        return self.driver.find_element(*tmp_locator).text

    # 日曆操作
    def click_date_icon(self, date_icon):
        date_icon = self.formator_locator(self.locator.btn_date_icon, date_icon)
        self.click(date_icon)
        return self

    def select_date(self, year, month, day):
        year_locator = self.formator_locator(self.locator.date_cell_item, year)
        month_locator = self.formator_locator(self.locator.date_cell_item, month)
        dd_locator = self.formator_locator(self.locator.date_cell_item, day)
        self.click(self.locator.date_year_title)
        self.click(self.locator.date_year_title)
        self.wait_visible(year_locator)
        self.click(year_locator)
        self.wait_visible(month_locator)
        self.click(month_locator)
        self.wait_visible(dd_locator)
        self.click(dd_locator)
        return self
