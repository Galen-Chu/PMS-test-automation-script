from selenium.webdriver.common.by import By
from locators.base_locator import BaseLocator


class ArrivalGuestReportLocator(BaseLocator):

    # ----- 基本查詢條件區 -----
    input_ci_dat = (By.XPATH, "//div[@data-field-id='ci_dat']//input")
    # checkbox 真 input hidden，需 click label；//label 會 match 到 hidden 版本，加 class 限縮
    label_is_not_ci = (
        By.XPATH,
        "//div[@data-field-id='is_not_ci']//label[contains(@class,'checkbox')]",
    )
    label_is_print_rent = (
        By.XPATH,
        "//div[@data-field-id='is_print_rent']//label[contains(@class,'checkbox')]",
    )
    input_is_not_ci_checked = (By.XPATH, "//div[@data-field-id='is_not_ci']//input")
    input_is_print_rent_checked = (By.XPATH, "//div[@data-field-id='is_print_rent']//input")

    # ----- 進階條件區（需先 click undefined_toggle 展開）-----
    input_sort_cod = (By.XPATH, "//div[@data-field-id='sort_cod']//input")
    input_sql_mod = (By.XPATH, "//div[@data-field-id='sql_mod']//input")
    # Element UI dropdown 選項（避開全域 hidden li），共用 formator
    option_dropdown = (
        By.XPATH,
        "//ul[contains(@class,'el-select-dropdown__list') and not(contains(@style,'display: none'))]"
        "//li[normalize-space()='%s']",
    )

    # btn_search / btn_condition 直接沿用 BaseLocator（contains _doSearch / _toggle 已 match undefined_*）

    # ----- 報表區 -----
    iframe_report = (By.ID, "reportIframe")
