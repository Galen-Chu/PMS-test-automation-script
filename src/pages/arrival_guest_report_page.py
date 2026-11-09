import re
from time import sleep
from pages.athena_base_page import AthenaBasePage
from locators.arrival_guest_report_locator import ArrivalGuestReportLocator
from tools import report_reader


class ArrivalGuestReportPage(AthenaBasePage):

    def __init__(self, driver):
        super().__init__(driver, ArrivalGuestReportLocator())

    # 到達旅客報表 PMS02R0040 欄位地圖（Detail 格式 word 中心 x 落點歸欄）
    # 三行為一筆訂房卡：
    #   第 1 行：訂房卡號(22-62) + 房號(142-162) + 入住日期(302-352) + ...
    #   第 2 行：訂房名稱 + 序號 + ...
    #   第 3 行：關聯單號(22-62，位置同訂房卡號欄) + 訂房類別 + 備註（無入住日期欄）
    # 因訂房卡號 / 關聯單號同 x 範圍，靠「本行是否有入住日期」區分（第 1 行有、第 3 行無）
    DETAIL_COLUMNS = [
        ("ikey_col", 10, 130),  # 訂房卡號 / 關聯單號共用欄位
        ("room_col", 130, 180),  # 房號
        ("date_col", 300, 360),  # 入住日期（用來區分行類型）
        ("_rest", 360, 999),
    ]

    IKEY_PATTERN = re.compile(r"^\d{8}$")
    DATE_PATTERN = re.compile(r"^\d{4}/\d{2}/\d{2}$")
    ROOM_PATTERN = re.compile(r"^\d{2,4}$")

    # 頁尾查詢回顯的 keys（PDF 實際格式：查詢條件 排序方式: X 排除已入住資料: Y 入住日期: D 報表格式: X 列印房租: Y）
    ECHO_KEYS = ("排序方式", "排除已入住資料", "入住日期", "報表格式", "列印房租")

    # Group 格式最後一頁的房型 × 客層小計統計表欄位地圖（實測 word 中心 x 落點）
    SUMMARY_COLUMNS = [
        ("room_type", 170, 250),  # 房型 182-202
        ("guest_f", 400, 470),  # 散客 418-438
        ("guest_c", 480, 550),  # 商務 498-518
        ("guest_g", 560, 630),  # 團體 578-598
        ("subtotal", 640, 710),  # 小計 658-678
    ]

    def expand_advanced(self):
        """展開進階查詢條件區（露出 sort_cod / sql_mod 等）。"""
        self.click(self.locator.btn_condition)
        return self

    def set_is_not_ci(self, checked):
        """設定「排除已入住資料」checkbox 至目標狀態（冪等 setter）。"""
        return self._set_checkbox(
            self.locator.input_is_not_ci_checked, self.locator.label_is_not_ci, checked
        )

    def set_is_print_rent(self, checked):
        """設定「列印房租」checkbox 至目標狀態（冪等 setter）。"""
        return self._set_checkbox(
            self.locator.input_is_print_rent_checked, self.locator.label_is_print_rent, checked
        )

    def _set_checkbox(self, input_locator, label_locator, target_checked):
        # Syncfusion checkbox 真 input hidden，click label 才觸發；attribute checked 有同步（實測）
        current = self.driver.find_element(*input_locator).get_attribute("checked") == "true"
        if current == target_checked:
            return self
        self.click(label_locator)
        return self

    def select_sort_cod(self, option_text):
        """選排序方式（如 'SORT_BY_IKEY : 依訂房卡號排序'）。"""
        return self._select_dropdown(self.locator.input_sort_cod, option_text)

    def select_sql_mod(self, option_text):
        """選報表格式（'group : group' 或 'detail : detail'）。"""
        return self._select_dropdown(self.locator.input_sql_mod, option_text)

    def _select_dropdown(self, input_locator, option_text):
        self.click(input_locator)
        sleep(0.5)
        option = self.format_locator(self.locator.option_dropdown, option_text)
        self.click(option)
        return self

    def query(self):
        """點藍色放大鏡查詢。"""
        self.click(self.locator.btn_search)
        return self

    def get_report_pdf_url(self):
        """查詢後取報表 iframe 的 PDF URL（輪詢等 src 非同步填入）。"""
        return self.get_iframe_src(self.locator.iframe_report)

    def parse_report(self, pdf_path):
        """解析到達旅客報表 PDF，回傳 Tier 1 斷言所需的結構化結果。

        - text/page_count：原始文字與頁數
        - echo：頁尾查詢回顯（排序方式 / 排除已入住資料 / 入住日期 / 報表格式 / 列印房租）
        - header_has_rent：表頭第 2 行是否含「房租」欄（驗列印房租開關）
        - summary_rows / summary_total：Group 格式最後一頁的房型 × 客層小計（Detail 無此表）
        """
        report = report_reader.Report(pdf_path)
        return {
            "text": report.text,
            "page_count": report.page_count,
            "echo": report_reader.parse_query_echo(report.text, keys=self.ECHO_KEYS),
            "header_has_rent": self._header_has_rent(report),
            **self._parse_summary(report),
        }

    def sort_column_values(self, pdf_path, sort_by):
        """抽指定排序欄的值序列（依 PDF 出現順序）供升序斷言。

        sort_by:
          - 'ikey'     → 每筆第 1 行的訂房卡號欄
          - 'link_nos' → 每筆第 3 行的關聯單號欄（同 x 範圍，靠「本行無入住日期」區分）
          - 'room'     → 每筆第 1 行的房號欄（未排房的筆房號為空，會被略過）
        """
        report = report_reader.Report(pdf_path)
        values = []
        for page_idx in range(report.page_count):
            for row_words in report.rows(page_idx):
                cells = report_reader.cells_by_columns(row_words, self.DETAIL_COLUMNS)
                left = cells.get("ikey_col", "").strip()
                if not self.IKEY_PATTERN.match(left):
                    continue
                is_first_row = bool(self.DATE_PATTERN.match(cells.get("date_col", "").strip()))
                if sort_by == "ikey" and is_first_row:
                    values.append(left)
                elif sort_by == "link_nos" and not is_first_row:
                    values.append(left)
                elif sort_by == "room" and is_first_row:
                    room = cells.get("room_col", "").strip()
                    if self.ROOM_PATTERN.match(room):
                        values.append(room)
        return values

    def _header_has_rent(self, report):
        # 表頭第 2 行含「房租」欄 = 送出時列印房租=Y；不含 = N
        # 用第 1 頁 words 判斷（頁尾也有「列印房租」字串，不能用整體 text 直接判斷）
        if report.page_count == 0:
            return False
        for row_words in report.rows(0)[:5]:  # 表頭固定在前 5 行
            texts = [w["text"] for w in row_words]
            if "訂房名稱/團號" in texts and "房租" in texts:
                return True
        return False

    def _parse_summary(self, report):
        # Group 格式報表尾有房型 × 客層小計表（明細 → 總房數/總人數 → 房型 統計 → 頁尾）；
        # 資料量大時統計表會跨頁（前頁收前幾個房型、末頁收其餘 + 小計行），須從
        # 「總房數」行所在頁起掃；Detail 無此表回傳空
        if report.page_count == 0:
            return {"summary_rows": [], "summary_total": None}
        start_page = self._summary_start_page(report)
        rows_data = []
        total = None
        for page_idx in range(start_page, report.page_count):
            for row_words in report.rows(page_idx):
                cells = report_reader.cells_by_columns(row_words, self.SUMMARY_COLUMNS)
                room_type = cells.get("room_type", "").strip()
                subtotal = report_reader.to_num(cells.get("subtotal", ""))
                # 總房數/總人數行 x 落點會撞欄（如總房數→room_type、總金額→subtotal），以「總」開頭排除
                if (
                    subtotal is None
                    or not room_type
                    or room_type == "房型"
                    or room_type.startswith("總")
                ):
                    continue
                if room_type == "小計":
                    total = cells
                else:
                    rows_data.append(cells)
        return {"summary_rows": rows_data, "summary_total": total}

    def _summary_start_page(self, report):
        # 統計表起點 = 「總房數」行所在頁；找不到（格式變動）退回最後一頁（保守）
        for page_idx in range(report.page_count - 1, -1, -1):
            if any(w["text"] == "總房數" for row in report.rows(page_idx) for w in row):
                return page_idx
        return report.page_count - 1
