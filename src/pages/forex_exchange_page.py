from time import sleep
from selenium.webdriver.common.keys import Keys
from pages.athena_base_page import AthenaBasePage
from locators.forex_exchange_locator import ForexExchangeLocator


class ForexExchangePage(AthenaBasePage):

    def __init__(self, driver):
        super().__init__(driver, ForexExchangeLocator())

    # ----- combogrid 姓名（搜尋+選取）-----
    def search_and_select_guest(self, name, room_no):
        """EasyUI combogrid 搜尋+選取（連動帶入 fullName/roomNumber/ikey/countryCode 4 欄）。
        click combo-arrow 開 panel → JS setValue+Enter 觸發 server query（#514 族：send_keys 不觸發 filter）
        → native click row 選取（panel 開後 row visible，native click 觸發 onSelect）。"""
        self.click(self.locator.combo_full_name)
        sleep(0.5)
        inp = self.driver.find_element(*self.locator.input_full_name)
        self.driver.execute_script(
            "var el=arguments[0]; var J=window.jQuery;"
            "J(el).val(arguments[1]);"
            "el.dispatchEvent(new Event('input',{bubbles:true}));"
            "el.dispatchEvent(new KeyboardEvent('keydown',{key:'Enter',code:'Enter',keyCode:13,bubbles:true}));",
            inp,
            name,
        )
        sleep(2)
        self.click(self.format_locator(self.locator.row_guest, room_no))
        return self

    # ----- 證件號碼（native type 觸發 Vue model）-----
    def input_id_code(self, value):
        self.input_with_clear(self.locator.input_id_code, value)
        return self

    # ----- 生日 Element UI DatePicker（picker UI，native click）-----
    def select_birthday(self, day):
        """click input 開 picker → click 日期 cell（picker UI 選日期，觸發 Vue model 同步，可靠）。"""
        self.click(self.locator.input_birthday)
        sleep(0.5)
        self.click(self.format_locator(self.locator.cell_birthday, day))
        return self

    # ----- 幣別 EasyUI combobox（native click）-----
    def select_currency(self, currency):
        """click combo-arrow 開 dropdown → click item（連動 buyRate 匯率）。"""
        self.click(self.locator.combo_currency)
        sleep(0.5)
        self.click(self.format_locator(self.locator.item_currency, currency))
        return self

    # ----- 金額 Syncfusion NumericTextBox（native send_keys + tab blur）-----
    def input_amount(self, foreign_amount, service_amount):
        """金額+手續費（send_keys + tab blur 觸發 ej2 change：totalAmt=金額×匯率, tmoneyAmt=總額-手續費）。
        Syncfusion 用 Ctrl+A+Backspace 清除（element.clear() 會破壞 ej2 instance）；前提：幣別已選（buyRate 有值）。"""
        self._set_numeric(self.locator.input_fmoney_amt, str(foreign_amount))
        self._set_numeric(self.locator.input_service_amt, str(service_amount))
        return self

    def _set_numeric(self, locator, value):
        el = self.driver.find_element(*locator)
        el.click()
        el.send_keys(Keys.CONTROL, "a")
        el.send_keys(Keys.BACKSPACE)
        el.send_keys(value)
        el.send_keys(Keys.TAB)

    # ----- 搜尋 ikey（列表驗證用）-----
    def search_by_ikey(self, ikey):
        """ikey 搜尋欄 visibility:hidden，JS native setter + dispatch 後 click 搜尋。"""
        inp = self.driver.find_element(*self.locator.input_ikey)
        self.driver.execute_script(
            "var el=arguments[0];"
            "var s=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;"
            "s.call(el,arguments[1]); el.dispatchEvent(new Event('input',{bubbles:true}));"
            "el.dispatchEvent(new Event('change',{bubbles:true}));",
            inp,
            ikey,
        )
        self.click(self.locator.btn_search)
        sleep(1)
        return self

    # ----- idCode 搜尋（隨機唯一 filter，取代 ikey+[-1] 排序假設）-----
    def search_by_idcode(self, id_code):
        """idCode 搜尋欄 visibility:hidden，JS native setter + dispatch + click 搜尋。
        idCode 隨機唯一，filter 結果只剩該筆（不依賴排序，避免 [-1] 取錯筆）。"""
        inp = self.driver.find_element(*self.locator.input_idcode_search)
        self.driver.execute_script(
            "var el=arguments[0];"
            "var s=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;"
            "s.call(el,arguments[1]); el.dispatchEvent(new Event('input',{bubbles:true}));"
            "el.dispatchEvent(new Event('change',{bubbles:true}));",
            inp,
            id_code,
        )
        self.click(self.locator.btn_search)
        sleep(1)
        return self

    # ----- 列表驗證（idCode filter 唯一筆欄位值）-----
    def get_latest_row_field(self, ikey, field):
        """取得 ikey 最新 row（搜尋後 DOM 最後一筆=最新）的指定欄位 text。
        水單累積：同 ikey 多筆，最新在 DOM 最後（排序舊在前）。"""
        row_locator = self.format_locator(self.locator.row_latest_by_ikey, ikey)
        rows = self.driver.find_elements(*row_locator)
        row_el = rows[-1]
        cell_locator = self.format_locator(self.locator.cell_in_row_by_field, field)
        return row_el.find_element(*cell_locator).text

    # ----- 重新打開編輯 Panel（驗證用）-----
    def open_edit_panel_for_latest(self, ikey):
        """勾選 ikey 最新水單 → 點編輯，重新打開該筆的編輯 Panel（帶入完整欄位）。
        水單累積，最新在 DOM 最後（find_elements[-1]）；ck 先查狀態未勾才 click。
        前提：列表已搜尋顯示該 ikey（test 端先 search_by_ikey）。"""
        row_locator = self.format_locator(self.locator.row_latest_by_ikey, ikey)
        rows = self.driver.find_elements(*row_locator)
        latest_row = rows[-1]
        ck = latest_row.find_element(*self.locator.ck_in_row)
        if ck.get_attribute("checked") != "true":
            ck.click()
        self.click(self.locator.btn_edit_panel)
        return self

    def get_edit_panel_fields(self):
        """讀取編輯 Panel 完整欄位值（重新打開後驗證用），返回 dict。
        混用既有新增欄位 locator（fullName/idCode/birthday/fmoneyAmt/serviceAmt）+
        編輯模式讀取 locator（roomNumber/fmoneyCode/countryCode/buyRate/totalAmt/tmoneyAmt）。
        ⚠️ idCode 編輯模式被遮罩（如 A12****789），斷言用前綴/後綴非完整值。"""
        d = self.driver
        return {
            "full_name": d.find_element(*self.locator.input_full_name).get_attribute("value"),
            "room_number": d.find_element(*self.locator.text_room_number).get_attribute("value"),
            "country_code": d.find_element(*self.locator.text_country_code).get_attribute("value"),
            "id_code": d.find_element(*self.locator.input_id_code).get_attribute("value"),
            "birthday": d.find_element(*self.locator.input_birthday).get_attribute("value"),
            "fmoney_code": d.find_element(*self.locator.text_fmoney_code).get_attribute("value"),
            "fmoney_amt": d.find_element(*self.locator.input_fmoney_amt).get_attribute("value"),
            "buy_rate": d.find_element(*self.locator.text_buy_rate).get_attribute("value"),
            "total_amt": d.find_element(*self.locator.text_total_amt).get_attribute("value"),
            "service_amt": d.find_element(*self.locator.input_service_amt).get_attribute("value"),
            "tmoney_amt": d.find_element(*self.locator.text_tmoney_amt).get_attribute("value"),
        }
