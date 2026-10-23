from pages.athena_base_page import AthenaBasePage
from locators.reservation_locator import ReservationLocator


class ReservationPage(AthenaBasePage):

    def __init__(self, driver):
        super().__init__(driver, ReservationLocator())

    def set_condition_value(self, field, value):
        locator_input = self.formator_locator(self.locator.input_condition, field)
        self.input(locator_input, value)
        return self

    def click_empty_room(self):
        self.click(self.locator.table_empty_pointer)
        return self

    def get_selected_room_no(self):
        return self.driver.find_element(*self.locator.text_selected_room).text.strip()

    def click_reservation(self):
        self.click(self.locator.btn_reservation)
        return self

    def click_edit_guest(self):
        self.click(self.locator.btn_edit_name)
        return self

    def select_company(self, company):
        tmp_locator = self.formator_locator(self.locator.company_selection, company)
        self.click(tmp_locator)
        return self

    def set_email(self, value):
        self.input(self.locator.input_email, value)
        return self

    def create_guest(self, first_name, last_name, salute, mobile):
        self.input(self.locator.input_first_name, first_name)
        self.input(self.locator.input_last_name, last_name)
        self.click(self.locator.input_first_name)
        self.input(self.locator.input_salute, ".")
        locator_option_salute = self.formator_locator(self.locator.option_salute, salute)
        self.click(locator_option_salute)
        self.input(self.locator.input_mobile, mobile)
        self.click(self.locator.btn_save_guest)
        self.click(self.locator.btn_save_guest)
        return self

    def save_card(self):
        self.click(self.locator.btn_save)
        return self

    def to_detail_tab(self):
        self.click(self.locator.tab_detail)
        return self

    def get_dialog_ikey(self):
        return self.driver.find_element(*self.locator.text_dialog_ikey).text

    def get_salute_code(self):
        return self.driver.find_element(*self.locator.text_salute_code).text

    def get_guest_info(self, field):
        locator_guest_info = self.formator_locator(self.locator.td_guest_info, field)
        return self.driver.find_element(*locator_guest_info).text

    def get_deposit_amo(self):
        return self.driver.find_element(*self.locator.text_deposit_amo).get_attribute("value")

    def has_guest_data_confirm_dialog(self):
        if self.driver.find_element(*self.locator.guest_data_confirm):
            return True
        return False

    # ----- 依房型訂房 -----
    def click_reservation_by_room_type(self):
        self.click(self.locator.btn_reservation_by_room_type)
        return self

    def click_btn_edit(self):
        self.click(self.locator.btn_edit_setting)
        return self

    def select_room_type_pointer(self, room_type):
        locator_room_type = self.formator_locator(self.locator.select_room_type, room_type)
        self.click(locator_room_type)
        return self

    def change_co_date(self, date):
        self.input_with_clear(self.locator.input_co_date, date)
        self.wait_clickable(self.locator.btn_save_setting)
        self.click(self.locator.btn_save_setting)
        return self

    def get_rent_total(self):
        return int(
            self.driver.find_element(*self.locator.input_rent_total)
            .get_attribute("value")
            .strip()
            .replace(",", "")
        )

    def get_rent_total_detail(self):
        self.click(self.locator.btn_rent_total_detail)
        self.wait_present(self.locator.text_rent_amounts)
        items = self.driver.find_elements(*self.locator.text_rent_amounts)
        amounts = [int(item.text.replace(",", "")) for item in items]
        return sum(amounts)

    def close_panel_by_title(self, title):
        locator_panel_close = self.formator_locator(self.locator.btn_panel_close, title)
        self.click(locator_panel_close)
        return self

    # ----- 依房型訂房 END -----

    def get_rent_day(self):
        rent_day_element = self.driver.find_element(*self.locator.rent_day)
        rent_day = rent_day_element.get_attribute("value")
        return rent_day
