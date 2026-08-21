from selenium.webdriver.common.by import By
from locators.base_locator import BaseLocator


class CheckInListLocator(BaseLocator):

    # ----- 搜尋區 -----
    btn_search = (By.XPATH, "//div[@data-field-id='searchButton']//button")
    btn_dropdown = (By.XPATH, "//div[@data-field-id='dropdownButton']//button")
    input_room_nos = (By.XPATH, "//div[@data-field-id='roomNos']//input")

    # ----- 篩選（dropdownButton 展開後） -----
    col_checkin_status = (By.XPATH, "//div[@data-field-id='checkinStatus']")
    option_checkin_status = (By.XPATH, "//li[normalize-space()='%s']")

    # ----- 操作列 -----
    btn_check_in = (By.XPATH, "//div[@data-field-id='r_1010']//button")
    btn_cancel_check_in = (By.XPATH, "//div[@data-field-id='r_1020']//button")

    # ----- Grid -----
    cell_room_nos = (By.XPATH, "//td[@field='roomNos' and normalize-space()='%s']")
    text_order_status_by_room = (
        By.XPATH,
        "//tr[.//td[@field='roomNos' and normalize-space()='%s']]//td[@field='orderStatus']",
    )

    # ----- Check In Dialog（入住） -----
    checkbox_not_ci = (By.XPATH, "//div[@id='NotCiPanel']//input[@name='form-field-checkbox']")
    btn_do_check_in = (By.XPATH, "//button[@data-field-id='r_1011']")
    btn_make_card_new = (By.XPATH, "//button[normalize-space()='新卡']")
    btn_close_make_card_dialog = (By.XPATH, "(//a[contains(@class,'panel-tool-close')])[last()]")
    btn_close_check_in_dialog = (
        By.XPATH,
        "(//div[contains(@class,'panel-title') and contains(.,'check In')]"
        "/..//a[contains(@class,'panel-tool-close')])[last()]",
    )

    # ----- Check In Dialog（取消入住） -----
    checkbox_cancel_ci = (By.XPATH, "(//input[@name='form-field-checkbox'])[1]")
    btn_do_cancel_check_in = (By.XPATH, "//button[@data-field-id='r_1021']")
    label_cancel_assign = (
        By.XPATH,
        "(//label[contains(@class,'checkbox') and contains(.,'取消排房')])[last()]",
    )
    label_dirty_room = (
        By.XPATH,
        "(//label[contains(@class,'checkbox') and contains(.,'改成髒房')])[last()]",
    )
    btn_confirm = (By.XPATH, "//button[normalize-space()='確定']")
