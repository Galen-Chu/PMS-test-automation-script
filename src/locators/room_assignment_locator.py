from selenium.webdriver.common.by import By
from locators.base_locator import BaseLocator


class RoomAssignmentLocator(BaseLocator):

    assign_remark_icon = (By.XPATH, "//td[@field='has_assign_rmk']//i")
    select_room_no = (
        By.XPATH,
        "(//div[@style='outline: none;']//div[@class='card-row']/span[text()='%s'])[last()]",
    )
    text_in_detail_tab = (
        By.XPATH,
        "//tr[contains(@id, 'OrderDtList')]//td[@field='%s']//span//input[@type='text']",
    )
    check_room_sta = (
        By.XPATH,
        "//tr[contains(@id, 'OrderDtList')]//td[@field='assign_sta_check']//input[@type='checkbox']",
    )
    lock_assign_checkbox = (By.XPATH, "//td[@field='asi_lock']//input[@type='checkbox']")
    checked_lock_assign_checkbox = (By.XPATH, "//td[@field='asi_lock']//input[@class]")
    room_nos_readonly = (By.XPATH, "//td[@field='room_nos']//input[@readonly]")

    # ----- 右側篩選工具列 -----
    check_assignable_room = (
        By.XPATH,
        "//label[@data-field-id='chkAssign']//span[@class='el-checkbox__inner']",
    )

    # ----- 右側房間卡片 -----
    big_room_type = (
        By.XPATH,
        "//div[contains(@data-field-id, 'BigGraphics_%s')]//span[contains(@class, 'Type')]",
    )
    big_room_date_range = (
        By.XPATH,
        "//div[contains(@data-field-id, 'BigGraphics_%s')]//span[contains(@class, 'DateRange')]",
    )
