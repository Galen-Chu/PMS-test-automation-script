from selenium.webdriver.common.by import By
from locators.base_locator import BaseLocator


class TodolistEditLocator(BaseLocator):
    department_dropdown = (
        By.XPATH,
        "//div[.//label[normalize-space()='處理部門']]//span[@class='textbox combo']",
    )
    department_options = (By.XPATH, "//div[text()='%s']")
    todolist_table = (
        By.XPATH,
        "(//tr[contains(@id,'toDoListDataGrid')]//td[@field='%s']/div)[last()]",
    )
    todolist_lastrow = (By.XPATH, "(//tr[contains(@id,'toDoListDataGrid')])[last()]")
