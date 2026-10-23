from selenium.webdriver.support.wait import WebDriverWait
from pages.base_page import BasePage
from locators.todolist_edit_locator import TodolistEditLocator


class TodolistEditComponent(BasePage):

    def __init__(self, driver):
        super().__init__(driver, TodolistEditLocator())

    def create_todo(self, departments):
        self.click(self.locator.department_dropdown)
        for department in departments:
            department_locator = self.formator_locator(self.locator.department_options, department)
            self.click(department_locator)
        return self

    def get_todolist_info(self, field):
        todolist_info = self.formator_locator(self.locator.todolist_table, field)
        WebDriverWait(self.driver, 2).until(
            lambda d: d.find_element(*todolist_info).text.strip() != ""
        )
        todolist_info = self.driver.find_element(*todolist_info).text
        return todolist_info

    def click_todoitem(self):
        self.click(self.locator.todolist_lastrow)
        return self
