import time

from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from pages.athena_base_page import AthenaBasePage
from locators.co_list_locator import CoListLocator


class CoListPage(AthenaBasePage):

    def __init__(self, driver):
        super().__init__(driver, CoListLocator())

    # ----- 搜尋 + 選卡 -----

    def search_by_guest_name(self, guest_name):
        """輸入住客姓名並搜尋（先清空所有搜尋欄，避免與房號搜尋條件殘留交互）"""
        self.click(self.locator.btn_clear)
        self.input_with_clear(self.locator.input_guest_name, guest_name)
        self.click(self.locator.btn_search)
        return self

    def search_by_room_no(self, room_no):
        """輸入房號並搜尋（轉帳驗證用：目標帳戶與來源不同姓名，改用房號定位）。
        先清空所有搜尋欄，避免與姓名搜尋條件殘留交互。"""
        self.click(self.locator.btn_clear)
        self.input_with_clear(self.locator.input_room_nos, room_no)
        self.click(self.locator.btn_search)
        return self

    def click_card_row(self, room_no):
        """點選 C/O 清單 Grid 中指定房號的資料列（需先搜尋確保房號唯一）"""
        locator = self.format_locator(self.locator.cell_room_nos, room_no)
        self.click(locator)
        return self

    def click_checkout_tab(self):
        """切換 C/O 清單 Check Out 頁籤（退房後記錄；#486 Then 驗證）。"""
        self.click(self.locator.tab_checkout)
        return self

    def click_inhouse_tab(self):
        """切換 C/O 清單 In House 頁籤（#509 退房還原後驗證回 In house）。"""
        self.click(self.locator.tab_inhouse)
        return self

    def click_restore_checkout(self):
        """Check Out tab 退房還原按鈕（text 定位避 r_1040 衝突；#509 When）。"""
        self.click(self.locator.btn_restore_checkout)
        return self

    def click_checkedout_toolbar(self):
        """Check Out tab 已結帳按鈕（開已結帳 dialog；#512 入口 A）。"""
        self.click(self.locator.btn_checkedout_toolbar)
        return self

    def click_cancel_checkout_record(self):
        """已結帳 dialog 結帳還原（撤銷當筆結帳記錄；#512 When）。"""
        self.click(self.locator.btn_cancel_checkout_record)
        return self

    def close_checkedout_dialog(self):
        """關閉已結帳 dialog（#512 結帳還原後，切 C/O 清單 tab 前需關，避 dialog 擋 tab）。"""
        self.click(self.locator.btn_close_checkedout_dialog)
        return self

    def click_edit_payment(self):
        """已結帳 dialog 更改付款方式（開更改付款方式 dialog；#514 When）。"""
        self.click(self.locator.btn_edit_payment)
        return self

    def click_clear_payment(self):
        """更改付款方式 dialog 清除付款（清原付款，綠色加號出現；#514 When）。"""
        self.click(self.locator.btn_clear_payment)
        return self

    def click_do_save(self):
        """更改付款方式 dialog 橘色磁碟片儲存 doSave（#514 When）。"""
        self.click(self.locator.btn_do_save)
        return self

    def has_card_row(self, room_no):
        """當前 grid 是否有該房號 row（#486 切 Check Out 後驗證退房資料顯示）。
        多 grid 共用 room_nos field，is_displayed 過濾避隱藏 grid 同房號 cell。"""
        locator = self.format_locator(self.locator.cell_room_nos, room_no)
        return any(el.is_displayed() for el in self.driver.find_elements(*locator))

    def click_open_guest_account(self):
        """點擊「住客帳維護」(co_Button)，開啟住客帳維護單筆 dialog。
        未開班時會先彈開班 dialog（session 級，由 caller 偵測 dialog_shift 處理）。"""
        self.click(self.locator.btn_open_guest_account)
        return self

    def close_guest_account_dialog(self):
        """關閉住客帳維護單筆 dialog（panel-title scope，避免打到 hidden close）。
        轉帳驗證用：關閉來源 dialog 才能回 C/O 清單重搜目標帳戶。"""
        self.click(self.locator.btn_close_guest_account)
        return self

    # ----- 入帳（轉帳前置：建立可轉消費）-----

    def enter_consumption(self, item, folio):
        """入帳一筆消費作為轉帳標的。可循環入帳（每次新增，作為「入帳取代復原」解法）。

        item: 消費代號 Element UI el-select（如 '1001 : 房租'，單價自動帶入）
        folio: 入帳帳夾 EasyUI combobox（'1'=住客帳 folio，確保消費留在來源可轉出）
        """
        self.click(self.locator.btn_open_entry)
        self.sleep(1)
        # 消費代號（Element UI）：click input 開 dropdown → click option
        self.click(self.locator.input_entry_item)
        self.sleep(1)
        locator_item = self.format_locator(self.locator.select_option, item)
        self.click(locator_item)
        # 帳夾（EasyUI combobox，select 指令不支援，手動 click input → click combobox-item）
        self.click(self.locator.input_entry_folio)
        self.sleep(0.5)
        locator_folio = self.format_locator(self.locator.select_option_by_combobox_item, folio)
        self.click(locator_folio)
        # save（消費即寫入主帳）
        self.click(self.locator.btn_entry_save)
        self.sleep(1)
        # 關閉入帳 panel（否則遮擋工具列轉帳鈕，click intercepted）
        self.click(self.locator.btn_close_entry_panel)
        return self

    # ----- 轉帳（Gherkin 步驟對應，拆細讓 allure.step 清楚）-----

    def click_open_transfer_item(self):
        """點擊工具列「轉帳」鈕，開啟轉帳項目選擇 dialog（入帳 panel 需先關閉）"""
        self.click(self.locator.btn_open_transfer_item)
        return self

    def select_transfer_item_folio(self, folio):
        """選轉帳項目選擇 dialog 的帳夾（多 folio 帳戶需手動選，grid 才載入消費）。
        單 folio 帳戶（如 PM房）dialog 預設帶入 folio，免呼叫。

        folio: EasyUI combobox-item text（如 '1:1' = folio_nam:folio_nos）
        """
        self.click(self.locator.input_transfer_item_folio)
        self.sleep(0.5)
        locator = self.format_locator(self.locator.select_option_by_combobox_item, folio)
        self.click(locator)
        self.sleep(0.5)
        return self

    def check_transfer_item_first(self):
        """勾選轉帳項目選擇 dialog 第一筆未勾消費 checkbox（勾任一筆，不定位特定筆）。
        事後 acct_nos diff 精確追蹤轉出哪一筆，取代全轉 + 來源清空 assert（假綠源頭）。"""
        elements = self.driver.find_elements(*self.locator.checkbox_transfer_item)
        unchecked = [e for e in elements if not e.is_selected()]
        if unchecked:
            unchecked[0].click()
            self.sleep(0.3)
        return self

    def click_open_transfer_folio(self):
        """點擊轉帳項目選擇 dialog 內「轉帳」，開啟轉帳帳夾選擇 dialog"""
        self.click(self.locator.btn_open_transfer_folio)
        return self

    def click_transfer_target_type(self, target_type):
        """勾選轉帳帳夾選擇的轉帳對象 radio。
        target_type: radio label 關鍵字（'相同訂房卡'/'全部房號'/'選擇房號'）
        """
        locator = self.format_locator(self.locator.label_transfer_target_type, target_type)
        self.click(locator)
        return self

    def type_transfer_room_filter(self, keyword):
        """轉帳帳夾選擇 dialog 輸入房號過濾（選擇房號 radio 時用）。
        type 即時過濾 grid，不需 Enter。keyword 如 'C' 過濾現金帳（C 開頭房號）。
        """
        self.input_with_clear(self.locator.input_transfer_room_filter, keyword)
        self.sleep(1)
        return self

    def click_transfer_target_room(self, room_no):
        """點擊上層 grid 目標房 row（相同訂房卡下的 PM房）"""
        locator = self.format_locator(self.locator.cell_transfer_target_room, room_no)
        self.click(locator)
        return self

    def click_transfer_target_folio(self, folio_no):
        """點擊下層 grid 目標 folio row（click 目標房後才展開）"""
        locator = self.format_locator(self.locator.cell_transfer_target_folio, folio_no)
        self.click(locator)
        return self

    def click_confirm_transfer(self):
        """點擊轉帳確認（不可逆，消費從來源移到目標 folio）"""
        self.click(self.locator.btn_confirm_transfer)
        return self

    def close_transfer_item_dialog(self):
        """關閉轉帳項目選擇 dialog（轉帳後不自動關閉，folio tab 顯示未刷新）"""
        self.click(self.locator.btn_close_transfer_item_dialog)
        return self

    # ----- 驗證 -----

    def get_folio_tab_text(self, folio_no):
        """讀住客帳維護 folio tab 顯示文字。
        格式 '<folio> (<帳夾總額>)'，如 '1 (1,000)' = folio 1 帳夾總額 1,000。"""
        locator = self.format_locator(self.locator.text_folio_tab, folio_no)
        return self.driver.find_element(*locator).text

    def get_folio_tab_amount(self, folio_no):
        """讀 folio tab 的帳夾總金額（轉帳驗證用：目標帳夾轉入金額 == 來源轉出金額）。
        目標帳戶可能有大量歷史消費，比筆數/代號可靠。
        tab 格式 '<folio> (<金額>)'，如 '1 (1,000)' → 1000。"""
        text = self.get_folio_tab_text(folio_no)
        amount_str = text.split("(")[1].split(")")[0].replace(",", "")
        return int(amount_str)

    def has_folio_tab(self, folio_no):
        """偵測 folio tab 是否存在（folio2 首次 add 前可能無 tab，移動守恆驗證用）。"""
        locator = self.format_locator(self.locator.text_folio_tab, folio_no)
        elements = self.driver.find_elements(*locator)
        return len(elements) > 0

    def switch_folio_tab(self, folio_no):
        """切換住客帳維護的 folio tab（消費 grid 只顯示當前 tab 的消費）。
        讀取特定 folio 的 acct_nos 前須先切到該 tab。"""
        locator = self.format_locator(self.locator.text_folio_tab, folio_no)
        self.click(locator)
        return self

    def get_folio_acct_nos(self, folio_no):
        """讀住客帳維護指定 folio 的所有消費 acct_nos（唯一流水號 set）。

        acct_nos 為隱藏欄（display:none），Selenium .text 回空字串，須用 textContent。
        切到目標 folio tab 後讀取（grid 只顯示當前 tab 消費）。回傳 acct_nos 字串 set，
        供前後 diff 精確追蹤消費移動（同一筆移動流水號不變，取代金額守恆的假綠）。
        累積制卡 >50 筆時 grid 分頁（EasyUI 50/頁）——diff 用途須收集全部頁，
        只讀單頁（含跳末頁）會因新筆插入位置讀不到而 diff 殘缺（#292 炸點：
        106 筆 3 頁，before/after 各讀末頁 diff 不到本次新增筆）。
        """
        self.switch_folio_tab(folio_no)
        self.sleep(0.5)
        # 回第 1 頁從頭收集（冪等——已在第 1 頁 no-op），逐頁翻到末頁
        self.click(self.locator.btn_folio_grid_first_page)
        self.sleep(0.5)
        acct_nos = set()
        while True:
            # retry：消費 grid 重新渲染（virtual rendering）偶發讓 element 參考失效
            for _ in range(3):
                try:
                    elements = self.driver.find_elements(*self.locator.cell_acct_nos)
                    acct_nos.update(e.get_attribute("textContent").strip() for e in elements)
                    break
                except StaleElementReferenceException:
                    self.sleep(0.3)
            if self._folio_grid_on_last_page():
                return acct_nos
            self.click(self.locator.btn_folio_grid_next_page)
            self.sleep(0.5)

    def _folio_grid_on_last_page(self):
        # pager「Displaying X to Y of Z items」Y==Z = 已在末頁；單頁時 Y 即 Z
        text = self.driver.find_element(*self.locator.text_folio_grid_pager).text
        showing = text.split("to")[1].split("of")[0].strip()
        total = text.split("of")[1].split()[0].strip()
        return showing == total

    def get_folio_consumable_acct_nos(self, folio_no):
        """讀指定 folio 的正消費 acct_nos set（排除訂金——ensure_folio_clean 判據用）。

        訂金列 item_nam 前綴 'dd:'，不可註銷屬正常殘留，納入判據會永遠判沒清乾淨。
        辨識用消費代號前綴非 item_tot 負數（負數亦見於重分類抵銷項，#553）。
        全頁收集對齊 get_folio_acct_nos（判斷正消費有無須與全量一致）。
        """
        acct_nos = set()
        for nam, nos, _tot in self._iter_folio_rows(folio_no):
            # 空值 row（ghost placeholder）排除
            if nam and nos and not nam.startswith("dd:"):
                acct_nos.add(nos)
        return acct_nos

    def _iter_folio_rows(self, folio_no):
        """逐頁遍歷指定 folio 消費 grid 的 (item_nam, acct_nos, item_tot)（全頁收集）。

        回第 1 頁從頭遍歷、翻到末頁（pager Y==Z 判斷）——>50 筆分頁時
        單頁讀取會漏筆（新筆插頭部）。item_tot 為原始文字（千分位逗號留呼叫端 parse）。
        """
        self.switch_folio_tab(folio_no)
        self.sleep(0.5)
        self.click(self.locator.btn_folio_grid_first_page)
        self.sleep(0.5)
        while True:
            # retry：負載下 grid 渲染替換讓 row 參考失效
            for _ in range(3):
                try:
                    rows = self.driver.find_elements(*self.locator.row_folio_consume)
                    pairs = [
                        (
                            row.find_element(*self.locator.cell_item_nam_in_row).text.strip(),
                            row.find_element(*self.locator.cell_acct_nos_in_row)
                            .get_attribute("textContent")
                            .strip(),
                            row.find_element(*self.locator.cell_item_tot_in_row).text.strip(),
                        )
                        for row in rows
                    ]
                    break
                except StaleElementReferenceException:
                    self.sleep(0.3)
                    pairs = []
            yield from pairs
            if self._folio_grid_on_last_page():
                return
            self.click(self.locator.btn_folio_grid_next_page)
            self.sleep(0.5)

    # ----- 對帳（#464 預估款轉帳：folio 新增 vs 預估款當天）-----

    def get_folio_item_nams_by_acct_nos(self, folio_no, acct_nos_set):
        """讀 folio 指定 acct_nos set 對應的 item_nam set（#464 對帳用）。
        folio grid row 的 acct_nos（hidden textContent）配對 item_nam（visible .text）。
        全頁遍歷篩 acct_nos in set 讀 item_nam——單頁讀取在分頁卡上
        會 miss（新筆插頭部、頁面可能停末頁）。"""
        nams = set()
        for nam, nos, _tot in self._iter_folio_rows(folio_no):
            if nos in acct_nos_set:
                nams.add(nam)
        return nams

    def get_folio_items_by_acct_nos(self, folio_no, acct_nos_set):
        """讀 folio 指定 acct_nos set 的 (item_nam, item_tot) 清單（#292 對帳用）。
        房務入帳每筆生 2 筆消費（貨款+服務費）acct_nos 連號，以 acct_nos diff 鎖定
        本次新增筆後讀名稱與金額精確比對。全頁遍歷配對（分頁卡單頁讀取會 miss）。"""
        items = []
        for nam, nos, tot in self._iter_folio_rows(folio_no):
            if nos in acct_nos_set:
                items.append((nam, int(tot.replace(",", ""))))
        return items

    def get_folio_negative_items(self, folio_no):
        """讀 folio grid item_tot 為負值的 item（item_nam -> item_tot int dict）。
        轉住宿期間後 folio1 含負數抵銷 item（#553 Then：原當天消費重分類到 folio99）。"""
        self.switch_folio_tab(folio_no)
        self.sleep(0.5)
        negatives = {}
        for row in self.driver.find_elements(*self.locator.row_folio_consume):
            item_nam = row.find_element(*self.locator.cell_item_nam_in_row).text.strip()
            item_tot_text = row.find_element(*self.locator.cell_item_tot_in_row).text.strip()
            item_tot = int(item_tot_text.replace(",", ""))
            if item_tot < 0:
                negatives[item_nam] = item_tot
        return negatives

    def get_estimate_today_items(self):
        """讀預估款維護 grid「當天」（最早 acct_dat，今天以後 filter）的 item_nos set（#464 對帳用）。
        預估款維護 dialog 需已開。chain 新建卡預估款都未入帳，當天 item_nos = 當天轉帳會入帳的內容。
        最早 acct_dat = 今天（grid「只顯示今天以後」filter，最早是今天）。"""
        dates = {}
        for row in self.driver.find_elements(*self.locator.row_estimate):
            acct_dat = row.find_element(*self.locator.cell_acct_dat_in_row).text.strip()
            item_nos = row.find_element(*self.locator.cell_item_nos_in_row).text.strip()
            dates.setdefault(acct_dat, set()).add(item_nos)
        if not dates:
            return set()
        return dates[min(dates)]

    # ----- 指定訂金（#488）-----

    def click_open_assign_deposit(self):
        """點擊「指定訂金」(r_1130)，開啟指定訂金 dialog。"""
        self.click(self.locator.btn_open_assign_deposit)
        return self

    def has_assigned_deposit(self):
        """偵測指定訂金 dialog 是否已帶訂金（deposit_nos textbox-value 非空）。
        循環解用：已綁則需先刪除才能重新綁定（同訂金+同帳夼重複 save 報「資料無異動」）。"""
        value = self.driver.find_element(*self.locator.input_deposit_nos_value).get_attribute(
            "value"
        )
        return bool(value)

    def clear_deposit_nos(self):
        """清空 deposit_nos combogrid 的 textbox-text（循環解刪除已綁訂金）。

        EasyUI combogrid 的 textbox-text not interactable（Selenium send_keys 失敗），
        且 combogrid 無 native clear API，需 execute_script 觸發 change 讓 combogrid
        更新 value。為 test code 唯一使用 JS 的操作（框架限制，非 locator 問題）。
        """
        script = (
            "var inp=arguments[0]; inp.focus(); inp.select(); "
            "document.execCommand('delete'); "
            "inp.dispatchEvent(new Event('change',{bubbles:true}));"
        )
        inp = self.driver.find_element(*self.locator.input_deposit_nos_text)
        self.driver.execute_script(script, inp)
        return self

    def select_deposit(self, deposit_name):
        """combogrid 選訂金帳戶（click combo-arrow 開 dropdown → click alt_nam row）。
        deposit_name: combogrid alt_nam 欄位值（如 'Checkout Deposit'）。"""
        self.click(self.locator.btn_deposit_combo_arrow)
        self.sleep(0.5)
        locator = self.format_locator(self.locator.cell_deposit_option, deposit_name)
        self.click(locator)
        return self

    def select_deposit_folio(self, folio):
        """選使用訂金的帳夼（EasyUI combobox，'1:1' = folio_nam:folio_nos）。"""
        self.click(self.locator.input_dps_folio_nos)
        self.sleep(0.5)
        locator = self.format_locator(self.locator.select_option_by_combobox_item, folio)
        self.click(locator)
        return self

    def click_save_assign_deposit(self):
        """點擊指定訂金 dialog save（綁定或刪除）。save 後「儲存成功」alert。"""
        self.click(self.locator.btn_save_assign_deposit)
        return self

    def close_assign_deposit_dialog(self):
        """關閉指定訂金 dialog（save 刪除後 folio tab 即時刷新，可不關；復原流程關掉較乾淨）。"""
        self.click(self.locator.btn_close_assign_deposit)
        return self

    # ----- 單筆拆帳（#555）-----

    def click_consumption_last(self, item_name):
        """點擊消費款項 Grid 最後一筆指定名稱消費（剛入帳新消費 acct_nos 最大）。
        item_name: item_nam 值（如 '1001:房租'）。split_value 依賴標的金額故須拆剛入帳筆。"""
        locator = self.format_locator(self.locator.cell_consumption_last, item_name)
        self.click(locator)
        return self

    def click_split(self):
        """點擊「單筆拆帳」(split)，開啟「請輸入拆分方式」dialog（需先選 Grid 行）。"""
        self.click(self.locator.btn_split)
        return self

    def select_split_method(self, method):
        """選拆分方式（Syncfusion DDL，native click span 開 + click li 選）。
        method: 選項關鍵字（'AMOUNT'/'PERCENT'/'AVERAGE'）。"""
        self.click(self.locator.span_split_rule)
        self.sleep(0.3)
        locator = self.format_locator(self.locator.li_split_rule_option, method)
        self.click(locator)
        return self

    def input_split_value(self, value):
        """輸入拆分值（Syncfusion numeric input）。"""
        self.input_with_clear(self.locator.input_split_value, str(value))
        return self

    def click_split_confirm(self):
        """點擊拆帳 dialog 確定（1 筆拆成 2 筆，帳夾總額不變）。"""
        self.click(self.locator.btn_split_confirm)
        return self

    def get_consumption_count(self):
        """住客帳維護消費款項 Grid 的資料筆數（拆帳驗證用：1 筆拆 2 筆 → +1）。"""
        rows = self.driver.find_elements(*self.locator.row_consumption)
        return len(rows)

    # ----- 帳夾管理 / 移動帳夾（#559）-----

    def click_open_folio_management(self):
        """點擊「帳夾管理」(r_1030)，開啟帳夾管理 dialog（雙 Grid：消費款項 + 帳夾）。"""
        self.click(self.locator.btn_open_folio_management)
        return self

    def check_folio_mgmt_consumption_first(self):
        """勾選帳夾管理消費款項 Table 第一筆消費 ck（不定位特定筆）。
        帳夾管理無 acct_nos 且排序不同，無法可靠定位特定筆；勾任一筆，
        事後在住客帳維護用 acct_nos diff 精確追蹤移動哪一筆。"""
        self.click(self.locator.checkbox_folio_consume_first)
        return self

    def select_folio_in_table(self, folio_no):
        """選帳夾 Table 的 folio row（移動目標）。folio_no: folio_nam 值（如 '2'）。"""
        locator = self.format_locator(self.locator.cell_folio_in_table, folio_no)
        self.click(locator)
        return self

    def click_folio_move(self):
        """點擊「移動」（需先勾消費 ck + 選帳夼 folio row 才 enabled）。"""
        self.click(self.locator.btn_folio_move)
        return self

    def click_folio_save(self):
        """點擊帳夾管理 save（移動生效）。save 後「儲存成功」alert。"""
        self.click(self.locator.btn_folio_save)
        return self

    def close_folio_management(self):
        """關閉帳夾管理 dialog。⚠️ save 後 folio tab 不即時刷新，需關 dialog 才刷新。"""
        self.click(self.locator.btn_close_folio_management)
        return self

    # ----- 結帳 / 付款方式（#496）-----

    def get_account_status(self):
        """讀帳戶狀態 combobox 值（復原判斷用）。回傳如 'O : 開帳' / 'K : 關帳'。"""
        return self.driver.find_element(*self.locator.text_account_status).get_attribute("value")

    def is_account_open(self):
        """帳戶狀態是否 O:開帳（#496 起點；K:關帳需開帳復原）。"""
        return "O" in self.get_account_status()

    def click_toggle_account(self):
        """點擊開關帳 toggle（K→O 需 alertOK『是否要開帳?』；O→K 需 alertOK『是否要關帳?』）。"""
        self.click(self.locator.btn_toggle_account)
        return self

    def click_checkout_toolbar(self):
        """點擊住客帳維護工具列『結帳』(r_PMS0310011_1100)，觸發關帳流程（未關帳 alert『是否要關帳?』）。"""
        self.click(self.locator.btn_checkout_toolbar)
        return self

    def click_add_payment(self):
        """點擊綠色加號(sub-button--add)新增付款方式，觸發『請輸入付款方式』dialog。"""
        self.click(self.locator.btn_add_payment)
        return self

    def select_payment_method(self, code):
        """選付款方式（Element UI el-select）。code: '10' 現金 / '31' VISA / '00' 沖訂金。
        contains 代號匹配避選項全形空白問題。
        Element UI el-select 需 JS click 開 dropdown + JS click option（native click input
        不開、native click option 抓 hidden li），複製 CLI select 指令完整邏輯（同
        clear_deposit_nos 的框架限制例外，非 locator 問題）。
        動畫視窗期：click 後 dropdown options 需數幀才掛上，單次 query 撲空會靜默失效
        ——Python 端輪詢（每次 execute_script 間隔讓出 JS thread，動畫才能推進；不可用
        JS busy-loop，同步 loop 會凍結 main thread 反而讓 dropdown 永遠展不開）。"""
        sel = self.driver.find_element(*self.locator.select_pay_way)
        self.driver.execute_script("arguments[0].click()", sel)
        keyword = f"{code}:"
        deadline = time.monotonic() + 2
        clicked = False
        while time.monotonic() < deadline:
            clicked = self.driver.execute_script(
                """
                var kw = arguments[0];
                var dds = document.querySelectorAll('.el-select-dropdown');
                for (var d = dds.length - 1; d >= 0; d--) {
                    var dd = dds[d];
                    if (dd.style.display === 'none' || dd.offsetHeight === 0) continue;
                    var items = dd.querySelectorAll('li.el-select-dropdown__item');
                    if (items.length === 0) continue;
                    for (var i = 0; i < items.length; i++) {
                        var t = items[i].textContent.replace(/\\s/g, '');
                        if (t.indexOf(kw) >= 0) { items[i].click(); return true; }
                    }
                }
                return false;
            """,
                keyword,
            )
            if clicked:
                break
            self.sleep(0.2)
        if not clicked:
            raise NoSuchElementException(
                f"付款方式選項未選到: {keyword}（2s 內 dropdown 無 visible options）"
            )
        return self

    def input_credit_card(self, card_nos, mm, yyyy):
        """填信用卡號 + 有效月/年（選信用卡後動態長出 3 欄，現金無此分支）。
        完全複製 CLI type 邏輯（scrollIntoView + click + CONTROL+a + send_keys）：
        credit_nos 在結帳 dialog 內深處，沒 scrollIntoView 時 send_keys 不寫入 DOM value。"""
        self.sleep(1)  # 等信用卡欄位動態長出 + Vue render 穩定
        for locator, val in [
            (self.locator.input_credit_nos, card_nos),
            (self.locator.input_expira_mm, mm),
            (self.locator.input_expira_yyyy, yyyy),
        ]:
            el = self.driver.find_element(*locator)
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'})", el)
            self.sleep(0.2)
            el.click()
            el.send_keys(Keys.CONTROL, "a")
            el.send_keys(val)
        return self

    def input_sign_company(self, company_name):
        """客戶簽帳(41)選簽帳公司（EasyUI combogrid）。
        combogrid textbox-text not interactable（send_keys 失敗，#488 同證），用 JS：
        setValue + dispatch input（combogrid 接收值）→ dispatch keydown Enter
        （觸發 server-side 查詢載入公司列表）→ click 公司 row（textContent match）。
        自動帶入 sign_nam/cust_nam/uni_cod/信用額度。操作序列 CLI 實測驗證
        （type --enter + js click row → cust_cod=WEB00000，2026-07-29 Phase 2）。"""
        sel = self.driver.find_element(*self.locator.input_sign_cust_cod)
        self.driver.execute_script(
            "var el=arguments[0], name=arguments[1];"
            "el.scrollIntoView({block:'center'});"
            "el.focus(); el.value=name;"
            "el.dispatchEvent(new Event('input',{bubbles:true}));"
            "el.dispatchEvent(new KeyboardEvent('keydown',{key:'Enter',code:'Enter',keyCode:13,bubbles:true}));",
            sel,
            company_name,
        )
        self.sleep(0.6)
        self.driver.execute_script(
            "var name=arguments[0];"
            "var rows=document.querySelectorAll('div.combo-p tr.datagrid-row');"
            "for (var i=0;i<rows.length;i++){"
            "if (rows[i].textContent.indexOf(name)>=0){rows[i].click();return;}}",
            company_name,
        )
        return self

    def select_deposit_in_payment(self, deposit_name):
        """更改付款方式 dialog 內 deposit_nos combogrid 選訂金帳戶（EasyUI combogrid，跨卡選項）。
        native combo-arrow 被 textbox-text overlay + send_keys 不觸發 combogrid filter，沿用
        input_sign_company JS 模式（setValue+dispatch+Enter 開 panel filter → JS click row
        textContent match）。deposit_name: combogrid alt_nam 欄位值（跨卡訂金帳戶名）。"""
        sel = self.driver.find_element(*self.locator.input_deposit_nos_text)
        self.driver.execute_script(
            "var el=arguments[0], name=arguments[1];"
            "el.scrollIntoView({block:'center'});"
            "el.focus(); el.value=name;"
            "el.dispatchEvent(new Event('input',{bubbles:true}));"
            "el.dispatchEvent(new KeyboardEvent('keydown',{key:'Enter',code:'Enter',keyCode:13,bubbles:true}));",
            sel,
            deposit_name,
        )
        self.sleep(0.7)
        self.driver.execute_script(
            "var name=arguments[0];"
            "var rows=document.querySelectorAll('div.combo-p tr.datagrid-row');"
            "for (var i=0;i<rows.length;i++){"
            "if (rows[i].textContent.indexOf(name)>=0){rows[i].click();return;}}",
            deposit_name,
        )
        return self

    def input_pay_amt(self, amount):
        """type 付款金額（Syncfusion numeric，多筆分攤用）。
        單筆自動帶入應收免 type；多筆分攤需 type 改值。
        scroll/CONTROL+a 同 input_credit_card（Syncfusion numeric 深處 send_keys 需 scroll）。"""
        el = self.driver.find_element(*self.locator.input_pay_amt)
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'})", el)
        self.sleep(0.2)
        el.click()
        el.send_keys(Keys.CONTROL, "a")
        el.send_keys(str(amount))
        return self

    def get_pay_way_value(self):
        """讀付款方式 dialog 的 el-select 帶入值（#601 驗證簽帳 41 自動帶入用）。"""
        return self.driver.find_element(*self.locator.input_pay_way_value).get_attribute("value")

    def get_sign_cust_cod_value(self):
        """讀簽帳公司 combogrid 帶入值（#601 驗證訂房公司自動帶入，'代號:名稱'）。"""
        return self.driver.find_element(*self.locator.input_sign_cust_cod).get_attribute("value")

    def close_sign_pay_dialogs(self, tip):
        """#601 收尾：不結帳關閉付款方式 → 結帳兩層 dialog（簽帳結帳流程由 #496 覆蓋）。

        關閉鏈（CLI 實證）：付款方式 close → 「資料尚未儲存，確定要離開嗎?」確定
        → 結帳 close → 「是否要開帳?」取消（保持 K:關帳由開頭冪等復原）
        → 「帳夾『1』有項目未結，請確認。」確定。
        tip: TipComponent（alert 按鈕 locator 在 tip_locator）。"""
        self.click(self.locator.btn_close_payment_dialog)
        self.sleep(0.5)
        tip.click_ok()
        self.sleep(0.5)
        self.click(self.locator.btn_close_checkout_dialog)
        self.sleep(0.5)
        tip.click_btn_by_text("取消")
        self.sleep(0.5)
        tip.click_ok()
        self.sleep(0.5)
        return self

    def click_save_payment(self):
        """點擊付款方式 save(r_w_pay_dt_1032)，付款存入結帳 dialog pay_tot，dialog 關，無 alert。"""
        self.click(self.locator.btn_save_payment)
        return self

    def click_checkout_dialog(self):
        """點擊結帳 dialog 內結帳(checkout)，觸發結帳。
        實測直接跳發票載具 dialog，跳過 Gherkin『是否要結帳?』alert。"""
        self.click(self.locator.btn_checkout_dialog)
        return self

    def click_invoice_confirm(self):
        """點擊發票載具確定(printInVoiceSave)，儲存後 alert『確認附屬程式已打開』。"""
        self.click(self.locator.btn_invoice_confirm)
        return self

    def close_print_bill_dialog(self):
        """關閉列印帳單 dialog（panel-tool-close=取消列印）。"""
        self.click(self.locator.btn_close_print_bill)
        return self

    def click_cancel_messagebox(self):
        """點擊 el-message-box 取消按鈕（退房確認按取消不退房；alert-ok 無 --cancel 支援）。"""
        self.click(self.locator.btn_cancel_messagebox)
        return self

    def click_confirm_messagebox(self):
        """點擊 el-message-box 確定按鈕（退房確認按確定=退房，狀態轉 Check Out）。"""
        self.click(self.locator.btn_confirm_messagebox)
        return self

    def get_messagebox_text(self):
        """讀 el-message-box 整段訊息（多 <p> 組成，text_tip 雙層 p 只抓首 p 抓不全）。"""
        return self.driver.find_element(*self.locator.text_messagebox).text

    # ----- 沖訂金(00) setup（#496 第 5 變體，獨立 test）-----
    # 00 沖訂金與前 4 變體流程結構不同：setup 建訂金 + 結帳 dialog 自動帶入 00
    # （前 4 變體綠色加號→手動 select；00 無綠色加號/save_payment，直接 checkout）

    # ----- 發票載具 dialog / 發票明細（#497）-----
    def input_invoice_ubn(self, ubn):
        """發票載具 dialog 填統一編號。"""
        self.input_with_clear(self.locator.input_invoice_ubn, ubn)
        return self

    def select_carrier_type(self, carrier_value):
        """選載具類別（原生 select，Selenium Select 類。選後統編 DISABLED）。
        carrier_value: 'CQ0001'(自然人憑證) / '3J0002'(手機條碼)。"""
        sel = Select(self.driver.find_element(*self.locator.select_carrier_type))
        sel.select_by_value(carrier_value)
        self.sleep(0.5)  # 等 Vue 更新（載具顯碼 enable）
        return self

    def input_carrier_id(self, carrier_id):
        """填載具顯碼（選載具類別後 enabled）。"""
        self.input_with_clear(self.locator.input_carrier_id, carrier_id)
        return self

    def select_donate_yes(self):
        """捐贈=是（click label，Element UI radio native 被 label 蓋）。"""
        self.click(self.locator.rb_donate_yes)
        return self

    def input_love_code(self, code):
        """填愛心碼（捐贈=是後 enabled）。"""
        self.input_with_clear(self.locator.input_love_code, code)
        return self

    def select_print_proof_yes(self):
        """列印證明聯=是（沒統編變體必需，否則擋 checkout）。"""
        self.click(self.locator.rb_print_proof_yes)
        return self

    def fill_invoice(self, invoice_type, data):
        """依變體填入發票載具（checkout 開 dialog 後、確定前；settle_account 呼叫）。
        invoice_type: 'none'(沒統編需列印證明聯) / 'ubn'(統編) / 'carrier'(載具) / 'love'(愛心碼)。
        data: test_data dict，含對應變體欄位（ubn/carrier_type/carrier_id/love_code）。"""
        if invoice_type == "none":
            self.select_print_proof_yes().sleep(0.3)
        elif invoice_type == "ubn":
            self.input_invoice_ubn(data["ubn"]).sleep(0.3)
        elif invoice_type == "carrier":
            self.select_carrier_type(data["carrier_type"]).sleep(0.5)
            self.input_carrier_id(data["carrier_id"]).sleep(0.3)
        elif invoice_type == "love":
            self.select_donate_yes().sleep(0.3)
            self.input_love_code(data["love_code"]).sleep(0.3)
        return self

    def select_latest_checkout_row(self):
        """選已結帳 grid 最新一筆結帳 row（click 最後序號 cell，序號遞增=最新結帳）。
        發票明細驗證前必呼叫，否則 uninvDetail 顯示 dialog 預設（可能舊發票）。
        結帳累積超過分頁大小（50 筆）時最新結帳在末頁，先跳最後頁再選（冪等）。"""
        self.click(self.locator.btn_checkedout_last_page)
        self.sleep(0.5)
        self.click(self.locator.cell_latest_checkout)
        return self

    def click_reinvoice(self):
        """點重開發票按鈕（已結帳 dialog，PMS03100311090）→ alert「是否確定要重開發票」。"""
        self.click(self.locator.btn_reinvoice)
        return self

    def get_checkout_invoice_no(self):
        """讀已結帳 grid 選中 row 的發票號碼（td textContent；重開前後比對新舊號）。"""
        return self.driver.find_element(*self.locator.text_checkout_invoice_no).text

    def get_checkout_pay_methods(self):
        """已結帳 dialog 下方 Table #32 的付款方式名稱值 list（#514 doSave 後驗證更改生效）。
        回傳代號前綴 list（如 ['10', '31']）；多筆付款時多值。"""
        elements = self.driver.find_elements(*self.locator.table_paymethod_value)
        return [e.text.split(":")[0].strip() for e in elements if e.text]

    def open_checkedout_dialog(self):
        """開已結帳 dialog（住客帳維護「已結帳總額」欄旁 [...]）。"""
        self.click(self.locator.btn_open_checkedout)
        return self

    def click_invoice_detail(self):
        """點發票明細按鈕（已結帳 dialog 內 uninvDetail），等第一張發票載入屬性區。"""
        self.click(self.locator.btn_invoice_detail)
        # 開窗後屬性區載入非同步；直接 get_invoice_detail 會搶在載入前讀到空/殘留值
        self.wait_invoice_detail_row_shown(0)
        return self

    def get_invoice_detail(self):
        """get 發票明細關鍵欄位，返回 dict（#497 Postconditions 驗證用）。"""
        fields = {
            "發票號碼": self.locator.text_inv_nos,
            "發票金額": self.locator.text_inv_amt,
            "統一編號": self.locator.text_inv_ubn,
            "是否捐贈": self.locator.text_inv_donate,
            "愛心碼": self.locator.text_inv_love,
            "載具類別": self.locator.text_inv_carrier_type,
            "載具顯碼": self.locator.text_inv_carrier_id1,
            "載具隱碼": self.locator.text_inv_carrier_id2,
        }
        return {
            name: (self.driver.find_element(*loc).get_attribute("value") or "")
            for name, loc in fields.items()
        }

    def close_invoice_detail(self):
        """關閉發票明細視窗。"""
        self.click(self.locator.btn_close_invoice_detail)
        return self

    def open_deposit_dialog(self):
        """點擊住客帳維護「訂金編號」欄旁 [...]（sub-button--more），開啟「訂金單筆新增」dialog。
        00 沖訂金 setup：帳戶需有訂金（餘額 > 0）結帳才自動帶入 00。"""
        self.click(self.locator.btn_open_deposit_dialog)
        return self

    def select_deposit_dt_pay_way(self, code):
        """選訂金付款方式（Element UI el-select，deposit_dt_pay_way td dfid）。
        code: '10' 現金（訂金本身的付款方式，非結帳付款方式）。
        el-select 需 JS click 開 dropdown + JS click option（同 select_payment_method 框架限制）。
        todo: 與 select_payment_method 的 el-select JS 可抽 _select_el_option helper（backlog debt）"""
        sel = self.driver.find_element(*self.locator.select_deposit_dt_pay_way)
        self.driver.execute_script("arguments[0].click()", sel)
        self.sleep(0.3)
        keyword = f"{code}:"
        self.driver.execute_script(
            """
            var kw = arguments[0];
            var dds = document.querySelectorAll('.el-select-dropdown');
            for (var d = dds.length - 1; d >= 0; d--) {
                var dd = dds[d];
                if (dd.style.display === 'none' || dd.offsetHeight === 0) continue;
                var items = dd.querySelectorAll('li.el-select-dropdown__item');
                for (var i = 0; i < items.length; i++) {
                    var t = items[i].textContent.replace(/\\s/g, '');
                    if (t.indexOf(kw) >= 0) { items[i].click(); return; }
                }
            }
        """,
            keyword,
        )
        return self

    def input_deposit_dt_use_amt(self, amount):
        """輸入訂金使用金額（Syncfusion numeric td dfid）。"""
        self.input_with_clear(self.locator.input_deposit_dt_use_amt, str(amount))
        return self

    def save_deposit(self):
        """點擊訂金單筆新增 dialog save（訂金存入帳戶）。save 後「儲存成功」alert。"""
        self.click(self.locator.btn_save_deposit)
        return self

    def get_pay_way(self):
        """讀結帳 dialog 付款方式 td text（00 沖訂金時自動帶入「00:沖訂金」）。
        與 select_pay_way 不同：手動選時用 el-select input value；自動帶入時讀 td text。"""
        return self.driver.find_element(*self.locator.text_pay_way).text

    # ----- 分發票 / 多張發票（#731）-----

    def click_invoice(self):
        """點擊分發票按鈕（直接開設定 dialog，無 alert；Gherkin『是否要結帳』不準）。"""
        self.click(self.locator.btn_invoice)
        return self

    def input_uniinv_count(self, value):
        """設定 dialog 發票張數（Syncfusion numeric，type 有效）。"""
        self.input_with_clear(self.locator.input_uniinv_count, str(value))
        return self

    def check_is_divided_equally(self):
        """勾選金額均分 checkbox（狀態型：已勾則不重覆 click）。"""
        label = self.driver.find_element(*self.locator.cb_is_divided_equally)
        if "is-checked" not in (label.get_attribute("class") or ""):
            self.click(self.locator.cb_is_divided_equally)
        return self

    def click_check_invoice_num(self):
        """設定 dialog 儲存（開分發票 dialog，grid row = 張數）。"""
        self.click(self.locator.btn_checkInvoiceNum)
        return self

    def select_invoice_copy(self, num):
        """click 分發票 dialog 左欄張號選張（右側載入該張屬性+明細）。num=張號 1/2/3...
        選張後明細 grid 非同步刷新，sleep 等載入完成（連跑 session 累積時尤需）。"""
        self.click(self.format_locator(self.locator.cell_invoice_num, str(num)))
        self.sleep(0.8)
        return self

    def input_unit_price(self, value):
        """明細單價改值 + Enter 觸發 cell endEdit → price 連動重算、左欄 invoice_amount 更新。
        price 是 unit_price × count 的 computed readonly，改 unit_price 連動 price。"""
        self.click(self.locator.cell_unit_price)
        self.sleep(0.3)
        el = self.driver.find_element(*self.locator.input_unit_price)
        el.send_keys(Keys.CONTROL, "a")
        el.send_keys(str(value))
        el.send_keys(Keys.ENTER)
        return self

    def fill_split_invoice(self, invoice_type, data):
        """分發票 dialog 逐張屬性填入（結構同 #497 發票載具 dialog；per 張獨立可不同）。
        invoice_type: none/ubn/carrier/love。"""
        if invoice_type == "none":
            self.click(self.locator.rb_split_print_proof_yes)
        elif invoice_type == "ubn":
            self.input_with_clear(self.locator.input_split_ubn, data["ubn"])
        elif invoice_type == "carrier":
            Select(
                self.driver.find_element(*self.locator.select_split_carrier_type)
            ).select_by_value(data["carrier_type"])
            self.input_with_clear(self.locator.input_split_carrier_id, data["carrier_id"])
        elif invoice_type == "love":
            self.click(self.locator.rb_split_donate_yes)
            self.input_with_clear(self.locator.input_split_love_code, data["love_code"])
        return self

    def click_save_invoice_split(self):
        """分發票 dialog 儲存（r_1050 panel-title scope 避三度衝突）。
        儲存後「確認附屬程式已打開 並 重整網頁」alert（Gherkin『是否列印帳單』不準）。"""
        self.click(self.locator.btn_save_invoice_split)
        return self

    def select_invoice_detail_row(self, idx):
        """click 發票明細視窗品明細 grid 某行（選該張發票，上方單張屬性刷新）。idx=0..N-1。"""
        self.click(self.format_locator(self.locator.cell_invoice_detail_row, str(idx)))
        self.wait_invoice_detail_row_shown(idx)
        return self

    def wait_invoice_detail_row_shown(self, idx, timeout=10):
        """等品明細第 idx 列的發票號碼反映到上方屬性區（選列/開窗後屬性刷新皆非同步）。

        就緒訊號 = 屬性區值 == grid 列值（兩個 runtime 視圖一致），非期望值——
        歷史殘留值（非空但非本列）會被攔住，不會假穩定放行。輪詢每輤重新
        find_element，屬性區重繪中的 StaleElement 下一輪自然穿過。
        """
        row_locator = self.format_locator(self.locator.cell_invoice_detail_row, str(idx))

        def _row_shown(_driver):
            row_nos = self._safe_grid_text(row_locator)
            return row_nos != "" and self._safe_input_value(self.locator.text_inv_nos) == row_nos

        WebDriverWait(self.driver, timeout).until(_row_shown)
        return self

    def _safe_grid_text(self, locator):
        # grid 儲存格值在 DOM text；元素未渲染/重繪期回空字串讓 wait 條件下一輪重試
        try:
            return (self.driver.find_element(*locator).text or "").strip()
        except (NoSuchElementException, StaleElementReferenceException):
            return ""

    def _safe_input_value(self, locator):
        # 屬性區 DISABLED input 值在 value 屬性（非 DOM text）
        try:
            return (self.driver.find_element(*locator).get_attribute("value") or "").strip()
        except (NoSuchElementException, StaleElementReferenceException):
            return ""
