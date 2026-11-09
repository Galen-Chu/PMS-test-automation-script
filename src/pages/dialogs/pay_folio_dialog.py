from pages.athena_base_page import AthenaBasePage
from locators.pay_folio_locator import PayFolioLocator


class PayFolioDialog(AthenaBasePage):

    def __init__(self, driver):
        super().__init__(driver, PayFolioLocator())

    # ----- 線上繳款單 dialog（#2130）-----

    def open_pay_folio_dialog(self):
        self.click(self.locator.btn_open_payfolio)
        return self

    def click_add(self):
        self.click(self.locator.btn_payfolio_add)
        return self

    def click_save(self):
        self.click(self.locator.btn_payfolio_save)
        return self

    def click_cancel(self):
        """刪除選取的有效筆（N/F→D 即時生效，不需存檔）。"""
        self.click(self.locator.btn_payfolio_cancel)
        return self

    def close_dialog(self):
        self.click(self.locator.btn_payfolio_close)
        return self

    def select_folio_by_nos(self, folio_nos):
        """以繳款單號選取 row（選取後主檔帶入該筆值）。

        e-row + td[field] 完整寫法：td 直接 locate 會匹配 hidden 副本
        無聲失敗（結構文件實證陷阱）。
        """
        locator_row = self.format_locator(self.locator.row_folio_by_nos, folio_nos)
        self.click(locator_row)
        return self

    def select_first_active_folio(self):
        """選取第一筆未取消帳單（狀態 N/F 的 row）——復原用。"""
        self.click(self.locator.row_folio_active_first)
        return self

    def select_deleted_folio(self):
        """選取 D:刪除筆（addButton 需選 D 筆才 enabled；無 D 筆時不選取）。"""
        if self.driver.find_elements(*self.locator.row_folio_deleted_first):
            self.click(self.locator.row_folio_deleted_first)
        return self

    def has_active_folio(self):
        """grid 是否存在未取消帳單（N/F 筆，會擋 addButton）。"""
        return bool(self.driver.find_elements(*self.locator.row_folio_active_first))

    def get_saved_folio_nos(self):
        """讀存檔生成的新繳款單號（選取態主檔 input 或 grid row，取主檔）。"""
        return self.get_field_value("folioNos") or ""

    def get_grid_count(self, field):
        """數繳款單 dialog 內指定欄位的資料列數。

        主 grid（folioNos）/明細 grid（seqNos）用；scan 的 gridRows 受
        frozen/regular 雙計干擾，DOM 計數最準（結構文件實證）。
        """
        return self.driver.execute_script(
            "var f=arguments[0];"
            "return document.querySelectorAll("
            "\"div[role='dialog'] div.e-grid td[field='\"+f+\"']\").length;",
            field,
        )

    def get_field_value(self, dfid):
        """讀主檔欄位值（選取/新增態 input value，如 payAmount/folioStatus/altName）。"""
        return self.driver.execute_script(
            "var d=arguments[0];"
            "var el=document.querySelector("
            "\"div[role='dialog'] div[data-field-id='\"+d+\"'] input\");"
            "return el?el.value:null;",
            dfid,
        )
