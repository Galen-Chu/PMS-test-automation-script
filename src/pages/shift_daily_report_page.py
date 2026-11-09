from time import sleep
from pages.athena_base_page import AthenaBasePage
from locators.shift_daily_report_locator import ShiftDailyReportLocator
from tools import report_reader


class ShiftDailyReportPage(AthenaBasePage):

    def __init__(self, driver):
        super().__init__(driver, ShiftDailyReportLocator())

    # 交班日報表 PMS03R0010 欄位地圖（報表結構 schema：word 中心 x 落點歸欄）
    # 並排雙表，以 x 邊界隔離左（收入明細）/ 右（付款方式）
    LEFT_COLS = [("code", 30, 90), ("name", 90, 350), ("amount", 350, 430)]
    RIGHT_COLS = [("method", 430, 700), ("amount", 700, 820)]

    def select_hall(self, hall_option):
        """選廳別（Element UI 下拉，必填）。

        hall_option 為選項文字前綴（如 'FO :'）。點 input 展開（避開 clearable 的 icon 陷阱），
        再依前綴點選項。
        """
        self.click(self.locator.input_hall)
        sleep(0.5)
        locator = self.format_locator(self.locator.option_hall, hall_option)
        self.click(locator)
        return self

    def get_batch_date(self):
        """回讀查詢日期欄位值（供 Tier 1 查詢回顯斷言的預期基準，避免硬編環境 system_date）。"""
        return self.driver.find_element(*self.locator.input_batch_date).get_attribute("value")

    def query(self):
        """點「藍色放大鏡」查詢。"""
        self.click(self.locator.btn_search)
        return self

    def get_report_pdf_url(self):
        """查詢後取報表 iframe 的 PDF URL（輪詢等 src 非同步填入）。"""
        return self.get_iframe_src(self.locator.iframe_report)

    def parse_report(self, pdf_path):
        """解析交班日報表 PDF，回傳 Tier 1 斷言所需的結構化結果。

        依欄位地圖分欄抽取左（收入明細，key=code）/ 右（付款方式，key=method）兩表，
        各遇第一個「合計」即停。只回傳原始結構（items/total/echo/text/page_count），
        彙總不變量等「驗證」交由 test 端負責（page 不放斷言）。
        """
        report = report_reader.Report(pdf_path)
        left_items, left_total = report.extract_grid(self.LEFT_COLS, "code", "合計")
        right_items, right_total = report.extract_grid(self.RIGHT_COLS, "method", "合計")
        return {
            "text": report.text,
            "page_count": report.page_count,
            "echo": report_reader.parse_query_echo(report.text),
            "left_items": left_items,
            "left_total": left_total,
            "right_items": right_items,
            "right_total": right_total,
        }
