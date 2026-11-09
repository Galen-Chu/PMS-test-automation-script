from selenium.webdriver.common.by import By
from locators.base_locator import BaseLocator


class ServiceQuantityReportLocator(BaseLocator):

    # ----- 查詢條件區（單區，無基本/進階之分）-----
    # query_dat Syncfusion datepicker 雙 input：[1]=placeholder「請選擇」，[2]=實際日期值
    input_query_dat = (By.XPATH, "(//div[@data-field-id='query_dat']//input)[2]")

    # Element UI 單選：click input 展開 dropdown
    # ⚠️ report_typ 與 template 的 UI label 都是「報表格式」，禁止用 label 定位，須用 data-field-id
    input_sort_by = (By.XPATH, "//div[@data-field-id='sort_by']//input")
    input_report_typ = (By.XPATH, "//div[@data-field-id='report_typ']//input")

    # Element UI 選項（避開全域 hidden popup，共用 formator；與 arrival_guest_report 同公式）
    option_dropdown = (
        By.XPATH,
        "//ul[contains(@class,'el-select-dropdown__list') and not(contains(@style,'display: none'))]"
        "//li[normalize-space()='%s']",
    )

    # query_range radio（CI/ALL，click label 切換；radio 冪等，直接 click 目標 label）
    label_query_range = (
        By.XPATH,
        "//div[@data-field-id='query_range']//label[normalize-space()='%s']",
    )

    # btn_search / btn_condition 直接沿用 BaseLocator（contains _doSearch / _toggle 已 match undefined_*）

    # ----- 報表區 -----
    iframe_report = (By.ID, "reportIframe")
