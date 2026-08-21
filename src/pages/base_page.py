from time import sleep
from ast import literal_eval
import allure
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    ElementNotInteractableException,
    NoSuchElementException,
    StaleElementReferenceException,
)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# pylint: disable=unused-import
from locators.header_locator import HeaderLocator
from locators.login_locator import LoginLocator
from locators.home_locator import HomeLocator
from locators.reservation_locator import ReservationLocator
from locators.housekeeping_account_locator import HousekeepingAccountLocator
from locators.share_panel_locator import SharePanelLocator
from locators.tip_locator import TipLocator
from locators.guest_account_locator import GuestAccountLocator
from locators.checkin_locator import CheckinLocator
from locators.company_panel_locator import CompanyPanelLocator
from locators.service_item_locator import ServiceItemLocator
from locators.rate_cod_locator import RateCodLocator
from locators.room_control_locator import RoomControlLocator
from locators.base_locator import BaseLocator
from locators.lost_management_locator import LostManagementLocator
from locators.reservation_card_locator import ReservationCardLocator
from locators.spare_parts_locator import SparePartsLocator
from locators.spare_parts_batch_locator import SparePartsBatchLocator
from locators.transport_services_locator import TransportServicesLocator
from locators.todolist_edit_locator import TodolistEditLocator
from locators.pre_credit_locator import PreCreditLocator
from locators.message_edit_locator import MessageEditLocator
from locators.room_assignment_locator import RoomAssignmentLocator
from locators.maindesk_locator import MaindeskLocator
from locators.check_in_list_locator import CheckInListLocator

# pylint: enable=unused-import


class BasePage:

    def __init__(self, driver):
        prefix = (
            type(self).__name__.replace("Page", "").replace("Component", "").replace("Dialog", "")
        )
        self.locator = globals()[f"{prefix}Locator"]
        self.driver = driver

    def formator_locator(self, locator, values):
        return literal_eval(str(locator) % values)

    def click(self, locator, retries=5, delay=1):
        for attempt in range(retries):
            try:
                element = self.driver.find_element(*locator)
                element.click()
                return  # 點擊成功就結束
            except (
                ElementClickInterceptedException,
                ElementNotInteractableException,
                NoSuchElementException,
                StaleElementReferenceException,
            ) as _:
                if attempt < retries - 1:
                    sleep(delay)
                else:
                    raise

    def clear(self):
        self.click(self.locator.btn_clear)
        return self

    def input_clear(self, locator):
        element = self.driver.find_element(*locator)
        element.send_keys(Keys.CONTROL, "a")
        element.send_keys(Keys.BACKSPACE)
        return self

    def input_with_clear(self, locator, value):
        element = self.driver.find_element(*locator)
        element.clear()
        element.send_keys(value)

    def input(self, locator, value):
        self.driver.find_element(*locator).send_keys(value)

    def pointer_to_element(self, locator):
        target_element = self.driver.find_element(*locator)
        actions = ActionChains(self.driver)
        actions.move_to_element(target_element).perform()

    def has_element(self, locator):
        try:
            self.driver.implicitly_wait(2)
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
        finally:
            self.driver.implicitly_wait(10)

    def wait_clickable(self, locator, timeout=10):
        WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))
        return self

    def wait_visible(self, locator, timeout=10):
        WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
        return self

    def wait_gone(self, locator, timeout=10):
        WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located(locator))
        return self

    def screenshot(self, file_name):
        if hasattr(self.driver, "get_screenshot_as_png"):
            allure.attach(
                self.driver.get_screenshot_as_png(), file_name, allure.attachment_type.PNG
            )
        return self

    def sleep(self, seconds):
        sleep(seconds)
        return self

    def assert_data(self, title, real, expect):
        allure.attach(
            f"Real: {real} , Expect: {expect}", f"實際結果-{title}", allure.attachment_type.TEXT
        )
        assert real == expect

    def assert_data_in_list(self, title, reals, expect):
        allure.attach(
            f"Real: {reals} , Expect: {expect}", f"實際結果-{title}", allure.attachment_type.TEXT
        )
        assert expect in reals

    def assert_data_not_in_list(self, title, reals, expect):
        allure.attach(
            f"Real: {reals} , Expected not to find: {expect}",
            f"實際結果-{title}",
            allure.attachment_type.TEXT,
        )
        assert expect not in reals

    def assert_data_has_count(self, title, real):
        allure.attach(f"Real: {real}", f"實際結果-{title}", allure.attachment_type.TEXT)
        assert int(real) > 0

    # ----- Athena Base -----
    def expand_search_condition(self):
        self.click(self.locator.btn_condition)
        return self

    def select(self, field, value):
        locator_select_dropdown = self.formator_locator(self.locator.select_dropdown, field)
        self.click(locator_select_dropdown)
        sleep(1)
        locator_select_option = self.formator_locator(self.locator.select_option, value)
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

    def click_toolbar_item(self, item, panel=None):
        if panel:
            locator_toolbar_item = self.formator_locator(
                self.locator.btn_toolbar_item_by_panel, (panel, item)
            )
        else:
            locator_toolbar_item = self.formator_locator(self.locator.btn_toolbar_item, item)
        self.click(locator_toolbar_item)
        return self

    def click_toolbar_item_2(self, item, panel=None):
        if panel:
            locator_toolbar_item = self.formator_locator(
                self.locator.btn_toolbar_item_by_panel, (panel, item)
            )
        else:
            locator_toolbar_item = self.formator_locator(self.locator.btn_toolbar_item_2, item)
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

    def click_target_ikey(self, ikey):
        locator_ikey = self.formator_locator(self.locator.text_ikey, ikey)
        self.click(locator_ikey)
        return self

    def click_target_ikey_2(self, ikey):
        locator_ikey = self.formator_locator(self.locator.text_ikey_2, ikey)
        self.click(locator_ikey)
        return self

    def click_target_ikey_3(self, ikey):
        locator_ikey = self.formator_locator(self.locator.text_ikey_3, ikey)
        self.click(locator_ikey)
        return self

    def click_by_data_field(self, data_field_id):
        tmp_locator = self.formator_locator(self.locator.col_by_data_field_id, data_field_id)
        self.click(tmp_locator)
        return self

    def get_by_data_field(self, data_field_id):
        tmp_locator = self.formator_locator(self.locator.col_by_data_field_id, data_field_id)
        self.click(tmp_locator)
        return self

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

    def get_diplaying_items_count(self):
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
