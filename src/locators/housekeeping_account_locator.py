from selenium.webdriver.common.by import By
from locators.base_locator import BaseLocator


class HousekeepingAccountLocator(BaseLocator):

    # -----房務帳作業-----
    btn_add = (By.XPATH, "//div[@data-field-id='grid-add']")
    # -----房務帳作業 END-----

    # -----選擇班別-----
    dropdown_options = (By.XPATH, "//div[@data-field-id='%s']")  # rsptCode # shiftCode
    item_option = (By.XPATH, "//li[@data-value='%s']")
    confirm_button = (By.XPATH, "//div[@data-field-id='confirmButton']/button")
    # -----選擇班別 END-----

    # ----- 房務帳編輯資料 -----
    dropdown_room_nos = (By.XPATH, "//div[@data-field-id='roomNos']/span")
    item_room_nos = (By.XPATH, "//div[text()='%s']")
    btn_add_housekeeping = (
        By.XPATH,
        "//div[@class='e-dlg-header-content' and //child::div[text()='房務帳資料編輯']]\
                            /following-sibling::div//div[@class='sub-button--add']",
    )
    dropdown_type = (
        By.XPATH,
        "//span[@aria-labelledby='%s_hidden']/span",
    )  # smallType # productNos
    item_type_option = (By.XPATH, "//li[@role='option' and @data-value='%s']/span")  # H002 、 M001
    btn_save = (By.XPATH, "//div[@data-field-id='saveButton']")
    input_room_nos = (By.XPATH, "//span[@class='e-filter-parent']//input[@role='combobox']")
    # ----- 房務帳編輯資料 END-----

    # ----- 自 mainline 補入 (2026-11-09) -----
    dialog_shift = (By.XPATH, "//div[@data-field-id='confirmButton']//button")
    # -----選擇班別 END-----

    # ----- 房務帳編輯資料 -----

    btn_add_housekeeping = (
        By.XPATH,
        "//div[@class='e-dlg-header-content' and //child::div[text()='房務帳資料編輯']]\
                            /following-sibling::div//div[@class='sub-button--add']",
    )

    dropdown_type = (
        By.XPATH,
        "//span[@aria-labelledby='%s_hidden']/span",
    )  # smallType # productNos

    input_minibar_rate = (By.XPATH, "//div[@data-field-id='minibarDiscRate']//input")

    input_laundry_rate = (By.XPATH, "//div[@data-field-id='laundryDiscRate']//input")
    # row 編輯態欄位以 input id 直接讀取

    input_row_field = (
        By.XPATH,
        "//input[@id='%s']",
    )  # discRate / discAmount / specialAmount / specialServ / totalAmount

    input_total = (By.XPATH, "//div[@data-field-id='total']//input")

    input_key_nos = (By.XPATH, "//div[@data-field-id='keyNos']//input")
    # ----- 折扣率與驗證欄位（#292）END -----
