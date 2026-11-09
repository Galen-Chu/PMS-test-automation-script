from selenium.webdriver.common.by import By
from locators.base_locator import BaseLocator


class ShiftDailyReportLocator(BaseLocator):

    # ----- 查詢條件區 -----
    input_hall = (By.XPATH, "//div[@data-field-id='rspt_cod']//input")  # 廳別（Element UI，必填）
    option_hall = (
        By.XPATH,
        "//ul[contains(@class,'el-select-dropdown__list')]"
        "//span[starts-with(normalize-space(),'%s')]",
    )
    input_batch_date = (
        By.XPATH,
        "//div[@data-field-id='batch_dat']//input",
    )  # 查詢日期（預設 system_date）
    input_print_type = (
        By.XPATH,
        "//div[@data-field-id='print_type']//input",
    )  # 列印項目（預設 S：服務項目）
    input_income_type = (
        By.XPATH,
        "//div[@data-field-id='income_type']//input",
    )  # 查詢依據（預設 1：入帳收入）

    # 查詢按鈕重用 BaseLocator.btn_search（(//button[contains(@data-field-id,'_doSearch')])[last()] 已 match undefined_doSearch）

    # ----- 報表區 -----
    iframe_report = (By.ID, "reportIframe")  # 查詢前不存在，查詢後動態載入
