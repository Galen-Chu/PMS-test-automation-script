import re

from pages.athena_base_page import AthenaBasePage
from locators.booking_quantity_forecast_report_locator import BookingQuantityForecastReportLocator
from tools import report_reader


class BookingQuantityForecastReportPage(AthenaBasePage):

    def __init__(self, driver):
        super().__init__(driver, BookingQuantityForecastReportLocator())

    # 訂房數量預估報表(依參數) PMS01R0100 欄位地圖（word 中心 x 落點歸欄）
    # 單行記錄 22 欄；月累計行（"NN 月累計"）與合計行（"合計"）用 date 欄內容識別
    COLUMNS = [
        ("date", 0, 55),  # 日行 2024/01/05；月累計 "01 月累計"；合計 "合計"
        ("weekday", 55, 80),  # FRI 等（僅日行）
        ("holiday", 80, 108),  # 假日/平日（僅日行）
        ("total_rooms", 108, 145),  # 總房間數
        ("occupied", 145, 180),  # 住房間數
        ("repair", 180, 225),  # 修理參觀
        ("occ_rate", 225, 265),  # 住房率（百分比，加總無意義）
        ("arrival", 265, 300),  # 到達
        ("departure", 300, 333),  # 離店
        ("stayover", 333, 360),  # 續住
        ("wi", 360, 385),  # W/I
        ("du", 385, 405),  # D/U
        ("rest", 405, 435),  # Rest
        ("hu", 435, 455),  # H/U
        ("comp", 455, 485),  # Comp
        ("adult", 485, 515),  # 大
        ("child", 515, 530),  # 小
        ("guests", 530, 575),  # 總人數
        ("rent", 575, 625),  # 房租收入
        ("fb", 625, 680),  # 餐飲收入
        ("total_income", 680, 720),  # 全部收入
        ("avg_ro", 720, 770),  # 平均房價(R/O)
        ("avg_bf", 770, 830),  # 平均房價(BF)
    ]

    DATE_PATTERN = re.compile(r"^\d{4}/\d{2}/\d{2}$")

    # 頁尾查詢回顯 keys（PDF：查詢條件: 起訖日期: 起日 ~ 訖日）
    ECHO_KEYS = ("起訖日期",)

    # 表頭主要欄位（結構驗證用）
    HEADER_FIELDS = (
        "日期",
        "總房間數",
        "住房間數",
        "住房率",
        "總人數",
        "房租收入",
        "全部收入",
        "合計",
    )

    def get_qry_dat_range(self):
        """讀 qry_dat 起訖日期（預設 = 滾房租日 +3 月）。echo 比對用，環境無關。"""
        start = self.driver.find_element(*self.locator.input_qry_dat_start).get_attribute("value")
        end = self.driver.find_element(*self.locator.input_qry_dat_end).get_attribute("value")
        return start, end

    def query(self):
        """點藍色放大鏡查詢。"""
        self.click(self.locator.btn_search)
        return self

    def get_report_pdf_url(self):
        """查詢後取報表 iframe 的 PDF URL（輪詢等 src 非同步填入 .pdf）。"""
        return self.get_iframe_src(self.locator.iframe_report)

    def parse_report(self, pdf_path):
        """解析訂房數量預估報表 PDF，回傳 Tier 1 斷言所需的結構化結果。

        - text/page_count：原始文字與頁數
        - echo：頁尾查詢回顯（起訖日期）
        - header_fields_present：表頭主要欄位是否存在
        - day_rows / monthly_rows / total_row：依行類型分類的欄位 dict
          （日行 date 為日期；月累計行含「月累計」；合計行 date == '合計'）
        """
        report = report_reader.Report(pdf_path)
        text = report.text
        day_rows, monthly_rows, total_row = [], [], None
        for page_idx in range(report.page_count):
            for row_words in report.rows(page_idx):
                cells = report_reader.cells_by_columns(row_words, self.COLUMNS)
                date_val = cells.get("date", "").strip()
                if not date_val:
                    continue
                if date_val == "合計":
                    total_row = cells
                elif "月累計" in date_val:
                    monthly_rows.append(cells)
                elif self.DATE_PATTERN.match(date_val):
                    day_rows.append(cells)
        return {
            "text": text,
            "page_count": report.page_count,
            "echo": report_reader.parse_query_echo(text, keys=self.ECHO_KEYS),
            "header_fields_present": {field: (field in text) for field in self.HEADER_FIELDS},
            "day_rows": day_rows,
            "monthly_rows": monthly_rows,
            "total_row": total_row,
        }
