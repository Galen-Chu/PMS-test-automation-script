from selenium.webdriver.common.by import By
from locators.base_locator import BaseLocator


class RateAuditReportLocator(BaseLocator):

    # ----- 查詢條件區 -----
    # 類別 guest_way 為 Element UI multi-select；input 被 el-select__tags 遮擋無法 native click，
    # 開下拉需 click tags（非 input）
    tags_guest_way = (
        By.XPATH,
        "//div[@data-field-id='guest_way']//div[contains(@class,'el-select__tags')]",
    )
    # 下拉選項（scope 到 visible ul；完整 text「F : 散客」唯一化，避撞其他 dropdown 同名 li）
    option_guest_way = (
        By.XPATH,
        "//ul[contains(@class,'el-select-dropdown__list') and not(contains(@style,'display: none'))]"
        "//li[normalize-space()='%s']",
    )
    # 查詢日期 input（Syncfusion DatePicker，預設 PMS 營業日；echo 動態比對用）
    input_search_date = (By.XPATH, "//div[@data-field-id='search_date']//input")

    # ----- 報表區 -----
    iframe_report = (By.ID, "reportIframe")
    # btn_search 沿用 BaseLocator（contains '_doSearch' match 'undefined_doSearch'）
