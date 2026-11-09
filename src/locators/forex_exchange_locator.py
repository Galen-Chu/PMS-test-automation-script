from selenium.webdriver.common.by import By
from locators.base_locator import BaseLocator


class ForexExchangeLocator(BaseLocator):

    # ----- 新增 Panel combogrid（姓名搜尋+選取）-----
    # combo-arrow 開 panel（EasyUI combogrid；panel 開後 row visible，native click 觸發 onSelect 帶入 4 欄）
    combo_full_name = (
        By.XPATH,
        "//div[@data-field-id='fullName']//a[contains(@class,'textbox-icon')]",
    )
    # combogrid textbox-text（JS setValue+Enter 觸發 server query；Selenium type 被 toolbar overlay 擋）
    input_full_name = (
        By.XPATH,
        "//div[@data-field-id='fullName']//input[contains(@class,'textbox-text')]",
    )
    # combogrid 結果 row（%s=房號；panel 開後 visible，native click 選取）
    row_guest = (By.XPATH, "//div[contains(@class,'combo-panel')]//tr[td[normalize-space()='%s']]")

    # ----- 新增 Panel 可編輯欄位 -----
    # 證件號碼（visible input name=idCode；hidden 在前會被首選，用 name 定位 visible 觸發 Vue）
    input_id_code = (By.XPATH, "//input[@name='idCode']")
    # 生日 Element UI DatePicker（click input 開 picker，picker UI 選日期觸發 Vue model）
    input_birthday = (
        By.XPATH,
        "//div[@data-field-id='birthday']//input[contains(@class,'el-input__inner')]",
    )
    # birthday picker 日期 cell（%s=日期數字，td text）
    cell_birthday = (
        By.XPATH,
        "//div[contains(@class,'el-date-picker')]//td[normalize-space()='%s']",
    )
    # 幣別 EasyUI combobox（click combo-arrow 開 dropdown，click item 選幣別，連動 buyRate 匯率）
    combo_currency = (
        By.XPATH,
        "//div[@data-field-id='fmoneyCode']//a[contains(@class,'textbox-icon')]",
    )
    item_currency = (By.XPATH, "//div[contains(@class,'combobox-item')][contains(.,'%s')]")
    # 金額 Syncfusion NumericTextBox（visible e-numerictextbox；native type + tab blur 觸發 ej2 連動 totalAmt/tmoneyAmt）
    input_fmoney_amt = (
        By.XPATH,
        "//div[@data-field-id='fmoneyAmt']//input[contains(@class,'e-numerictextbox')]",
    )
    input_service_amt = (
        By.XPATH,
        "//div[@data-field-id='serviceAmt']//input[contains(@class,'e-numerictextbox')]",
    )

    # ----- 搜尋區（列表驗證）-----
    # ikey 搜尋欄（visibility:hidden，JS setValue + dispatch）
    input_ikey = (By.XPATH, "//div[@data-field-id='ikey']//input")
    # idCode 搜尋欄（搜尋區 visibility:hidden；隨機唯一值 filter 定位剛新增水單，JS setValue + dispatch）
    input_idcode_search = (By.XPATH, "//div[@data-field-id='idCode']//input")

    # ----- 開班 dialog（未開班攔截）-----
    dialog_shift = (By.XPATH, "//div[contains(@class,'panel-title') and normalize-space()='開班']")

    # ----- alert（新增成功 是否列印水單？）-----
    # 取消按鈕（不列印；alert 開時唯一 visible 取消）
    btn_alert_cancel = (By.XPATH, "//button[normalize-space()='取消']")
    # 新增 Panel 關閉（save 後 Panel + window-mask 殘留，關 Panel 清 mask 才能操作列表）
    btn_close_panel = (By.XPATH, "(//a[contains(@class,'panel-tool-close')])[last()]")

    # ----- 列表 Grid（驗證新增 row）-----
    # ikey 定位 row（%s=ikey；搜尋後多筆，最新在 DOM 最後，page 用 find_elements[-1]）
    row_latest_by_ikey = (By.XPATH, "//td[@field='ikey' and normalize-space()='%s']/parent::tr")
    # 列表欄位 cell（%s=field name；相對 row element scope，配 row_latest_by_ikey 用）
    cell_in_row_by_field = (By.XPATH, ".//td[@field='%s']")

    # ----- 重新打開編輯 Panel（驗證用）-----
    # 編輯按鈕（操作列，需先勾選資料列；match=1）
    btn_edit_panel = (By.XPATH, "//button[img/@alt='edit']")
    # row 內 ck checkbox（row scope，配 row_latest_by_ikey；勾選最新水單後點編輯重開 Panel）
    ck_in_row = (By.XPATH, ".//input[@name='ck']")
    # 編輯 Panel 讀取欄位（EasyUI textbox-text：房號/幣別）
    text_room_number = (
        By.XPATH,
        "//div[@data-field-id='roomNumber']//input[contains(@class,'textbox-text')]",
    )
    text_fmoney_code = (
        By.XPATH,
        "//div[@data-field-id='fmoneyCode']//input[contains(@class,'textbox-text')]",
    )
    # 國籍（name 定位，disabled input value）
    text_country_code = (By.XPATH, "//input[@name='countryCode']")
    # 編輯 Panel 數值欄位（Syncfusion NumericTextBox：匯率/總額/淨額）
    text_buy_rate = (
        By.XPATH,
        "//div[@data-field-id='buyRate']//input[contains(@class,'e-numerictextbox')]",
    )
    text_total_amt = (
        By.XPATH,
        "//div[@data-field-id='totalAmt']//input[contains(@class,'e-numerictextbox')]",
    )
    text_tmoney_amt = (
        By.XPATH,
        "//div[@data-field-id='tmoneyAmt']//input[contains(@class,'e-numerictextbox')]",
    )
