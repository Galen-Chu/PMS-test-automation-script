from selenium.webdriver.common.by import By


class HeaderLocator:

    btn_menu_item = (By.XPATH, "//button[@data-dropdown='%s']")
    btn_dropdown_item = (
        By.XPATH,
        "//*[contains(@class, 'sub-menu-item') and normalize-space()='%s']",
    )
