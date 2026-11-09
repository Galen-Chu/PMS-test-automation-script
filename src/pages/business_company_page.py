from time import sleep

from pages.athena_base_page import AthenaBasePage
from locators.business_company_locator import BusinessCompanyLocator
from tools.display_helper import DisplayHelper


class BusinessCompanyPage(AthenaBasePage):

    def __init__(self, driver):
        super().__init__(driver, BusinessCompanyLocator())

    # ----- 導航 / 搜尋 / 進維護視窗 -----

    def search_company(self, company_cod):
        self.set_value_by_data_field_id("cust_mn_show_cod", company_cod)
        self.click(self.locator.btn_search)
        return self

    def click_target_company(self, company_cod):
        locator_row = self.format_locator(self.locator.text_company_row, company_cod)
        self.click(locator_row)
        return self

    def open_maintain_panel(self):
        self.click(self.locator.btn_edit)
        return self

    def close_maintain_panel(self):
        self.click(self.locator.btn_close_maintain)
        return self

    # ----- 合約驗證讀值 -----

    def has_contract_row(self):
        return self.has_element(self.locator.text_contract_row)

    # ----- #776 inline 修改 -----

    def click_contract_cell_to_edit(self, contract_cod):
        locator_cell = self.format_locator(self.locator.text_contract_cell, contract_cod)
        self.click(locator_cell)
        return self

    def type_remark1(self, value):
        self.input_with_clear(self.locator.input_remark1, value)
        return self

    def select_contract_combobox(self, field, value):
        locator_arrow = self.format_locator(self.locator.btn_combobox_arrow_field, field)
        self.click(locator_arrow)
        locator_item = self.format_locator(self.locator.item_combobox, value)
        self.click(locator_item)
        return self

    # ----- combobox runtime 探測（選項是環境資料，不寫 test_data）-----

    def _visible_combobox_items(self, field):
        """開欄位下拉並回傳 visible 選項元素清單（等動畫收斂後取）。

        panel 收合後不離開 DOM 只隱藏，須以 visible 過濾。
        """
        locator_arrow = self.format_locator(self.locator.btn_combobox_arrow_field, field)
        self.click(locator_arrow)
        sleep(2)
        return self.driver.find_elements(*self.locator.item_combobox_visible)

    def _pick_combobox_item(self, field, match):
        """依條件挑 visible 選項 click，成功後 yield 寫入的欄位值（顯示格式）。

        動畫未收斂時 click 可能拋 not interactable 但事件實已送達（值已選入），
        故以欄位值已寫入為成功判準，不採信 click 的回傳狀態。
        """
        for item in self._visible_combobox_items(field):
            text = item.text.strip()
            if not match(text):
                continue
            item.click()
            sleep(0.5)
            locator_input = self.format_locator(self.locator.input_field_textbox, field)
            value = self.driver.find_element(*locator_input).get_attribute("value")
            if value:
                return DisplayHelper.normalize_display_value(value)
        raise ValueError(f"combobox {field} 無匹配選項或選後未寫入值")

    def pick_contract_combobox(self, field, exclude=None):
        """取第一個可用選項（排除 exclude），回傳寫入後欄位值（顯示格式）。"""
        exclude = DisplayHelper.normalize_display_value(exclude) if exclude else None
        return self._pick_combobox_item(field, lambda text: bool(text) and text != exclude)

    def pick_hotel(self):
        """選館別 01 本館（00 訂房中心有全系統合約日期衝突勿選）。

        以 '01 :' 代號前綴比對，館名顯示文字跨環境不同。
        """
        return self._pick_combobox_item(
            field="hotel_cod", match=lambda text: text.startswith("01 :")
        )
