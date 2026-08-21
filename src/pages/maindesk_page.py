from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage


class MaindeskPage(BasePage):
    # ----- 多筆頁面 -----
    def click_room_status_tag(self, tag):
        tmp_locator = self.formator_locator(self.locator.room_status_tag, tag)
        self.click(tmp_locator)
        return self

    def click_floor(self, floor):
        tmp_locator = self.formator_locator(self.locator.floor, floor)
        self.click(tmp_locator)
        return self

    def click_first_room(self):
        self.click(self.locator.first_room)
        return self

    def get_room_stay_days(self):
        return self.driver.find_element(*self.locator.room_stay_days).text

    def get_room_number(self):
        return self.driver.find_element(*self.locator.room_number).text

    def get_room_style(self):
        return self.driver.find_element(*self.locator.room_style).text

    def get_room_guest_name(self):
        return self.driver.find_element(*self.locator.room_guest_name).text

    # ----- 多筆頁面 End -----

    # ----- 內部共用方法 -----
    def _get_input_value(self, field):
        tmp_locator = self.formator_locator(self.locator.input_by_label, field)
        return self.driver.find_element(*tmp_locator).get_attribute("value")

    def _click_span_button(self, field):
        tmp_locator = self.formator_locator(self.locator.btn_guest_function_span, field)
        return self.click(tmp_locator)

    # ----- 內部共用方法 End -----

    # ----- 房間單筆 -----
    def click_toolbar_button_roomdetail(self, text):
        """點擊綜合櫃台工具列按鈕"""
        tmp_locator = self.formator_locator(self.locator.button_by_text, text)
        self.click(tmp_locator)
        return self

    def click_guest_function_roomdetail(self, function):
        """點擊房間細節顧客功能按鈕"""
        tmp_locator = self.formator_locator(self.locator.btn_guest_function_maindesk, function)
        self.click(tmp_locator)
        return self

    def click_add_guest(self):
        self._click_span_button("appendSingleRow")
        return self

    def click_edit_button(self, field):
        tmp_locator = self.formator_locator(self.locator.btn_edit_field, field)
        self.click(tmp_locator)
        return self

    def click_edit_card_nos_button(self):
        self._click_span_button("openCarNosDialog")
        return self

    def input_car_nos(self, car_nos):
        self.input_with_clear(self.locator.carNos_textarea, car_nos)
        return self

    def input_guest_remark(self, guest_remark):
        self.input_with_clear(self.locator.guest_remark_column, guest_remark)
        return self

    def input_guest_name(self, guest_name):
        self.input(self.locator.guest_row_field, guest_name)
        self.input(self.locator.guest_row_field, Keys.ENTER)
        return self

    def click_dropdown_guest(self, guest_name):
        tmp_locator = self.formator_locator(
            self.locator.text_by_field_then_text, ("alt_nam", guest_name)
        )
        self.click(tmp_locator)
        return self

    def select_stay_days(self, day):
        self.click(self.locator.days_dropdown)
        tmp_locator = self.formator_locator(self.locator.days_options, (day, day))
        self.click(tmp_locator)
        return self

    def has_profile_note(self):
        return self.driver.find_elements(*self.locator.check_precredit)

    def get_room_mn_text(self, field):
        return self._get_input_value(field)

    def get_notice_content(self):
        notice_content = self.driver.find_element(*self.locator.notice_content_text).get_attribute(
            "value"
        )
        return notice_content

    def get_roomdetail_guest_name(self):
        guest_name = self.driver.find_element(*self.locator.guest_row_field).get_attribute("value")
        return guest_name

    def get_maindesk_precredit_amount(self):
        guest_name = self.driver.find_element(*self.locator.text_precredit_amount).text
        return guest_name

    def get_room_dt_row_text(self, field):
        tmp_locator = self.formator_locator(self.locator.text_in_room_dt_row, field)
        return self.driver.find_element(*tmp_locator).text

    def get_guest_remark(self):
        return self.driver.find_element(*self.locator.guest_remark_column).get_attribute("value")

    # ----- 房間單筆 End -----

    # ----- 改退房日 視窗 -----
    def select_date_by_field(self, date_field, year, month, day):
        """根據欄位名稱選擇日期（改退房日視窗專用）"""
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

    def click_room_checkbox(self):
        self.click(self.locator.room_checkbox_in_table)
        return self

    # ----- 改退房日 視窗 End -----

    # ----- 換房價 視窗 -----
    def click_save_rate_code_change(self):
        self.click(self.locator.btn_save)
        return self

    def set_column_data(self, field, value):
        tmp_locator = self.formator_locator(self.locator.text_by_field, "rent_amt")
        self.click(tmp_locator)
        tmp_locator = self.formator_locator(self.locator.input_row_data, field)
        self.input_with_clear(tmp_locator, value)
        return self

    def get_header_text(self, field):
        return self._get_input_value(field)

    def select_use_cod(self, field, use_cod):
        tmp_locator = self.formator_locator(self.locator.select_dropdown_by_span, field)
        self.click(tmp_locator)
        tmp_locator = self.formator_locator(self.locator.select_option_by_combobox_item, use_cod)
        self.click(tmp_locator)
        return self

    # ----- 換房價 視窗 End -----

    # ----- 換房 視窗 -----
    def click_dirty_room_ck(self):
        self.click(self.locator.dirty_room_ck)
        return self

    # ----- 指定訂金 視窗 -----
    def clear_specify_deposit(self):
        tmp_locator = self.formator_locator(self.locator.input_dropdown_field, "訂金編號")
        self.input_clear(tmp_locator)
        return self

    def select_specify_deposit(self, value):
        tmp_locator = self.formator_locator(self.locator.input_dropdown_field, "訂金編號")
        self.input(tmp_locator, value)
        self.sleep(2)
        self.input(tmp_locator, Keys.ENTER)
        tmp_locator = self.formator_locator(self.locator.room_dt_row, f"000000{value}")
        self.click(tmp_locator)
        return self

    def get_specify_deposit_nos(self):
        return self._get_input_value("訂金編號")

    # ----- 指定公帳號 視窗 -----
    def is_master_room_exit(self):
        tmp_locator = self.formator_locator(self.locator.button_by_text, "取消公帳號")
        tmp_element = self.driver.find_elements(*tmp_locator)
        return tmp_element

    def select_first_master_room(self, value):
        tmp_locator = self.formator_locator(self.locator.input_dropdown_field, "公帳號")
        self.input(tmp_locator, value)
        self.sleep(2)
        self.input(tmp_locator, Keys.ENTER)
        self.click(self.locator.first_master_room)
        return self

    def get_specify_master_room(self):
        return self._get_input_value("公帳號")

    # ----- 注意事項 視窗 -----
    def input_note_content(self, value):
        self.input_with_clear(self.locator.notice_content_textarea, value)
        return self

    # ----- 預授權 視窗 -----
    def click_edit_precredit(self):
        self.click(self.locator.btn_edit_precredit)
        return self

    # ----- 車號 視窗 -----
    def get_car_nos(self):
        tmp_locator = self.formator_locator(self.locator.input_by_data_field_id, "carNos")
        return self.driver.find_element(*tmp_locator).get_attribute("value")

    def click_confirm_button(self):
        tmp_locator = self.formator_locator(self.locator.button_by_text, "確定")
        self.click(tmp_locator)
        return self
