from tools.random_helper import RandomHelper


class ShareSteps:

    @staticmethod
    def open_shift(web, hall_type, shift, pw):  # 開班
        web.share_panel_component.select_by_label("廳別", hall_type)
        web.share_panel_component.input_by_label("班別", shift)
        web.share_panel_component.input_by_label("密碼", pw)
        web.share_panel_component.click_panel_footer_btn("開班", "確認")
        web.tip_component.click_ok().sleep(2)

    @staticmethod
    def to_reservation_detail(web, menu, func_name, search_cond, search_value, toolbar):
        # 訂房卡頁面 > 訂房明細
        web.header_component.expand_menu(menu).sleep(1)
        web.header_component.to_func_page(func_name).sleep(1)
        web.reservation_card_dialog.search_reservation_card(search_cond, search_value).sleep(1)
        web.reservation_card_dialog.click_edit_reservation_card().sleep(2)
        web.reservation_card_dialog.click_card_toolbar(toolbar).sleep(1)

    @staticmethod
    def create_or_enter_reservation_detail(
        web,
        search_cond,
        search_value,
        toolbar,
        first_name=None,
        last_name=None,
        rate_cod_name=None,
        room_type=None,
    ):
        # 訂房卡頁面查詢 > 無訂房卡則建立訂房卡並進入明細 or 有訂房卡直接進入訂房明細
        web.header_component.expand_menu("訂房").sleep(1)
        web.header_component.to_func_page("訂房卡").sleep(1)

        web.reservation_card_dialog.search_reservation_card(search_cond, search_value).sleep(1)
        if web.reservation_card_dialog.has_reservation_card():
            web.reservation_card_dialog.click_edit_reservation_card().sleep(2)
        else:
            web.reservation_card_dialog.click_btn_add().sleep(1)
            web.reservation_page.click_edit_guest().sleep(3)
            web.reservation_page.create_guest(
                first_name, last_name, "Miss.", RandomHelper.generate_phone_mobile()
            )
            web.tip_component.click_ok().sleep(1)
            web.reservation_card_dialog.click_edit_rate_cod()
            web.reservation_card_dialog.set_rate_code(rate_cod_name, room_type).sleep(1)
            web.reservation_page.save_card()
            web.tip_component.click_ok().sleep(2)

        web.reservation_card_dialog.click_card_toolbar(toolbar).sleep(3)

    @staticmethod
    def verify_save_success_tip(web, message=None):  # 顯示'儲存成功'提示
        if message:
            web.athena_base_page.screenshot(f"Then 顯示'{message}'提示")
            web.athena_base_page.assert_data(message, web.tip_component.get_tip_text(), message)
        else:
            web.athena_base_page.screenshot("Then 顯示'儲存成功'提示")
            web.athena_base_page.assert_data(
                "儲存成功", web.tip_component.get_tip_text(), "儲存成功"
            )
        web.tip_component.click_ok()

    @staticmethod
    def click_btn_save(web, save_method=None):  # 點擊[橘色磁碟片]進行儲存
        if save_method:
            save_method()
        else:
            web.athena_base_page.click_toolbar_with_icon("save").sleep(1)
        web.athena_base_page.screenshot("And 點擊儲存")

    @staticmethod
    def check_out_guest(web, pay_code="10"):
        # 住客退房（含現金結帳）：復原 → 結帳 → 退房確定 → Check Out（C:結帳/退房完成）。
        # restore 組（#486/#509/#512/#514）setup 用。前提：住客帳維護 dialog 已開。
        # 復原：確保 O:開帳（K 關帳則 toggle + 兩 alert：是否開帳 / 開帳成功）
        if not web.co_list_page.is_account_open():
            web.co_list_page.click_toggle_account().sleep(1)
            web.base_page.wait_visible(web.tip_component.locator.btn_alert_ok)
            web.tip_component.click_ok().sleep(1)
            web.base_page.wait_visible(web.tip_component.locator.btn_alert_ok)
            web.tip_component.click_ok().sleep(1)
        # 復原：確保 folio 有帳務（結帳清空則入帳一筆作結帳標的）
        if web.co_list_page.get_folio_tab_amount("1") == 0:
            web.co_list_page.enter_consumption("1001 : 房租", "1").sleep(1)
        # 結帳（發票走 none：沒統編需列印證明聯）+ 退房確定（轉 Check Out）
        ShareSteps.settle_account(web, pay_code, "none")
        web.base_page.wait_visible(web.co_list_page.locator.btn_cancel_messagebox)
        web.co_list_page.click_confirm_messagebox().sleep(1)
        # 退房完成系統 alert（按確定退房後出現，alertOK 關；#486 Phase 2 驗證）
        web.base_page.wait_visible(web.tip_component.locator.btn_alert_ok)
        web.tip_component.click_ok().sleep(1)

    @staticmethod
    def ensure_account_open(web):
        # 確保住客帳開帳（K:關帳則開帳）。前提：住客帳維護 dialog 已開（帳戶狀態 combobox 在 dialog 內）。
        # 開帳 = toggle + 兩次 alertOK（是否要開帳? → 開帳成功）。
        if not web.co_list_page.is_account_open():
            web.co_list_page.click_toggle_account().sleep(1)
            web.base_page.wait_visible(web.tip_component.locator.btn_alert_ok)
            web.tip_component.click_ok().sleep(1)
            web.base_page.wait_visible(web.tip_component.locator.btn_alert_ok)
            web.tip_component.click_ok().sleep(1)

    @staticmethod
    def ensure_cash_room_cleared(web, room):
        """#459 開頭冪等：住客帳維護列表搜尋 room，殘留（上次未清）則結帳退房釋放 C 號回 combobox。
        C 號數量有限，建立即永久消耗；結帳退房才釋放（domain 校正：刪除≠結帳退房）。"""
        web.guest_account_page.search_room(room).sleep(0.5)
        if web.guest_account_page.has_cash_room_in_list(room):
            web.guest_account_page.click_card_row(room).sleep(0.5)
            web.guest_account_page.click_guest_maintain().sleep(1)
            # 未開班先跳開班 dialog（ensure 在 test 開頭，PMS session 可能未開班）
            if web.guest_account_page.has_element(web.guest_account_page.locator.dialog_shift):
                ShareSteps.open_shift(web, "FO : 飯店櫃檯", "a", "autotest")
                web.guest_account_page.sleep(1)
            # 等單筆 dialog 開（btn_checkout render）— dialog 非同步載入
            web.base_page.wait_visible(web.guest_account_page.locator.btn_checkout)
            # 空帳結帳（無付款流程）：結帳 → 是否退房確定 → 退房完成確定
            web.guest_account_page.click_checkout().sleep(1)
            web.base_page.wait_visible(web.tip_component.locator.btn_alert_ok)
            web.tip_component.click_ok().sleep(1)
            web.base_page.wait_visible(web.tip_component.locator.btn_alert_ok)
            web.tip_component.click_ok().sleep(1)
            web.guest_account_page.close_single_dialog().sleep(1)

    @staticmethod
    def ensure_checkedout_inhouse(web, room, pay_code="10"):
        # 確保卡 In house + 已結帳（K:關帳，當班結帳記錄，未退房）。#515 重開發票 setup 用。
        # 對照 ensure_checkout_state，但結帳不退房（settle_account + 取消退房 messagebox）。
        # 偵測 is_account_open：O 未結帳 → 入帳(若空)+結帳+取消退房；K 已結帳 → 跳過（冪等）。
        web.co_list_page.click_inhouse_tab().sleep(1)
        web.co_list_page.search_by_room_no(room).sleep(1)
        web.co_list_page.click_card_row(room).sleep(1)
        web.co_list_page.click_open_guest_account().sleep(1)
        if web.co_list_page.has_element(web.co_list_page.locator.dialog_shift):
            ShareSteps.open_shift(web, "FO : 飯店櫃檯", "a", "autotest")
            web.co_list_page.sleep(1)
        if web.co_list_page.is_account_open():
            if web.co_list_page.get_folio_tab_amount("1") == 0:
                web.co_list_page.enter_consumption("1001 : 房租", "1").sleep(1)
            ShareSteps.settle_account(web, pay_code, "none")
            web.base_page.wait_visible(web.co_list_page.locator.btn_cancel_messagebox)
            web.co_list_page.click_cancel_messagebox().sleep(1)

    @staticmethod
    def ensure_checkout_state(web, card_name, room, pay_code="10"):
        # 確保卡在 Check Out tab 並選取（restore 組 #509/#512/#514 冪等 setup）。
        # 已 CO 直接用；IH 則 check_out_guest 推 CO（產生當班結帳記錄 + 付款方式）。
        # 前提：已導航 C/O 清單。解決方案 A 每案獨立 setup 的起點冪等（前案終態 CO/IH 皆可）。
        web.co_list_page.click_checkout_tab().sleep(1)
        if web.co_list_page.has_card_row(room):
            web.co_list_page.click_card_row(room).sleep(1)
            return
        # In house，推到 CO
        web.co_list_page.click_inhouse_tab().sleep(1)
        web.co_list_page.search_by_guest_name(card_name).sleep(1)
        web.co_list_page.click_card_row(room).sleep(1)
        web.co_list_page.click_open_guest_account().sleep(1)
        if web.co_list_page.has_element(web.co_list_page.locator.dialog_shift):
            ShareSteps.open_shift(web, "FO : 飯店櫃檯", "a", "autotest")
            web.co_list_page.sleep(1)
        ShareSteps.check_out_guest(web, pay_code)
        web.co_list_page.close_guest_account_dialog().sleep(1)
        web.co_list_page.click_checkout_tab().sleep(1)
        web.co_list_page.click_card_row(room).sleep(1)

    @staticmethod
    def ensure_folio_clean(web, folio="1"):
        # 冪等清帳：註銷指定 folio 的未結帳消費（累積制卡 setup——每輪起點恆乾淨，
        # 消費 grid 的順序/分頁假設（新筆插頭部、>50 筆分頁）恢復有效）。
        # 註銷 = 列直接消失、folio 金額同步回落（詳 co_list.md 註銷段）。
        # ⚠️ 訊銷 dialog 顯示「當前選中 folio tab」的消費（非全部 folio），
        # 開頭判斷的 get_folio_consumable_acct_nos 已 switch 到目標 folio（讀取即切 tab）。
        # ⚠️ 僅剩訂金（dd:）或無正消費時，開訊銷只跳 alert「找不到可以註銷資料」且
        # dialog 停留 hidden（close/checkbox 全不可互動）——故開頭先判斷：
        # 無正消費直接 return，不點訊銷按鈕。
        # ⚠️ 已結帳記錄屬歷史清不到（invoice 族分頁另以 pagination-last 處理）；
        # 未結帳的跨班歷史可註銷，但轉帳轉入的帳不可訊銷（攔到 alert 即視為已乾淨）。
        # 前提：住客帳維護 dialog 已開。
        page = web.co_list_page
        for _ in range(2):
            # 完成判據兼前置判斷（排除訂金 dd:）：無正消費 = 已乾淨（或僅剩不可清項）
            if not web.co_list_page.get_folio_consumable_acct_nos(folio):
                return
            page.click(page.locator.btn_open_void)
            web.base_page.wait_present(page.locator.btn_void_save)
            # 防禦：grid 顯示有帳但 dialog 跳「找不到可以註銷資料」alert（轉入帳等
            # server 端不可清項）——alert 蓋住 dialog 攔 click 且 dialog 停留 hidden，
            # soft-wait 出現即關、視為無可清。alertOK 是 DOM 常駐隱藏容器（display:none），
            # has_element 恆 True——判準用 is_displayed
            deadline = time.monotonic() + 5
            while time.monotonic() < deadline:
                alerts = web.driver.find_elements(*web.tip_component.locator.btn_alert_ok)
                if alerts and alerts[0].is_displayed():
                    web.tip_component.click_ok().sleep(0.5)
                    return
                time.sleep(0.2)
            checkboxes = [
                c
                for c in page.driver.find_elements(*page.locator.checkbox_void_item)
                if not c.is_selected()
            ]
            if checkboxes:
                for checkbox in checkboxes:
                    checkbox.click()
                    # 勾選間隔給 EasyUI 勾選事件處理——毫秒連發時勾選 DOM 有套但
                    # EasyUI 內部 checked state 沒記，儲存送出空清單（成功但沒清）
                    page.sleep(0.2)
                page.click(page.locator.btn_void_save)
                page.sleep(1)
                web.base_page.wait_visible(web.tip_component.locator.btn_alert_ok)
                web.tip_component.click_ok().sleep(1)
            # folio tab 不即時刷新——關閉註銷 dialog 後筆數與金額才同步
            page.click(page.locator.btn_close_void)
            page.sleep(1)

    @staticmethod
    def open_contract_tab(web, company_cod):  # 商務公司→搜尋→維護視窗→合約頁籤
        web.header_component.expand_menu("業務").sleep(1)
        web.header_component.to_func_page("商務公司").sleep(2)
        web.business_company_page.search_company(company_cod).sleep(2)
        web.business_company_page.click_target_company(company_cod).sleep(1)
        web.business_company_page.open_maintain_panel().sleep(2)
        web.share_panel_component.click_detail_tab("contract").sleep(1)

    @staticmethod
    def restore_room_to_inhouse(web, room):
        """退房還原：C/O 清單 Check Out tab 指定房回 In house（#501 復原子房用）。
        前提：已導航 C/O 清單。房號在 Check Out tab 才還原（不在則跳過，冪等）。
        團體子房退房後落在 Check Out tab；還原後回團體管理已入住 tab（非 C/O 清單 In house tab）。"""
        web.co_list_page.click_checkout_tab().sleep(1)
        web.co_list_page.search_by_room_no(room).sleep(1)
        if web.co_list_page.has_card_row(room):
            web.co_list_page.click_card_row(room).sleep(1)
            web.co_list_page.click_restore_checkout().sleep(1)
            web.base_page.wait_visible(web.tip_component.locator.btn_alert_ok)
            web.tip_component.click_ok().sleep(1)
            web.base_page.wait_visible(web.tip_component.locator.btn_alert_ok)
            web.tip_component.click_ok().sleep(1)

    @staticmethod
    def settle_account(web, pay_code="10", invoice_type=None, invoice_data=None):
        # 結帳框架（關帳 → 現金付款 → checkout → [發票載具填入] → 發票確定 → 列印帳單關閉）
        # 不含退房確認（確定/取消 + 是否退房斷言）——是各 test 的斷言點，留呼叫者。
        # invoice_type/invoice_data: 發票載具變體（'none'/'ubn'/'carrier'/'love' + 對應 data 欄位），
        #    None=不填；沒統編場景傳 'none'（fill_invoice 會 select_print_proof_yes 否則擋 checkout）。
        # 付款固定單筆現金；#496 多筆變體/00 沖訂金自動帶入的付款邏輯是 test 核心，不走此 helper。
        # 關帳（工具列結帳 → 連續兩 alert：是否關帳 / 關帳成功）
        web.co_list_page.click_checkout_toolbar().sleep(1)
        web.base_page.wait_visible(web.tip_component.locator.btn_alert_ok)
        web.tip_component.click_ok().sleep(1)
        web.base_page.wait_visible(web.tip_component.locator.btn_alert_ok)
        web.tip_component.click_ok().sleep(1)
        # 付款（綠色加號 + 現金 + save）
        web.co_list_page.click_add_payment().sleep(0.5)
        web.co_list_page.select_payment_method(pay_code).sleep(0.5)
        web.co_list_page.click_save_payment().sleep(0.5)
        # checkout（開發票載具 dialog）→ 依變體填入
        web.co_list_page.click_checkout_dialog().sleep(1)
        if invoice_type:
            web.co_list_page.fill_invoice(invoice_type, invoice_data)
        # 發票確定 → 附屬程式 alert → 列印帳單關閉（=取消列印）
        web.co_list_page.click_invoice_confirm().sleep(1)
        web.base_page.wait_visible(web.tip_component.locator.btn_alert_ok)
        web.tip_component.click_ok().sleep(1)
        web.co_list_page.close_print_bill_dialog().sleep(1)
