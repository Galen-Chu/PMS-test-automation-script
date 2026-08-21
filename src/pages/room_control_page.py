from time import sleep
from pages.base_page import BasePage


class RoomControlPage(BasePage):

    def change_floor(self, floor):
        tmp_locator = self.formator_locator(self.locator.btn_change_floor, floor)
        self.click(tmp_locator)
        return self

    def choose_room(self, room_no):
        locator_room = self.formator_locator(self.locator.btn_room_no, room_no)
        self.click(locator_room)
        return self

    def get_room_status(self):
        element = self.driver.find_element(*self.locator.clean_status)
        return element.get_attribute("value")

    def get_room_color(self, room_no):
        element = self.formator_locator(self.locator.room_block, room_no)
        return self.driver.find_element(*element).get_attribute("style")

    def get_room_icon(self, room_no, icon_index):
        element = self.formator_locator(self.locator.room_icon, (room_no, icon_index))
        return self.driver.find_element(*element).get_attribute("class")

    def get_room_status_list(self):
        elements = self.driver.find_elements(*self.locator.room_status_list)
        return [element.text for element in elements]

    def check_room(self, room_no):
        locator_room = self.formator_locator(self.locator.room_checkbox, room_no)
        self.click(locator_room)
        return self

    def check_all_rooms(self):
        self.click(self.locator.checkbox_all_rooms)
        return self

    def filter_room_status(self, status):
        self.click(self.locator.select_room_status)
        sleep(1)
        locator_status = self.formator_locator(self.locator.select_room_status_item, status)
        self.click(locator_status)
        return self

    def close_clean_floor_dialog(self):
        self.click(self.locator.btn_close_clean_floor)
        return self

    def select_category(self, category):
        self.click(self.locator.select_category)
        sleep(1)
        locator_category = self.formator_locator(self.locator.select_category_item, category)
        self.click(locator_category)
        return self

    def select_date_by_label(self, label, year, month, day):
        locator_date = self.formator_locator(self.locator.date_by_label, label)
        self.click(locator_date)
        sleep(1)
        self.click(self.locator.date_title_year)
        locator_year = self.formator_locator(self.locator.date_year, year)
        self.click(locator_year)
        locator_month = self.formator_locator(self.locator.date_month, month)
        self.click(locator_month)
        locator_day = self.formator_locator(self.locator.date_day, day)
        self.click(locator_day)
        return self

    def input_reason(self, reason):
        self.input(self.locator.input_reason, reason)
        return self

    def save_repair_visit_changes(self):
        self.click(self.locator.btn_repair_visit_save)
        return self

    def has_use_date(self, room, date):
        locator_date = self.formator_locator(self.locator.date_by_room, (room, date))
        return self.has_element(locator_date)

    def has_use_reason(self, room, reason):
        locator_reason = self.formator_locator(self.locator.reason_by_room, (room, reason))
        return self.has_element(locator_reason)

    def set_reason_floor(self, reason):
        self.input_with_clear(self.locator.input_reason_floor, reason)
        return self

    def check_room_floor(self, room_no):
        locator_room = self.formator_locator(self.locator.checkbox_room_floor, room_no)
        self.click(locator_room)
        return self

    def get_error_rooms(self):
        elements = self.driver.find_elements(*self.locator.room_errors)
        return [element.text.split("在")[0].split("房號")[1] for element in elements]

    def get_room_repair_list(self):
        elements = self.driver.find_elements(*self.locator.room_repair_list)
        return [element.text for element in elements if element.text.strip() != ""]

    def check_room_repair_item(self, room_no):
        locator_room = self.formator_locator(self.locator.room_repair_list_item, room_no)
        self.click(locator_room)
        return self

    def change_room_repair_day(self, label, day):
        locator_date = self.formator_locator(self.locator.room_repair_datepicker, label)
        self.click(locator_date)
        sleep(1)
        locator_day = self.formator_locator(self.locator.room_repair_day, day)
        self.click(locator_day)
        return self

    def input_room_repair_reason(self, reason):
        self.input_with_clear(self.locator.room_repair_reason, reason)
        return self

    def save_room_repair(self):
        self.click(self.locator.room_repair_save)
        return self

    def check_all_room_repair(self):
        self.click(self.locator.room_repair_check_all)
        return self

    def input_defect_reason(self, reason):
        self.input_with_clear(self.locator.input_defect, reason)
        return self

    # 拆併床相關方法
    def check_bed_setup_room(self, room_no):
        """勾選拆併床設定Table中的房間"""
        locator_room = self.formator_locator(self.locator.checkbox_bed_setup_room, room_no)
        self.click(locator_room)
        return self

    def select_bed_setting(self, bed_setting):
        """選擇拆床、併床或無設定"""
        self.click(self.locator.select_bed_setting)
        sleep(1)
        locator_setting = self.formator_locator(self.locator.select_bed_setting_item, bed_setting)
        self.click(locator_setting)
        return self

    def save_bed_setup(self):
        """點擊橘色磁碟片儲存拆併床設定"""
        self.click(self.locator.btn_bed_setup_save)
        return self

    def get_bed_setup_status(self, room_no):
        """取得房間的拆併床設定狀態"""
        locator_status = self.formator_locator(self.locator.bed_setup_status, room_no)
        element = self.driver.find_element(*locator_status)
        return element.text

    def close_bed_setup_dialog(self):
        """關閉拆併床設定對話框"""
        self.click(self.locator.btn_close_bed)
        return self
