from selenium.webdriver.common.by import By
from locators.base_locator import BaseLocator


class ForexRateLocator(BaseLocator):

    # ----- 開班 dialog（未開班攔截，同外幣匯兌族）-----
    dialog_shift = (By.XPATH, "//div[contains(@class,'panel-title') and normalize-space()='開班']")

    # ----- Grid inline 新增行 editing cell（add 觸發）-----
    # 匯入幣別 EasyUI combobox（textbox-text：click focus + type filter 開下拉；arrow click 無反應）
    input_fmoney_code = (
        By.XPATH,
        "//td[@field='fmoneyCode']//input[contains(@class,'textbox-text')]",
    )
    # combobox-item（%s=幣別代號；type filter 後多 combo-p 殘留 hidden，page 用 find_elements 取 displayed）
    item_currency = (By.XPATH, "//div[contains(@class,'combobox-item')][contains(.,'%s')]")
    # 匯率 / 手續費 EasyUI textbox(number)（textbox-text visible，2 hidden template 無此 class）
    input_buy_rate = (By.XPATH, "//td[@field='buyRate']//input[contains(@class,'textbox-text')]")
    input_service_amt = (
        By.XPATH,
        "//td[@field='serviceAmt']//input[contains(@class,'textbox-text')]",
    )

    # ----- 列表 Grid body row（驗證欄位 + 復原刪除）-----
    # 指定幣別 body row 的 tr（%s=代號；doSearch 後可見，has/get/remove 用，row-scoped）
    tr_by_currency = (
        By.XPATH,
        "//tr[contains(@class,'datagrid-row') and .//td[@field='fmoneyCode'][contains(.,'%s')]]",
    )
    # row 內欄位 cell（%s=field；相對 tr element scope，get_row_field 讀欄位 / remove click fmoneyCode cell 用）
    cell_in_row_by_field = (By.XPATH, ".//td[@field='%s']")
