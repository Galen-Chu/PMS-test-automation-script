from selenium.webdriver.common.by import By

from locators.base_locator import BaseLocator


class BusinessCompanyLocator(BaseLocator):

    # ----- 搜尋區 -----
    input_company_cod = (By.XPATH, "//div[@data-field-id='cust_mn_show_cod']//input")
    btn_search = (By.XPATH, "//button[@data-field-id='PMS0610010_doSearch']")
    text_company_row = (By.XPATH, "//td[@field='cust_mn_show_cod']/div[text()='%s']")

    # ----- 工具列 -----
    btn_edit = (By.XPATH, "//button[.//img[@alt='edit']]")

    # ----- 維護視窗 -----
    btn_close_maintain = (
        By.XPATH,
        "//div[contains(@class, 'panel-title') and text()='商務公司維護']"
        "/parent::div//a[contains(@class, 'panel-tool-close')]",
    )

    # ----- 合約 inline 修改（#776）-----
    # click 目標合約 cell 進 inline 編輯（值 = 合約編號）
    text_contract_cell = (By.XPATH, "//td[@field='contract_cod' and normalize-space()='%s']")
    input_remark1 = (By.XPATH, "//td[@field='remark1']//input[contains(@class,'textbox-text')]")
    btn_combobox_arrow_field = (By.XPATH, "//td[@field='%s']//a[contains(@class,'textbox-icon')]")
    item_combobox = (By.XPATH, "(//div[@class='combobox-item' and text()='%s'])[last()]")
    # 開啟中（visible）combobox 下拉 panel 內的選項
    item_combobox_visible = (
        By.XPATH,
        "//div[contains(@class,'panel-htop') and not(contains(@style,'none'))]"
        "//div[contains(@class,'combobox-item')]",
    )
    # 編輯列欄位的 visible textbox——編輯態 div 是 editable wrapper，值須讀 input value 非 div text
    input_field_textbox = (
        By.XPATH,
        "(//tr[contains(@id, 'companyContractDgId')]"
        "/td[@field='%s']//input[contains(@class,'textbox-text')])[last()]",
    )
    # 空 grid 有 1px transparent dummy row，以 contract_cod cell 有值判定真實資料列
    text_contract_row = (
        By.XPATH,
        "//tr[contains(@id, 'companyContractDgId')]"
        "/td[@field='contract_cod']/div[normalize-space()!='']",
    )
