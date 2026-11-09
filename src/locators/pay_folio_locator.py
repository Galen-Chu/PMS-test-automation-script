from selenium.webdriver.common.by import By

from locators.base_locator import BaseLocator


class PayFolioLocator(BaseLocator):

    # ----- 線上繳款單 dialog（PMS0120070，訂房卡工具列進入）-----
    btn_open_payfolio = (By.XPATH, "//div[@data-field-id='doOpenPayFolioDialog']//button")
    btn_payfolio_add = (By.XPATH, "//div[@data-field-id='addButton']//button")
    btn_payfolio_save = (By.XPATH, "//div[@data-field-id='saveButton']//button")
    btn_payfolio_cancel = (By.XPATH, "//div[@data-field-id='cancel']//button")
    # [last()]：訂房卡 dialog 嵌套多層，關閉鈕取最上層
    btn_payfolio_close = (By.XPATH, "(//button[@title='關閉'])[last()]")
    # 行選取：e-row + td[field] 完整寫法（td 直接 locate 撞 hidden 副本，結構文件實證）
    row_folio_by_nos = (
        By.XPATH,
        "(//tr[contains(@class,'e-row')]"
        "[.//td[@field='folioNos' and contains(.,'%s')]])[1]/td[@field='folioNos']",
    )
    # 第一筆未取消帳單（N:正常/F:上傳失敗 row；復原偵測/選取用）
    row_folio_active_first = (
        By.XPATH,
        "(//tr[contains(@class,'e-row')]"
        "[.//td[contains(@class,'e-rowcell') and (contains(.,'N:') or contains(.,'F:'))]]"
        "[.//td[@field='folioNos']])[1]/td[@field='folioNos']",
    )
    # 第一筆 D:刪除 row（addButton 前選取用）
    row_folio_deleted_first = (
        By.XPATH,
        "(//tr[contains(@class,'e-row')]"
        "[.//td[contains(@class,'e-rowcell') and contains(.,'D:')]]"
        "[.//td[@field='folioNos']])[1]/td[@field='folioNos']",
    )
