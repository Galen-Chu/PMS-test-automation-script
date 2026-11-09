from selenium.webdriver.common.by import By
from locators.base_locator import BaseLocator


class GuestRegistrationCardLocator(BaseLocator):

    # ----- 查詢區 -----
    # doSearch 走 BaseLocator.btn_search（contains _doSearch 已 match PMS02R0010_doSearch）

    # ----- 結果 Grid -----
    # 指定訂房卡號 body row 的 cell（%s=ikey；click 觸發 selection + ck 連動勾選）
    cell_ikey = (By.XPATH, "//td[@field='ikey' and normalize-space()='%s']")
    # 同 row 的列印房租 cell（%s=ikey；row-scoped，驗證批次設定結果）
    cell_is_prtrent_by_ikey = (
        By.XPATH,
        "//tr[td[@field='ikey' and normalize-space()='%s']]/td[@field='is_prtrent']",
    )

    # ----- 列印（el-dropdown）-----
    btn_print = (By.XPATH, "//button[normalize-space()='列印']")
    # 格式選項（PDF/WORD；EXCEL disabled）——el-dropdown menu 是 CLI describe 盲區但 find 正常
    li_print_pdf = (By.XPATH, "//li[normalize-space()='PDF']")

    # ----- PDF 預覽 dialog -----
    # 與 arrival/service report 同機制：EasyUI panel + iframe 載入 PDF（id 為 URL，用 class 定位）
    iframe_report = (By.XPATH, "//iframe[contains(@class,'iframeHt')]")
    btn_close_report_dialog = (By.XPATH, "//a[contains(@class,'panel-tool-close')]")

    # ----- 批次設定 dialog（Syncfusion）-----
    btn_batch_setting = (By.XPATH, "//button[normalize-space()='批次設定']")
    # 列印房租 DropDownList（click span 開 popup；值顯示於 span text）
    span_is_print = (By.XPATH, "//div[@data-field-id='isPrint']//span")
    # DDL popup 選項（%s=是/否；Syncfusion e-popup 開啟時 visible）
    li_is_print_option = (By.XPATH, "//div[@id='_popup']//li[normalize-space()='%s']")
    btn_batch_confirm = (By.XPATH, "//div[@data-field-id='confirmButton']//button")
