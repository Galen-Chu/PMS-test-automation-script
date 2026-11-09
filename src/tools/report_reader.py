"""PDF 報表讀取與座標感知抽取（Selenium-free）。

負責：下載報表 PDF、pdfplumber 解析、依「欄位地圖」做 words → 分行 → 分欄 的
確定性抽取。**不碰 Selenium**——iframe src 由 BasePage.get_iframe_src() 取得後傳入。

每張報表的欄位地圖（columns 的 x 邊界、哪欄放合計）是報表專屬 config，由呼叫端提供；
本模組只提供通用機制。
"""

import io
import re

import pdfplumber
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def download(url, save_to=None, timeout=30):
    """下載報表 PDF。

    URL 由 iframe src 取得，已含存取所需的 token（若該環境有）。
    save_to 給路徑則寫檔並回傳路徑；否則回傳 bytes。
    """
    resp = requests.get(url, verify=False, timeout=timeout)
    resp.raise_for_status()
    content_type = resp.headers.get("content-type", "")
    if "pdf" not in content_type.lower() and resp.content[:5] != b"%PDF-":
        raise ValueError(f"回應非 PDF（content-type={content_type}, url={url.split('?')[0]}）")
    if save_to:
        with open(save_to, "wb") as file:
            file.write(resp.content)
        return save_to
    return resp.content


def to_num(text):
    """'82,000' → 82000；非純數字回傳 None。"""
    text = (text or "").replace(",", "").strip()
    return int(text) if re.fullmatch(r"-?\d+", text) else None


def group_rows(words, y_tol=3):
    """依 top(y) 把 words 聚成視覺行，回傳 [[word, ...], ...]（由上而下，行內由左而右）。"""
    rows = []
    for word in sorted(words, key=lambda w: (w["top"], w["x0"])):
        for row in rows:
            if abs(row[0] - word["top"]) <= y_tol:
                row[1].append(word)
                break
        else:
            rows.append((word["top"], [word]))
    for _, row_words in rows:
        row_words.sort(key=lambda w: w["x0"])
    return [row_words for _, row_words in rows]


def cells_by_columns(row_words, columns):
    """依 x 邊界把一行的 words 分欄。

    columns = [(name, x_lo, x_hi), ...]，以 word 中心 x 落點歸欄。
    回傳 {name: 'joined text'}。
    """
    buckets = {name: [] for name, _, _ in columns}
    for word in row_words:
        center_x = (word["x0"] + word["x1"]) / 2
        for name, lo, hi in columns:
            if lo <= center_x < hi:
                buckets[name].append(word["text"])
                break
    return {name: " ".join(parts).strip() for name, parts in buckets.items()}


def sum_column(rows, col):
    """加總某欄的數值（非數字的欄——表頭/空白/文字——自動略過）。"""
    return sum(num for num in (to_num(row.get(col)) for row in rows) if num is not None)


def parse_query_echo(text, keys=("查詢依據", "列印項目", "廳別", "查詢日期")):
    """解析報表頁尾「查詢條件: 查詢依據: X 列印項目: Y 廳別: Z 查詢日期: D」為 dict。

    用於 Tier 1 查詢回顯驗證（報表確實反映送出的查詢參數）。keys 可依報表調整。

    「查詢條件」後的分隔符 accept: 冒號（半形/全形）或空白——不同報表 PDF 表達方式
    不同（如交班日報表用冒號，到達旅客報表用空白），regex 寬鬆化涵蓋兩種。
    """
    match = re.search(r"查詢條件[:：\s]+(.*)", text)
    segment = match.group(1) if match else text
    key_pattern = "|".join(map(re.escape, keys))
    result = {}
    for item in re.finditer(rf"({key_pattern})[:：]\s*(.*?)(?=(?:{key_pattern})[:：]|$)", segment):
        result[item.group(1)] = item.group(2).strip()
    return result


class Report:
    """解析後的報表：提供原始文字、頁數與座標抽取。"""

    def __init__(self, source):
        """source 可為 PDF bytes 或檔案路徑。"""
        if isinstance(source, (bytes, bytearray)):
            pdf_bytes = source
        else:
            with open(source, "rb") as file:
                pdf_bytes = file.read()
        self._pages_words = []
        texts = []
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            for page in pdf.pages:
                self._pages_words.append(page.extract_words())
                texts.append(page.extract_text() or "")
        self.text = "\n".join(texts)
        self.page_count = len(self._pages_words)

    def rows(self, page=0):
        """回傳指定頁的視覺行（每行為 word list）。"""
        return group_rows(self._pages_words[page])

    def extract_grid(self, columns, key_col, stop_value="合計", page=0):
        """依 columns 分欄逐行掃描，直到 key_col == stop_value（含）為止。

        回傳 (items, total_row)：
          items     = stop 之前的所有列（cell dict）——表頭/空白列會被 sum_column 自動略過
          total_row = 第一個 stop 列（cell dict），沒遇到則 None

        「遇第一個合計即停」用來隔離同名 label（報表下方常有第二、三個「合計」）。
        """
        items, total_row = [], None
        for row_words in self.rows(page):
            cells = cells_by_columns(row_words, columns)
            if cells.get(key_col) == stop_value:
                total_row = cells
                break
            items.append(cells)
        return items, total_row
