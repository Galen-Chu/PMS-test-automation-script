import re
from time import sleep
from selenium.webdriver.common.keys import Keys
from pages.athena_base_page import AthenaBasePage
from locators.service_quantity_report_locator import ServiceQuantityReportLocator
from tools import report_reader


class ServiceQuantityReportPage(AthenaBasePage):

    def __init__(self, driver):
        super().__init__(driver, ServiceQuantityReportLocator())

    # 服務數量報表 PMS02R0030 DETAIL 格式欄位地圖（word 中心 x 落點歸欄）
    # 單行一筆服務記錄，11 欄（座標實測，與結構文件 service_quantity_report.md 一致）
    DETAIL_COLUMNS = [
        ("ikey", 0, 80),  # 訂房卡號（如 00008259-1）
        ("room", 80, 130),  # 房號
        ("rate", 130, 190),  # 房價代號
        ("guest", 190, 370),  # 住客姓名
        ("adult", 370, 410),  # 大人
        ("child", 410, 445),  # 小孩
        ("item", 445, 600),  # 服務項目
        ("qty", 600, 645),  # 數量
        ("price", 645, 680),  # 單價
        ("ci", 680, 745),  # 入住日期
        ("co", 745, 820),  # 退房日期
    ]

    IKEY_PATTERN = re.compile(r"^\d{8}-\d+$")

    # 頁尾查詢回顯的 keys（PDF 格式：查詢條件: 查詢日期: D 報表格式: R 排序方式: S 查詢範圍: Q）
    ECHO_KEYS = ("查詢日期", "報表格式", "排序方式", "查詢範圍")

    # SUMMARY 總計區欄位地圖（服務項目 × 數量；總計 label 在前一行 label 欄）
    SUMMARY_TOTAL_COLUMNS = [
        ("label", 160, 200),  # 總計
        ("item", 200, 470),  # 服務項目名稱
        ("qty", 480, 540),  # 數量
    ]

    def set_query_dat(self, date):
        """設定查詢日期（服務發生日，非入住日）。

        query_dat 是 Syncfusion datepicker 雙 input：[2] 才是實際值 input。
        清掉預設值（system_date）後 type 新值，Tab blur 觸發寫入。
        """
        element = self.driver.find_element(*self.locator.input_query_dat)
        element.send_keys(Keys.CONTROL, "a")
        element.send_keys(Keys.DELETE)
        element.send_keys(date)
        element.send_keys(Keys.TAB)
        return self

    def select_sort_by(self, option_text):
        """選排序方式（如 'BY_DATE : 依服務日期'）。"""
        return self._select_dropdown(self.locator.input_sort_by, option_text)

    def select_report_typ(self, option_text):
        """選報表格式（'DETAIL : 明細' 或 'SUMMARY : 彙總'）。

        ⚠️ report_typ 與 template 的 UI label 都是「報表格式」；本 method 靠 data-field-id
        定位的 input_report_typ 區分，不靠 label。
        """
        return self._select_dropdown(self.locator.input_report_typ, option_text)

    def _select_dropdown(self, input_locator, option_text):
        self.click(input_locator)
        sleep(0.5)
        option = self.format_locator(self.locator.option_dropdown, option_text)
        self.click(option)
        return self

    def set_query_range(self, label_text):
        """設定查詢範圍 radio（'CI : 已入住' 或 'ALL : 全部'）。radio 冪等：直接 click 目標 label。"""
        label = self.format_locator(self.locator.label_query_range, label_text)
        self.click(label)
        return self

    def query(self):
        """點藍色放大鏡查詢。"""
        self.click(self.locator.btn_search)
        return self

    def get_report_pdf_url(self):
        """查詢後取報表 iframe 的 PDF URL（輪詢等 src 非同步填入）。"""
        return self.get_iframe_src(self.locator.iframe_report)

    def parse_report(self, pdf_path):
        """解析服務數量報表 PDF，回傳 Tier 1 斷言所需的結構化結果。

        - text/page_count：原始文字與頁數
        - echo：頁尾查詢回顯（查詢日期/報表格式/排序方式/查詢範圍）
        - report_typ：報表格式（DETAIL/SUMMARY，從 echo 推導）
        - summary_total_qty：SUMMARY 總計區數量加總（DETAIL 為 None）
        - summary_items：SUMMARY 各 item「小計 vs 明細加總」一致性（DETAIL 為 []），見 _parse_summary_items
        """
        report = report_reader.Report(pdf_path)
        echo = report_reader.parse_query_echo(report.text, keys=self.ECHO_KEYS)
        report_typ = echo.get("報表格式", "")
        return {
            "text": report.text,
            "page_count": report.page_count,
            "echo": echo,
            "report_typ": report_typ,
            "summary_total_qty": (
                self._parse_summary_total(report) if report_typ == "SUMMARY" else None
            ),
            "summary_items": self._parse_summary_items(report) if report_typ == "SUMMARY" else [],
        }

    def sort_column_values(self, pdf_path, sort_by):
        """抽 DETAIL 格式指定排序欄的值序列（依 PDF 出現順序）供升序斷言。

        sort_by:
          - 'ikey' → 訂房卡號欄
          - 'room' → 房號欄（未排房的筆房號為空會被略過）

        BY_DATE / BY_ITEM 不支援：自測環境單一服務日 / 單一服務項目，排序值全相同，
        無法以升序斷言驗證；相關組合只靠 echo 回顯確認參數送出。
        """
        report = report_reader.Report(pdf_path)
        values = []
        for page_idx in range(report.page_count):
            for row_words in report.rows(page_idx):
                cells = report_reader.cells_by_columns(row_words, self.DETAIL_COLUMNS)
                ikey = cells.get("ikey", "").strip()
                if not self.IKEY_PATTERN.match(ikey):
                    continue  # 跳過小計/合計/製表者/echo 等非資料行
                if sort_by == "ikey":
                    values.append(ikey)
                elif sort_by == "room":
                    room = cells.get("room", "").strip()
                    if room:
                        values.append(room)
        return values

    def _parse_summary_total(self, report):
        # SUMMARY 總計區：找「總計」label 行，往後 4 行內收「服務項目 + 數量」加總。
        # 單一服務項目收 1 筆；多項目加總（目前自測環境僅單項 2009:早餐拆帳大人）。
        if report.page_count == 0:
            return None
        last_page = report.page_count - 1
        rows = report.rows(last_page)
        for i, row_words in enumerate(rows):
            cells = report_reader.cells_by_columns(row_words, self.SUMMARY_TOTAL_COLUMNS)
            if cells.get("label") == "總計":
                total = 0
                found = False
                for j in range(i + 1, min(i + 5, len(rows))):
                    data = report_reader.cells_by_columns(rows[j], self.SUMMARY_TOTAL_COLUMNS)
                    item = data.get("item", "").strip()
                    qty = report_reader.to_num(data.get("qty", ""))
                    if item and qty is not None:
                        total += qty
                        found = True
                return total if found else None
        return None

    def _parse_summary_items(self, report):  # pylint: disable=too-many-locals
        """SUMMARY 各服務項目一致性（B 不變量）：每個 item 小計 == 該 item 明細數量加總。

        parse 策略（不靠 item 名稱邊界，靠小計值分組）：
        - 小計行（x190-250 有數字）→ 往後找最近的純數量行配對
        - 純數量行 = x258-820 全數字 + x190-250 無數字（排除房號行/頁碼/echo/總計表頭）
        - 按小計值分組（同值 = 同 item 多排重印），各組 detail_sum = 數量加總

        回傳 [{"subtotal": N, "detail_sum": M, "match": N == M}, ...]。

        邊界：兩 item 小計剛好相同會合併（detail_sum 變兩 item 加總 → match False 抓到，
        屬 false alarm，機率低接受）；跨頁小計/數量行未處理（SUMMARY 通常短）。
        """
        if report.page_count == 0:
            return []
        subtotal_x = (190, 250)
        qty_x = (258, 820)
        groups = {}
        for page_idx in range(report.page_count):
            rows = report.rows(page_idx)
            n = len(rows)
            for i, row_words in enumerate(rows):
                # 小計行：subtotal_x 範圍有數字
                subtotal = None
                for w in row_words:
                    cx = (w["x0"] + w["x1"]) / 2
                    if subtotal_x[0] <= cx < subtotal_x[1]:
                        num = report_reader.to_num(w["text"])
                        if num is not None:
                            subtotal = num
                            break
                if subtotal is None:
                    continue
                # 往後找純數量行，遇下一個小計行就停（本小計行無對應數量行）
                detail = 0
                for j in range(i + 1, n):
                    next_has_subtotal = any(
                        report_reader.to_num(w["text"]) is not None
                        for w in rows[j]
                        if subtotal_x[0] <= (w["x0"] + w["x1"]) / 2 < subtotal_x[1]
                    )
                    if next_has_subtotal:
                        break
                    qty_words = [
                        w for w in rows[j] if qty_x[0] <= (w["x0"] + w["x1"]) / 2 < qty_x[1]
                    ]
                    if not qty_words:
                        continue
                    nums = [report_reader.to_num(w["text"]) for w in qty_words]
                    if all(num is not None for num in nums):
                        detail = sum(nums)
                        break
                groups[subtotal] = groups.get(subtotal, 0) + detail
        return [
            {"subtotal": sub, "detail_sum": det, "match": sub == det}
            for sub, det in sorted(groups.items())
        ]
