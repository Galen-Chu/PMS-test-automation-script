from time import sleep
from pages.athena_base_page import AthenaBasePage
from locators.shift_detail_report_locator import ShiftDetailReportLocator
from tools import report_reader


class ShiftDetailReportPage(AthenaBasePage):

    def __init__(self, driver):
        super().__init__(driver, ShiftDetailReportLocator())

    # 交班明細表 PMS03R0020 欄位地圖（15 欄單一寬表，word 中心 x 落點歸欄）
    # 跨頁明細 + 最後一頁總計行（總計行的「總計:」文字落退房日欄，非公帳號欄）
    COLUMNS = [
        ("系統別", 0, 50),
        ("公帳號", 50, 90),
        ("房號單據", 90, 150),
        ("發票號碼", 150, 235),
        ("姓名", 235, 320),
        ("入住日", 320, 370),
        ("退房日", 370, 445),
        ("房租", 445, 490),
        ("服務費", 490, 535),
        ("客房其他", 535, 590),
        ("預收款", 590, 635),
        ("客房訂金", 635, 690),
        ("現金", 690, 720),
        ("MASTER", 720, 770),
        ("沖客房", 770, 820),
    ]
    # 8 個數值欄（Tier 1-3 彙總不變量：明細各欄加總 == 總計行）
    NUMERIC_COLS = ("房租", "服務費", "客房其他", "預收款", "客房訂金", "現金", "MASTER", "沖客房")

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
        """回讀查詢日期欄位值（供 Tier 1 查詢回顯斷言的預期基準，避免硬編環境預設日期）。"""
        return self.driver.find_element(*self.locator.input_batch_date).get_attribute("value")

    def query(self):
        """點「藍色放大鏡」查詢。"""
        self.click(self.locator.btn_search)
        return self

    def get_report_pdf_url(self):
        """查詢後取報表 iframe 的 PDF URL（輪詢等 src 非同步填入）。"""
        return self.get_iframe_src(self.locator.iframe_report)

    def parse_report(self, pdf_path):
        """解析交班明細表 PDF，回傳 Tier 1 斷言所需的結構化結果。

        跨頁逐行掃描（不用 extract_grid：本表跨頁，且總計行的「總計:」落退房日欄，
        非 extract_grid 假設的 key_col stop）：
        - 總計行：退房日欄 startswith「總計」→ total（記住後略過，不收入 items）
        - 資料行：8 數值欄至少一個是數字（涵蓋一般訂房卡列 + Card Deposit Add 列——
          兩者差異在公帳號欄是否為空，但都有數值，故以數值欄為資料列信號）
        - 表頭 / 分組碼（HFD/ADV/DPS）/ 頁尾文字 → 數值欄非數字或空，自動略過

        只回傳原始結構（items/total/echo/text/page_count），彙總不變量等「驗證」
        交由 test 端負責（page 不放斷言）。
        """
        report = report_reader.Report(pdf_path)
        items, total = [], None
        for page_idx in range(report.page_count):
            for row_words in report.rows(page_idx):
                cells = report_reader.cells_by_columns(row_words, self.COLUMNS)
                if cells.get("退房日", "").startswith("總計"):
                    total = cells
                    continue
                if any(
                    report_reader.to_num(cells.get(col)) is not None for col in self.NUMERIC_COLS
                ):
                    items.append(cells)
        return {
            "text": report.text,
            "page_count": report.page_count,
            "echo": report_reader.parse_query_echo(report.text),
            "items": items,
            "total": total,
        }
