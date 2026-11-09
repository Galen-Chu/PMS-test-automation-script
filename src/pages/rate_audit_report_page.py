import re
from time import sleep

from pages.athena_base_page import AthenaBasePage
from locators.rate_audit_report_locator import RateAuditReportLocator
from tools import report_reader


class RateAuditReportPage(AthenaBasePage):

    def __init__(self, driver):
        super().__init__(driver, RateAuditReportLocator())

    # 類別對應：code → (UI 選項 text, PDF 報表 token)
    # UI dropdown 顯示「F : 散客」（半形冒號 + 空白）；PDF 報表印「F:散客」（無空白）—— 兩者不同
    CATEGORY = {
        "F": ("F : 散客", "F:散客"),
        "G": ("G : 團體", "G:團體"),
        "C": ("C : 商務", "C:商務"),
    }

    # 頁尾查詢回顯 keys（PDF：查詢條件: 查詢日期: D 金額為零不顯示: Y 排序方式: X）
    ECHO_KEYS = ("查詢日期", "金額為零不顯示", "排序方式")

    # 表頭主要欄位（結構驗證用）
    HEADER_FIELDS = ("類別", "公帳號", "訂房卡號", "入住日期", "房租", "合計", "房號", "住客姓名")

    def get_search_date(self):
        """讀查詢日期 input 值（預設 = PMS 營業日）。echo 比對用，環境無關。"""
        return self.driver.find_element(*self.locator.input_search_date).get_attribute("value")

    def select_guest_way(self, code):
        """選類別（Element UI multi-select）。

        預設未選；click tags 開下拉 → click option。code: 'F'/'G'/'C'。
        """
        ui_text = self.CATEGORY[code][0]
        self.click(self.locator.tags_guest_way)
        sleep(0.5)
        option = self.format_locator(self.locator.option_guest_way, ui_text)
        self.click(option)
        return self

    def query(self):
        """點藍色放大鏡查詢。"""
        self.click(self.locator.btn_search)
        return self

    def get_report_pdf_url(self):
        """查詢後取報表 iframe 的 PDF URL（輪詢等 src 非同步填入 .pdf）。"""
        return self.get_iframe_src(self.locator.iframe_report)

    def parse_report(self, pdf_path, expected_code):
        """解析房價稽核表 PDF，回傳 Tier 1 斷言所需的結構化結果。

        - text/page_count：原始文字與頁數
        - echo：頁尾查詢回顯（查詢日期 / 金額為零不顯示 / 排序方式）
        - other_category_counts：非送出類別的出現次數（類別過濾不變量用）
        - header_fields_present：表頭主要欄位是否存在
        """
        report = report_reader.Report(pdf_path)
        text = report.text
        counts = {
            code: len(re.findall(re.escape(token), text))
            for code, (_, token) in self.CATEGORY.items()
        }
        other_counts = {code: count for code, count in counts.items() if code != expected_code}
        return {
            "text": text,
            "page_count": report.page_count,
            "echo": report_reader.parse_query_echo(text, keys=self.ECHO_KEYS),
            "other_category_counts": other_counts,
            "header_fields_present": {field: (field in text) for field in self.HEADER_FIELDS},
        }
