from time import sleep
from pages.athena_base_page import AthenaBasePage
from locators.forex_rate_locator import ForexRateLocator


class ForexRatePage(AthenaBasePage):

    def __init__(self, driver):
        super().__init__(driver, ForexRateLocator())

    # ----- 匯入幣別 EasyUI combobox（inline cell：type filter 開下拉）-----
    def select_currency(self, currency):
        """currency=幣別代號（如 'EUR'）。click input focus + type filter 使目標 item visible → click item。
        click input/arrow 不開下拉（EasyUI combobox 盲區），type filter 才使 item visible。
        type 後多 combo-p（visible + hidden 殘留），find_elements 取 displayed 的 click。"""
        inp = self.driver.find_element(*self.locator.input_fmoney_code)
        inp.click()
        sleep(0.3)
        inp.send_keys(currency)
        sleep(0.5)
        items = self.driver.find_elements(
            *self.format_locator(self.locator.item_currency, currency)
        )
        for item in items:
            if item.is_displayed():
                item.click()
                return self
        return self

    # ----- 匯率 / 手續費（EasyUI textbox number）-----
    def input_buy_rate(self, value):
        self.input_with_clear(self.locator.input_buy_rate, str(value))
        return self

    def input_service_amt(self, value):
        self.input_with_clear(self.locator.input_service_amt, str(value))
        return self

    # ----- 列表驗證 + 復原 -----
    def _find_row(self, currency):
        return self.driver.find_element(*self.format_locator(self.locator.tr_by_currency, currency))

    def has_currency_row(self, currency):
        """列表是否有指定幣別的 body row（doSearch 後判斷）。"""
        return self.has_element(self.format_locator(self.locator.tr_by_currency, currency))

    def get_row_field(self, currency, field):
        """讀指定幣別 body row 的欄位 text（currency 定位 row，field 取 cell）。
        前提：列表已 doSearch 顯示該 row。"""
        row = self._find_row(currency)
        return row.find_element(*self.format_locator(self.locator.cell_in_row_by_field, field)).text

    def remove_currency_row(self, currency):
        """刪除指定幣別已存正式 row 的同頁操作（click fmoneyCode cell 進 editing + remove）。
        EasyUI inline-edit grid：click cell 觸發 inline editing → remove 清 UI editing 行。
        ⚠️ remove 僅清 UI editing 行，未 commit DB delete；呼叫端需接 save 才真正刪除。
        前提：列表已 doSearch 顯示該 row。"""
        row = self._find_row(currency)
        cell = row.find_element(
            *self.format_locator(self.locator.cell_in_row_by_field, "fmoneyCode")
        )
        cell.click()
        sleep(0.3)
        self.click_toolbar_with_icon("remove")
        return self
