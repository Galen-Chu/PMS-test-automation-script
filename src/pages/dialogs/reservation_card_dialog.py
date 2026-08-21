import re
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage


class ReservationCardDialog(BasePage):

    # ----- 訂房卡共用 (多筆、單筆) -----
    def click_btn_add(self):
        self.click(self.locator.btn_add)
        return self

    def input_textarea(self, value):
        self.input(self.locator.textarea, value)
        return self

    def get_row_text(self, field):
        tmp_locator = self.formator_locator(self.locator.text_by_td_field, field)
        self.click(tmp_locator)
        return self.driver.find_element(*tmp_locator).text

    # ----- 訂房卡共用 (多筆、單筆)  End -----

    # ----- 訂房卡 多筆頁面 -----
    def click_edit_reservation_card(self):
        self.click(self.locator.btn_edit)
        return self

    def search_reservation_card(self, condition, value):
        btn_clear = self.formator_locator(self.locator.btn_search_toolbar, "clear")
        self.click(btn_clear)
        search_contdtion = self.formator_locator(self.locator.input_by_condition, condition)
        self.input(search_contdtion, value)
        btn_search = self.formator_locator(self.locator.btn_search_toolbar, "search")
        self.click(btn_search)
        return self

    def has_reservation_card(self):
        msg = self.driver.find_element(*self.locator.empty_msg).text
        if msg == "無任何資料":
            return False
        return True

    # ----- 訂房卡 多筆頁面 End -----

    # ----- 訂房卡 單筆視窗 -----
    def click_card_toolbar(self, toolbar):
        btn_reservation_detail = self.formator_locator(self.locator.btn_card_toolbar, toolbar)
        self.click(btn_reservation_detail)
        return self

    def click_deposit_setting(self):
        self.click(self.locator.btn_deposit_setting)
        return self

    def click_edit_rate_cod(self):
        self.click(self.locator.btn_select_rate_code)
        return self

    def set_rate_code(self, rate_cod_name, room_type):
        rate_cod_locator = self.formator_locator(
            self.locator.select_rate_code, (rate_cod_name, room_type)
        )
        self.click(rate_cod_locator)
        self.click_toolbar_item_2("確定")
        return self

    def set_rate_code_by_search_name(self, rate_cod_name, room_type):
        self.click(self.locator.btn_select_rate_code)
        self.input(self.locator.input_rate_cod_name, rate_cod_name)
        self.sleep(1)
        self.input(self.locator.input_rate_cod_name, Keys.ENTER)
        rate_cod_locator = self.formator_locator(
            self.locator.select_rate_code, (rate_cod_name, room_type)
        )
        self.click(rate_cod_locator)
        self.click_toolbar_item_2("確定")
        return self

    def get_link_nos(self):
        return self.driver.find_element(*self.locator.text_link_nos).text

    def get_text_in_tab(self, field):
        tmp_locator = self.formator_locator(self.locator.text_by_td_field, field)
        return self.driver.find_element(*tmp_locator).text

    # ----- 訂房卡 單筆視窗 End -----

    # ----- 訂房明細 視窗 -----
    def click_detail_toolbar(self, toolbar):
        btn_spare_spart = self.formator_locator(self.locator.btn_tool, toolbar)
        self.click(btn_spare_spart)
        return self

    def click_tab(self, tab_name):
        tab_locator = self.formator_locator(self.locator.tab_list, tab_name)
        self.click(tab_locator)
        return self

    def click_tab_toolbar(self, tab, toolbar):
        toolbar_locator = self.formator_locator(self.locator.toolbar_by_tab, (tab, toolbar))
        self.click(toolbar_locator)
        return self

    def click_tab_guest_function(self, function):
        function_locator = self.formator_locator(self.locator.tab_guest_function, function)
        self.click(function_locator)
        return self

    def click_edit_assign_notes(self):
        self.click(self.locator.btn_edit_assign_notes)
        return self

    def click_add_assign_notes(self):
        self.click(self.locator.btn_add_assign_notes)
        return self

    def click_save_assign_notes(self):
        self.click(self.locator.btn_save_assign_notes)
        return self

    def click_tab_add_btn(self, tab):
        tab_add_btn_locator = self.formator_locator(self.locator.btn_add_by_tab, tab)
        self.click(tab_add_btn_locator)
        return self

    def click_edit_guest(self):
        self.click(self.locator.btn_edit_guest)
        return self

    def click_tab_expense_rent(self):
        self.click(self.locator.tab_expense_rent)
        return self

    def select_guest_no_info(self, option):
        option_locator = self.formator_locator(self.locator.guest_no_info_option, option)
        self.click(option_locator)
        return self

    def is_guest_name_red(self):
        class_value = self.driver.find_element(*self.locator.guest_name_in_table).get_attribute(
            "class"
        )
        return "asiLock" in class_value

    def click_precredit(self):
        self.click(self.locator.tab_guest_precredit)
        return self

    def get_precredit_amount(self):
        return self.driver.find_element(*self.locator.tab_guest_precredit).text

    def get_guest_table_info_by_row(self):
        guest_name_list = []
        guest_info_locators = self.driver.find_elements(*self.locator.guest_name_in_table)
        for locator in guest_info_locators:
            guest_name_list.append(locator.text)
        return guest_name_list

    def get_guest_row_count(self):
        guest_count = len(self.driver.find_elements(*self.locator.tab_guest_table))
        return guest_count

    def get_all_guests_todo_status(self):
        todo_status_list = []
        todo_status_elements = self.driver.find_elements(*self.locator.tab_guest_function_status)
        for status_element in todo_status_elements:
            status = status_element.get_attribute("class")
            todo_status_list.append("check" in status)
        return todo_status_list

    def get_tab_service_info(self, field):
        tab_service_info = self.formator_locator(self.locator.tab_service_table, field)
        tab_service_info = self.driver.find_element(*tab_service_info).text
        return tab_service_info

    def get_tab_empty_msg(self, tab):
        empty_msg_locator = self.formator_locator(self.locator.empty_msg_by_tab, tab)
        return self.driver.find_element(*empty_msg_locator).text

    def get_tab_expense_info_in_row(self, date, field):
        tab_expense_info = self.formator_locator(self.locator.tab_expense_table, (date, field))
        tab_expense_info = self.driver.find_element(*tab_expense_info).text
        return tab_expense_info

    def get_tab_expense_info_by_date(self, date):
        expense_list = []
        expense_list_by_date = self.formator_locator(self.locator.tab_expense_list_by_date, date)
        expense_list_by_date = self.driver.find_elements(*expense_list_by_date)
        for item in expense_list_by_date:
            expense_list.append(item.text)
        return expense_list

    def get_expense_summary_info(self, field):
        expense_summary_info = self.formator_locator(
            self.locator.tab_expense_summary_section, field
        )
        expense_summary_info = self.driver.find_element(*expense_summary_info).get_attribute(
            "value"
        )
        return expense_summary_info

    def get_assign_notes(self):
        assign_notes_locator = self.locator.column_assign_notes
        assign_notes = self.driver.find_element(*assign_notes_locator).text
        return assign_notes

    # ----- 訂房明細 視窗 End -----

    # ----- 房間特色選單 視窗 -----
    def click_room_features(self, features):
        for feature in features:
            feature_locator = self.formator_locator(self.locator.select_room_features, feature)
            self.click(feature_locator)
        return self

    def unselect_room_features(self):
        checked_checkbox = self.driver.find_elements(*self.locator.checkbox_state)
        for checkbox in checked_checkbox:
            if checkbox.is_selected():
                checkbox = self.driver.find_element(*self.locator.checked_checkbox)
                checkbox.click()
        return self

    # ----- 房間特色選單 視窗 End -----

    # ----- 備品庫存查詢 視窗 -----
    def click_spare_parts_filter(self):
        self.click(self.locator.spare_parts_filter)
        return self

    def click_spare_parts_checkbox(self, target_num):
        spare_parts_checkboxes_element = self.driver.find_elements(
            *self.locator.spare_parts_checkboxes
        )
        selected_num = 0
        for checkbox in spare_parts_checkboxes_element:
            if selected_num == target_num:
                break
            checkbox.click()
            selected_num += 1
        return self

    def get_spare_parts_selected(self, target_num):
        selected_num = 0
        spare_parts_list = []
        spare_parts_selected_element = self.driver.find_elements(*self.locator.spare_parts_text)
        for element in spare_parts_selected_element:
            if selected_num == target_num:
                break
            spare_parts_list.append(element.text)
            selected_num += 1
        return spare_parts_list

    def get_spare_parts_search_result(self):
        spare_parts_search_result = self.driver.find_elements(
            *self.locator.spare_parts_search_result
        )
        spare_parts_list = []
        for item in spare_parts_search_result:
            item_text = item.text.strip()
            spare_parts_list.append(re.sub(r"\s*\(\d+\)$", "", item_text))
        return spare_parts_list

    # ----- 備品庫存查詢 視窗 End ----

    # ----- 團體名單 視窗 -----
    def click_move_guest(self, move_type):
        move_guest_locator = self.formator_locator(self.locator.btn_move_guest, move_type)
        self.click(move_guest_locator)
        return self

    def click_group_list_guest(self):
        self.click(self.locator.group_list_guest_checkbox)
        return self

    def click_group_list_row(self, row_num):
        group_list_row_locator = self.formator_locator(self.locator.group_list_row_by_num, row_num)
        self.click(group_list_row_locator)
        return self

    def get_group_list_row_info(self, row, field):
        group_list_row_locator = self.formator_locator(
            self.locator.group_list_row_by_field, (row, field)
        )
        group_list_row_info = self.driver.find_element(*group_list_row_locator).text
        return group_list_row_info

    # ----- 團體名單 視窗 End ----

    # ----- 備品資訊 視窗 -----
    def click_spare_parts_info_toolbar(self, toolbar):
        toolbar_locator = self.formator_locator(self.locator.btn_card_toolbar, toolbar)
        self.click(toolbar_locator)
        return self

    def get_info_in_spare_parts_info(self, field):
        info_locator = self.formator_locator(self.locator.text_batch_spare_by_label, field)
        info = self.driver.find_element(*info_locator).text
        return info

    # ----- 備品資訊 視窗 End -----

    # ----- notes 視窗 -----
    def click_add_notes(self):
        self.click(self.locator.btn_add_note)
        return self

    def click_remove_notes(self):
        self.click(self.locator.btn_remove_note)
        return self

    def get_notes_text(self):
        notes_info = self.driver.find_element(*self.locator.textarea).get_attribute("value")
        return notes_info

    # ----- notes 視窗 End -----

    # ----- 提醒事項 視窗 -----
    def input_reservation_remind_by_field(self, field_name, text):
        # 在指定提醒欄位輸入內容（支援：訂房提醒、入住提醒、其他提醒、退房提醒）
        remind_input_locator = self.formator_locator(
            self.locator.input_reservation_remind, field_name
        )
        self.input_with_clear(remind_input_locator, text)
        return self

    def get_reservation_remind_by_field(self, field_name):
        # 取得指定提醒欄位的內容（支援：訂房提醒、入住提醒、其他提醒、退房提醒）
        remind_input_locator = self.formator_locator(
            self.locator.input_reservation_remind, field_name
        )
        remind_content = self.driver.find_element(*remind_input_locator).get_attribute("value")
        return remind_content

    # ----- 提醒事項 視窗 End -----

    # ----- 房租細項 視窗 -----
    def get_expense_detail_data(self, row):
        data_list = []
        detail_locator = self.formator_locator(
            self.locator.expense_detail_colume_by_row_and_index, row
        )
        for data in self.driver.find_elements(*detail_locator):
            data_list.append(data.text)
        return data_list

    # ----- 房租細項 視窗 End -----

    # ----- 訂金單筆新增 視窗 -----
    def clear_deposit_nos(self):
        tmp_locator = self.formator_locator(self.locator.col_by_data_field_id, "depositNos")
        self.click(tmp_locator)
        self.sleep(1)
        self.click(tmp_locator)
        self.sleep(1)
        self.click(self.locator.btn_clear_depositNos)
        return self

    def select_deposit_no(self, deposit_no):
        """選擇已存在的訂金編號（下拉選單）"""
        tmp_locator = self.formator_locator(self.locator.col_by_data_field_id, "depositNos")
        self.click(tmp_locator)
        self.sleep(1)
        self.set_dropdown_filter(deposit_no).sleep(1)
        deposit_option = self.formator_locator(self.locator.select_option_dropdownbase, deposit_no)
        self.click(deposit_option)
        return self

    def select_invoice_method(self, field, invoice_method):
        """選擇發票開立方式（下拉選單）"""
        tmp_locator = self.formator_locator(self.locator.select_dropdown_by_span, field)
        self.click(tmp_locator)
        tmp_locator = self.formator_locator(
            self.locator.select_option_by_combobox_item, invoice_method
        )
        self.click(tmp_locator)
        return self

    def select_payment_method(self, payment_method):
        """選擇付款方式（下拉選單）"""
        self.click(self.locator.table_payment_method)
        payment_option = self.formator_locator(self.locator.select_option, payment_method)
        self.click(payment_option)
        return self

    def input_payment_amount(self, amount):
        """輸入金額"""
        self.input_with_clear(self.locator.input_payment_amount, amount)
        return self

    # ----- 訂金單筆新增/修改 視窗 End -----

    # ----- 公帳號相關 -----
    def check_use_folio(self):
        self.click(self.locator.checkbox_use_folio)
        return self

    def select_folio(self):
        self.click(self.locator.select_option_dropdownbase_first_item)
        return self

    # ----- 公帳號相關 End -----

    # ----- 關聯單號 -----
    def click_link_nos_button(self):
        """點擊[關聯單號]按鈕"""
        self.click(self.locator.btn_link_nos_dialog)
        return self

    def click_link_nos_add_button(self):
        """點擊[+]按鈕開啟新增關聯單號視窗"""
        self.click(self.locator.link_nos_add_button)
        return self

    def search_link_nos(self, ikey):
        """輸入訂房卡號進行查詢"""
        tmp_locator = self.formator_locator(self.locator.input_condition, "訂房卡號")
        self.input_with_clear(tmp_locator, ikey)
        self.click(self.locator.btn_search)
        return self

    def check_link_nos(self):
        """勾選查詢結果"""
        tmp_locator = self.formator_locator(self.locator.text_by_td_field, "ck")
        self.click(tmp_locator)
        return self

    def click_link_nos_remove(self):
        """點擊刪除"""
        self.click(self.locator.link_nos_remove_button)
        return self

    def get_link_nos_in_dialog(self):
        return self.driver.find_element(*self.locator.text_link_nos_in_dialog).get_attribute(
            "value"
        )

    def get_link_nos_row_data(self, row):
        row_data = []
        tmp_locator = self.formator_locator(self.locator.link_nos_row_data, row)
        row_data_elements = self.driver.find_elements(*tmp_locator)
        for data_element in row_data_elements:
            row_data.append(data_element.text)

        return row_data

    # ----- 關聯單號 End -----
