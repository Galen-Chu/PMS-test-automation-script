from pages.base_page import BasePage


class RoomAssignmentPage(BasePage):

    def has_assign_rmk(self):
        assign_remark = self.driver.find_elements(*self.locator.assign_remark_icon)
        return len(assign_remark) > 0

    def select_room_no(self, room_no):
        tmp_locator = self.formator_locator(self.locator.select_room_no, room_no)
        self.click(tmp_locator)
        return self

    def get_text_in_detail_tab(self, field):
        tmp_locator = self.formator_locator(self.locator.text_in_detail_tab, field)
        return self.driver.find_element(*tmp_locator).get_attribute("value")

    def click_room_sta_checkbox(self):
        self.click(self.locator.check_room_sta)
        return self

    def click_lock_assignment_checkbox(self):
        self.click(self.locator.lock_assign_checkbox)
        return self

    def click_assignable_room_checkbox(self):
        self.click(self.locator.check_assignable_room)
        return self

    def get_biggraph_room_type(self, room_no):
        tmp_locator = self.formator_locator(self.locator.big_room_type, room_no)
        return self.driver.find_element(*tmp_locator).text

    def get_biggraph_date_range(self, room_no):
        tmp_locator = self.formator_locator(self.locator.big_room_date_range, room_no)
        return self.driver.find_element(*tmp_locator).text

    def is_room_nos_readonly(self):
        element = self.driver.find_elements(*self.locator.room_nos_readonly)
        return len(element) > 0

    def is_lock_assign_checked(self):
        return self.driver.find_element(*self.locator.checked_lock_assign_checkbox).is_selected()

    def search_ikey(self, ikey):
        tmp_locator = self.formator_locator(self.locator.input_condition, "訂房卡號")
        self.input(tmp_locator, ikey)
        self.search()
        return self
