from time import sleep
import re
from pages.athena_base_page import AthenaBasePage
from locators.guest_registration_card_locator import GuestRegistrationCardLocator
from tools import report_reader


class GuestRegistrationCardPage(AthenaBasePage):

    def __init__(self, driver):
        super().__init__(driver, GuestRegistrationCardLocator())

    # 旅客住宿登記卡 PDF 欄位地圖（單卡一頁；word 中心 x 落點歸欄，實測 2026-08-17）
    # 值列有三段，靠 signature 行識別後各用各的欄位地圖：
    #   日期列（ikey 8 位數字 signature）：arrival x132 / departure x268 / ikey x398 / room x515
    #   房型/人數列（緊鄰日期列下方）：room_type x117 / person x294 / breakfast x437
    #   金額列（千分位數字 signature）：room_rate x150 / deposit x294 / balance x554
    DATE_COLUMNS = [
        ("arrival", 90, 230),  # 入住日期（與 guest_name 同 x 段，僅日期列用此地圖）
        ("departure", 240, 330),
        ("ikey", 360, 440),
        ("room", 440, 580),  # 未排房為空
    ]
    TYPE_COLUMNS = [
        ("room_type", 90, 230),  # STD/SPT/DSU...
        ("person", 240, 330),  # 住房人數
        ("breakfast", 360, 440),  # 每人每日早餐
    ]
    MONEY_COLUMNS = [
        ("room_rate", 90, 240),  # 房價
        ("deposit", 240, 330),  # 訂金
        ("balance", 440, 580),  # 結餘
    ]
    IKEY_PATTERN = re.compile(r"^\d{8}$")
    MONEY_PATTERN = re.compile(r"^[\d,]+$")

    # ----- 查詢 -----
    def search(self):
        """點放大鏡查詢（ci_dat 預設滾房租日，不需先填日期）。"""
        self.click(self.locator.btn_search)
        return self

    # ----- 資料列選取 -----
    def select_row_by_ikey(self, ikey):
        """click 指定訂房卡號 row（觸發 selection + ck checkbox 連動勾選；單選/多選同一機制，多選連續呼叫）。"""
        self.click(self.format_locator(self.locator.cell_ikey, ikey))
        sleep(0.5)
        return self

    def get_is_prtrent(self, ikey):
        """讀指定 row 的列印房租 cell 值（如 'Y : 是' / 'N : 否'）。"""
        return self.driver.find_element(
            *self.format_locator(self.locator.cell_is_prtrent_by_ikey, ikey)
        ).text

    # ----- 列印（PDF）-----
    def open_print_menu(self):
        """click 列印按鈕展開格式下拉選單（el-dropdown：PDF/EXCEL/WORD）。"""
        self.click(self.locator.btn_print)
        sleep(0.5)
        return self

    def click_print_pdf(self):
        """click PDF 格式：開「旅客登記卡報表」dialog + iframe 載入 PDF 預覽。"""
        self.click(self.locator.li_print_pdf)
        return self

    def get_report_pdf_url(self):
        """取預覽 dialog 內 PDF iframe 的 src（輪詢等 src 含 .pdf）。"""
        return self.get_iframe_src(self.locator.iframe_report)

    # pylint: disable=too-many-locals
    def parse_report(self, pdf_path):
        """解析旅客住宿登記卡 PDF，回傳每頁（每卡）的結構化欄位。

        回傳 {"page_count": N, "cards": [card, ...]}，card 含：
        guest_name / arrival / departure / ikey / room / room_type / person / breakfast /
        room_rate / deposit / balance（字串）+ *_num（to_num 數值，供結餘不變量）。
        未排房卡的 room 為空字串。
        """
        report = report_reader.Report(pdf_path)
        cards = []
        for page in range(report.page_count):
            rows = report.rows(page)
            card = {}
            for row_words in rows:
                texts = [w["text"] for w in row_words]

                # 姓名值列 signature：出現 Mr./Miss.（title 必印）；值在左欄 x90-230
                if "guest_name" not in card and ("Mr." in texts or "Miss." in texts):
                    name_words = [w["text"] for w in row_words if w["x0"] < 290]
                    card["guest_name"] = " ".join(name_words)

                # 日期值列 signature：本行含 8 位數字（ikey）
                ikey_cells = report_reader.cells_by_columns(row_words, self.DATE_COLUMNS)
                ikey = ikey_cells.get("ikey", "").strip()
                if self.IKEY_PATTERN.match(ikey):
                    card["ikey"] = ikey
                    card["arrival"] = ikey_cells.get("arrival", "").strip()
                    card["departure"] = ikey_cells.get("departure", "").strip()
                    card["room"] = ikey_cells.get("room", "").strip()

                # 房型/人數/早餐值列 signature：左欄有全大寫純字母房型代碼（STD/SPT/DSU，2-5 碼）
                if "ikey" in card and "room_type" not in card:
                    left_words = [w for w in row_words if 90 <= (w["x0"] + w["x1"]) / 2 < 230]
                    if any(
                        w["text"].isupper() and w["text"].isalpha() and 2 <= len(w["text"]) <= 5
                        for w in left_words
                    ):
                        type_cells = report_reader.cells_by_columns(row_words, self.TYPE_COLUMNS)
                        card["room_type"] = type_cells.get("room_type", "").strip()
                        card["person"] = type_cells.get("person", "").strip()
                        card["breakfast"] = type_cells.get("breakfast", "").strip()

                # 金額值列 signature：本行全部 word 都是數字/千分位
                if (
                    "room_rate" not in card
                    and texts
                    and all(self.MONEY_PATTERN.match(t) for t in texts)
                ):
                    money = report_reader.cells_by_columns(row_words, self.MONEY_COLUMNS)
                    if report_reader.to_num(money.get("room_rate", "")) is not None:
                        card["room_rate"] = money.get("room_rate", "").strip()
                        card["deposit"] = money.get("deposit", "").strip()
                        card["balance"] = money.get("balance", "").strip()

            if card.get("ikey"):
                for col in ("room_rate", "deposit", "balance"):
                    card[f"{col}_num"] = report_reader.to_num(card.get(col, ""))
                cards.append(card)
        return {"page_count": report.page_count, "cards": cards}

    def find_card(self, parsed, ikey):
        """從 parse_report 結果找指定 ikey 的卡（找不到回 None）。"""
        for card in parsed["cards"]:
            if card["ikey"] == ikey:
                return card
        return None

    def close_report_dialog(self):
        """關閉 PDF 預覽 dialog（panel-tool-close）。"""
        self.click(self.locator.btn_close_report_dialog)
        return self

    # ----- 批次設定 -----
    def open_batch_setting(self):
        """click 批次設定按鈕開 Syncfusion dialog（未選資料時攔 alert #1378）。"""
        self.click(self.locator.btn_batch_setting)
        sleep(0.5)
        return self

    def select_is_print(self, option):
        """列印房租 DropDownList 選是/否（click span 開 popup → click 選項）。"""
        self.click(self.locator.span_is_print)
        sleep(0.5)
        self.click(self.format_locator(self.locator.li_is_print_option, option))
        sleep(0.5)
        return self

    def confirm_batch_setting(self):
        """click 確定送出批次設定（成功 alert「儲存成功」；確定收尾在 test 端 TipComponent）。"""
        self.click(self.locator.btn_batch_confirm)
        sleep(1)
        return self

    def apply_batch_setting(self, ikey, option):
        """完整批次設定序列：選 row → 開 dialog → 選值 → 確定（alert 確定仍由 test 端處理）。"""
        self.select_row_by_ikey(ikey)
        self.open_batch_setting()
        self.select_is_print(option)
        self.confirm_batch_setting()
        return self
