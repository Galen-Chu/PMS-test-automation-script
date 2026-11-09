from selenium.webdriver.common.by import By
from locators.base_locator import BaseLocator


class CoListLocator(BaseLocator):

    # ----- 搜尋區 -----
    # btn_search 重用 BaseLocator（PMS0310020_doSearch 含 _doSearch 後綴）
    input_guest_name = (By.XPATH, "//div[@data-field-id='guest_mn.alt_nam']//input")
    # 房號搜尋欄（轉帳驗證用：目標帳戶與來源不同姓名，改用房號定位）
    input_room_nos = (By.XPATH, "//div[@data-field-id='guest_mn.room_nos']//input")

    # ----- Grid（C/O 清單主頁，需先搜尋確保房號唯一）-----
    cell_room_nos = (By.XPATH, "//td[@field='room_nos' and normalize-space()='%s']")
    # Check Out 頁籤（C/O 清單主 tab，退房後記錄；#486 Then 切換驗證退房資料顯示）
    tab_checkout = (By.XPATH, "//div[@id='tab-checkedOut_Tab']")
    # In House 頁籤（#509 退房還原後驗證回 In house）
    tab_inhouse = (By.XPATH, "//div[@id='tab-inHouse_Tab']")
    # Check Out tab 退房還原按鈕（text 定位避 r_1040 與住客帳維護入帳衝突；co_list:L143；#509 When）
    btn_restore_checkout = (By.XPATH, "//button[normalize-space()='退房還原']")
    # Check Out tab 已結帳按鈕（開已結帳 dialog PMS0310031；text 定位避 r_1050 衝突；#512 入口 A）
    btn_checkedout_toolbar = (By.XPATH, "//button[normalize-space()='已結帳']")
    # 已結帳 dialog 結帳還原（撤銷當筆結帳記錄；co_list:L703；#512 When）
    btn_cancel_checkout_record = (By.XPATH, "//button[@data-field-id='r_PMS0310031_1010']")
    # 已結帳 dialog 關閉（panel-title 已結帳 scope；#512 結帳還原後切 tab 前需關）
    btn_close_checkedout_dialog = (
        By.XPATH,
        "//div[contains(@class,'panel-title') and normalize-space()='已結帳']"
        "/parent::div//a[contains(@class,'panel-tool-close')]",
    )
    # 已結帳 dialog 更改付款方式（開更改付款方式 dialog PMS0310012；co_list:L707；#514 When）
    btn_edit_payment = (By.XPATH, "//button[@data-field-id='editPayMent']")
    # 更改付款方式 dialog 清除付款（co_list:L750；#514 清除原付款，綠色加號才出現）
    btn_clear_payment = (By.XPATH, "//button[@data-field-id='clearPayMent']")
    # 更改付款方式 dialog 橘色磁碟片儲存（co_list:L751；#514 doSave）
    btn_do_save = (By.XPATH, "//button[@data-field-id='doSave']")

    # ----- 住客帳維護入口 -----
    btn_open_guest_account = (By.XPATH, "//button[@data-field-id='co_Button']")
    # 開班 dialog 偵測：未開班時 click 住客帳維護自動彈開班 dialog（session 級，已開班則不彈）
    dialog_shift = (By.XPATH, "//div[@data-field-id='rspt_cod']//input")
    # 住客帳維護單筆 dialog 關閉（panel-title ancestor scope：多 dialog 時避免打到 hidden close）
    btn_close_guest_account = (
        By.XPATH,
        "//div[contains(@class,'panel-title') and normalize-space()='住客帳維護單筆']"
        "/ancestor::div[contains(@class,'panel')]//a[contains(@class,'panel-tool-close')]",
    )

    # ----- 入帳 panel（轉帳前置：建立可轉消費）-----
    btn_open_entry = (By.XPATH, "//button[normalize-space()='入帳']")
    # ----- 註銷（r_1060 開 dialog；累積制卡冪等清帳用；co_list.md 註銷段 2026-08-25 實測）-----
    btn_open_void = (By.XPATH, "//button[@data-field-id='r_1060']")
    # 註銷 dialog grid 的消費勾選 checkbox（顯示全部 folio 消費，非當前 tab）。
    # 排除 header 全選框（datagrid-header-check）——td[field=ck] 在 header 也存在，
    # 無帳時 data row 0 筆仍會誤抓全選框（8/26 transfer 炸點佐證）
    checkbox_void_item = (
        By.XPATH,
        "//div[contains(@class,'panel-title') and normalize-space()='註銷']"
        "/ancestor::div[contains(@class,'panel')]//td[@field='ck']"
        "[not(.//div[contains(@class,'datagrid-header-check')])]//input",
    )
    # 註銷 dialog 儲存（text 定位；dialog 內按鈕非工具列 save icon）
    btn_void_save = (
        By.XPATH,
        "//div[contains(@class,'panel-title') and normalize-space()='註銷']"
        "/ancestor::div[contains(@class,'panel')]//button[normalize-space()='儲存']",
    )
    # 註銷 dialog 關閉（folio tab 不即時刷新，關閉後筆數與金額才同步）
    btn_close_void = (
        By.XPATH,
        "//div[contains(@class,'panel-title') and normalize-space()='註銷']"
        "/ancestor::div[contains(@class,'panel')]//a[contains(@class,'panel-tool-close')]",
    )
    input_entry_item = (
        By.XPATH,
        "//div[@class='panel-title' and text()='入帳']/parent::div/following-sibling::div"
        "//div[contains(@class,'el-select')]//input",
    )
    input_entry_folio = (
        By.XPATH,
        "//div[@class='panel-title' and text()='入帳']/parent::div/following-sibling::div"
        "//input[@placeholder='請選擇']",
    )
    btn_entry_save = (
        By.XPATH,
        "//div[@class='panel-title' and text()='入帳']/parent::div/following-sibling::div//img[@alt='save']",
    )
    # 入帳 panel 不關會遮擋工具列轉帳鈕（click intercepted），save 後必須關
    btn_close_entry_panel = (
        By.XPATH,
        "//div[contains(@class,'panel-title') and normalize-space()='入帳']"
        "/parent::div//a[contains(@class,'panel-tool-close')]",
    )

    # ----- 轉帳 -----
    # 工具列轉帳鈕（text 定位：r_1050 與 Check Out tab「已結帳」同 id 衝突）
    btn_open_transfer_item = (By.XPATH, "//button[normalize-space()='轉帳']")
    # 轉帳項目選擇帳夾 dropdown（多 folio 帳戶需手動選才載入 grid；單 folio 如 PM房預設帶入）
    input_transfer_item_folio = (
        By.XPATH,
        "//div[contains(@class,'panel-title') and normalize-space()='轉帳項目選擇']"
        "/ancestor::div[contains(@class,'panel')]//input[@placeholder='請選擇']",
    )
    checkbox_transfer_item = (By.XPATH, "//input[@name='ck']")
    # 轉帳項目選擇 dialog 內轉帳鈕（not @data-field-id 排除工具列的 r_1050）
    btn_open_transfer_folio = (
        By.XPATH,
        "//button[normalize-space()='轉帳' and not(@data-field-id)]",
    )
    # 轉帳對象 radio：相同訂房卡 / 全部房號 / 選擇房號（三選一，%s = label 關鍵字）
    label_transfer_target_type = (
        By.XPATH,
        "//div[@data-field-id='choose']//label[contains(.,'%s')]",
    )
    # 選擇房號 radio 時的房號過濾 input（type 即時過濾 grid，不需 Enter）
    input_transfer_room_filter = (
        By.XPATH,
        "//div[contains(@class,'panel-title') and normalize-space()='轉帳帳夾選擇']"
        "/ancestor::div[contains(@class,'panel')]//input[@name='room_nos']",
    )
    # 上層 grid 目標房：panel-title ancestor scope 限縮（值 scope match=3 hidden=1，2026-07-24 實測）
    cell_transfer_target_room = (
        By.XPATH,
        "//div[contains(@class,'panel-title') and normalize-space()='轉帳帳夾選擇']"
        "/ancestor::div[contains(@class,'panel')]//td[@field='room_nos' and normalize-space()='%s']",
    )
    # 下層 grid folio：datagrid-view2 (regular) scope 限縮（frozen+regular 同欄位 match=2）
    cell_transfer_target_folio = (
        By.XPATH,
        "//div[contains(@class,'panel-title') and normalize-space()='轉帳帳夾選擇']"
        "/ancestor::div[contains(@class,'panel')]//div[contains(@class,'datagrid-view2')]"
        "//td[@field='folio_nam' and normalize-space()='%s']",
    )
    # 轉帳確認鈕：panel scope 比 [last()] 穩（兩 dialog 嵌套時 match=2）
    btn_confirm_transfer = (
        By.XPATH,
        "//div[contains(@class,'panel-title') and normalize-space()='轉帳帳夾選擇']"
        "/ancestor::div[contains(@class,'panel')]//button[normalize-space()='轉帳' and not(@data-field-id)]",
    )
    # 轉帳項目選擇 dialog 轉帳後不自動關閉，folio tab 不刷新，需手動關
    btn_close_transfer_item_dialog = (
        By.XPATH,
        "//div[contains(@class,'panel-title') and normalize-space()='轉帳項目選擇']"
        "/parent::div//a[contains(@class,'panel-tool-close')]",
    )

    # ----- folio tab（Postcondition assert 來源 folio 清空 / 金額守恆 / folio 切換）-----
    text_folio_tab = (By.XPATH, "//div[@id='tab-%s']")

    # ----- acct_nos 驗證（acct_nos diff：唯一流水號精確追蹤消費移動）-----
    # 住客帳維護消費款項 Grid 的 acct_nos 隱藏欄（display:none，.text 回空須用 textContent）。
    # scope：住客帳維護單筆 panel + datagrid-view2 data row，排除 header 與其他 grid。
    # grid 只顯示當前 folio tab 消費，讀取前須 switch_folio_tab 切到目標 folio。
    cell_acct_nos = (
        By.XPATH,
        "//div[contains(@class,'panel-title') and normalize-space()='住客帳維護單筆']"
        "/ancestor::div[contains(@class,'panel')]//div[contains(@class,'datagrid-view2')]"
        "//tr[contains(@class,'datagrid-row')]/td[@field='acct_nos']",
    )
    # 消費 grid pager 按鈕（累積制卡消費 >50 筆時分頁，get_folio_acct_nos 逐頁收集
    # 全部頁——diff 用途須全量，單頁讀取會漏新筆；點擊冪等——已在目標頁時無反應）
    btn_folio_grid_first_page = (
        By.XPATH,
        "//div[contains(@class,'panel-title') and normalize-space()='住客帳維護單筆']"
        "/ancestor::div[contains(@class,'panel')]//*[contains(@class,'pagination-first')]",
    )
    btn_folio_grid_next_page = (
        By.XPATH,
        "//div[contains(@class,'panel-title') and normalize-space()='住客帳維護單筆']"
        "/ancestor::div[contains(@class,'panel')]//*[contains(@class,'pagination-next')]",
    )
    # 消費 grid pager 資訊文字（「Displaying X to Y of Z items」，末頁判斷 Y==Z 用）
    text_folio_grid_pager = (
        By.XPATH,
        "//div[contains(@class,'panel-title') and normalize-space()='住客帳維護單筆']"
        "/ancestor::div[contains(@class,'panel')]//*[contains(@class,'pagination-info')]",
    )
    btn_folio_grid_last_page = (
        By.XPATH,
        "//div[contains(@class,'panel-title') and normalize-space()='住客帳維護單筆']"
        "/ancestor::div[contains(@class,'panel')]//*[contains(@class,'pagination-last')]",
    )
    # folio 消費款項 Grid 的 data row（tr）：對帳用，row 內配對 acct_nos(hidden)+item_nam(visible)。
    # 排除 header row——class=datagrid-header-row 含 'datagrid-row' 子串，其 td 值是
    # 表頭文字（服務名稱/消費編號），混入會污染 row 內配對讀值
    row_folio_consume = (
        By.XPATH,
        "//div[contains(@class,'panel-title') and normalize-space()='住客帳維護單筆']"
        "/ancestor::div[contains(@class,'panel')]//div[contains(@class,'datagrid-view2')]"
        "//tr[contains(@class,'datagrid-row') and not(contains(@class,'datagrid-header-row'))]",
    )
    # row_folio_consume 內的相對定位（find_element 傳入 row element 後用）
    cell_item_nam_in_row = (By.XPATH, ".//td[@field='item_nam']")
    cell_acct_nos_in_row = (By.XPATH, ".//td[@field='acct_nos']")
    cell_item_tot_in_row = (By.XPATH, ".//td[@field='item_tot']")

    # ----- 預估款維護 grid（#464 對帳：當天帳務 item_nos）-----
    row_estimate = (
        By.XPATH,
        "//div[contains(@class,'panel-title') and normalize-space()='預估款維護']"
        "/ancestor::div[contains(@class,'panel')]//div[contains(@class,'datagrid-view2')]"
        "//tr[contains(@class,'datagrid-row') and not(contains(@class,'datagrid-header-row'))]",
    )
    # row_estimate 內的相對定位
    cell_acct_dat_in_row = (By.XPATH, ".//td[@field='acct_dat']")
    cell_item_nos_in_row = (By.XPATH, ".//td[@field='item_nos']")

    # ----- 指定訂金（#488）-----
    # 指定訂金 dialog：deposit_nos 是 EasyUI combogrid（非 combobox），dps_folio_nos 是 combobox
    btn_open_assign_deposit = (By.XPATH, "//button[@data-field-id='r_1130']")
    # combogrid 下拉箭頭（click input 不開 dropdown，要 click combo-arrow）
    btn_deposit_combo_arrow = (
        By.XPATH,
        "//div[@data-field-id='deposit_nos']//a[contains(@class,'combo-arrow')]",
    )
    # combogrid dropdown 為 floating panel（combo-p），限縮 visible 避免打到 hidden 預建 panel
    cell_deposit_option = (
        By.XPATH,
        "//div[contains(@class,'combo-p') and not(contains(@style,'display: none'))]"
        "//td[@field='alt_nam' and normalize-space()='%s']",
    )
    # textbox-text：顯示值（清空用，combogrid not interactable 需 execute_script）
    input_deposit_nos_text = (
        By.XPATH,
        "//div[@data-field-id='deposit_nos']//input[contains(@class,'textbox-text')]",
    )
    # textbox-value：hidden 真值（偵測已綁用）
    input_deposit_nos_value = (
        By.XPATH,
        "//div[@data-field-id='deposit_nos']//input[contains(@class,'textbox-value')]",
    )
    # 使用訂金的帳夾 combobox（placeholder='請選擇'）
    input_dps_folio_nos = (
        By.XPATH,
        "//div[@data-field-id='dps_folio_nos']//input[@placeholder='請選擇']",
    )
    btn_save_assign_deposit = (
        By.XPATH,
        "//div[contains(@class,'panel-title') and normalize-space()='指定訂金']"
        "/ancestor::div[contains(@class,'panel')]//button[child::img[@alt='save']]",
    )
    btn_close_assign_deposit = (
        By.XPATH,
        "//div[contains(@class,'panel-title') and normalize-space()='指定訂金']"
        "/ancestor::div[contains(@class,'panel')]//a[contains(@class,'panel-tool-close')]",
    )

    # ----- 單筆拆帳（#555）-----
    # 選最後一筆消費（剛入帳的新消費 acct_nos 最大排末尾，排序已驗證）。多筆同名取 [last()]
    cell_consumption_last = (
        By.XPATH,
        "(//td[@field='item_nam' and normalize-space()='%s'])[last()]",
    )
    btn_split = (By.XPATH, "//button[@data-field-id='split']")
    # Syncfusion DDL：操作 target 是 span 非 input（input readonly，click 被 BLOCKED）
    span_split_rule = (
        By.XPATH,
        "//div[@data-field-id='splitRule']//span[contains(@class,'e-input-group')]",
    )
    # DDL 選項 li.e-list-item（native click 可行，2026-07-27 實測；結構文件記的時序失敗不準）
    li_split_rule_option = (By.XPATH, "//li[contains(@class,'e-list-item') and contains(.,'%s')]")
    input_split_value = (By.XPATH, "//div[@data-field-id='splitValue']//input")
    btn_split_confirm = (By.XPATH, "//div[@data-field-id='confirmButton']//button")
    # 住客帳維護消費款項 Grid 的 data row（panel scope，拆帳筆數驗證用）
    row_consumption = (
        By.XPATH,
        "//div[contains(@class,'panel-title') and normalize-space()='住客帳維護單筆']"
        "/ancestor::div[contains(@class,'panel')]//div[contains(@class,'datagrid-view2')]"
        "//tr[contains(@class,'datagrid-row')]",
    )

    # ----- 帳夾管理 / 移動帳夾（#559）-----
    btn_open_folio_management = (By.XPATH, "//button[@data-field-id='r_1030']")
    # 消費款項 Table 的 ck checkbox（勾第一筆；事後 acct_nos diff 追蹤，不定位特定筆）
    checkbox_folio_consume_first = (
        By.XPATH,
        "(//div[contains(@class,'panel-title') and normalize-space()='帳夾管理']"
        "/ancestor::div[contains(@class,'panel')]//input[@name='ck'])[1]",
    )
    # 帳夾 Table folio row（folio_nam 值 scope）
    cell_folio_in_table = (
        By.XPATH,
        "//div[contains(@class,'panel-title') and normalize-space()='帳夾管理']"
        "/ancestor::div[contains(@class,'panel')]//td[@field='folio_nam' and normalize-space()='%s']",
    )
    btn_folio_move = (
        By.XPATH,
        "//div[contains(@class,'panel-title') and normalize-space()='帳夾管理']"
        "/ancestor::div[contains(@class,'panel')]//button[normalize-space()='移動']",
    )
    btn_folio_save = (
        By.XPATH,
        "//div[contains(@class,'panel-title') and normalize-space()='帳夾管理']"
        "/ancestor::div[contains(@class,'panel')]//button[img[@alt='save']]",
    )
    btn_close_folio_management = (
        By.XPATH,
        "//div[contains(@class,'panel-title') and normalize-space()='帳夾管理']"
        "/ancestor::div[contains(@class,'panel')]//a[contains(@class,'panel-tool-close')]",
    )

    # ----- 結帳 / 付款方式（#496）-----
    # 結帳（住客帳維護工具列，觸發關帳流程：未關帳時 alert「尚有未入的預估款，是否要關帳?」）
    btn_checkout_toolbar = (By.XPATH, "//button[@data-field-id='r_PMS0310011_1100']")
    # 開關帳 toggle（復原用：K 關帳 → click + alertOK「是否要開帳?」→ O 開帳）
    btn_toggle_account = (By.XPATH, "//button[@data-field-id='r_1090']")
    # 結帳 dialog 內結帳（觸發結帳確認；實測直接跳發票載具，跳過 Gherkin 的「是否要結帳?」alert）
    btn_checkout_dialog = (By.XPATH, "//button[@data-field-id='checkout']")
    # 新增付款方式（綠色加號 sub-button--add，觸發「請輸入付款方式」dialog）
    btn_add_payment = (By.XPATH, "//div[contains(@class,'sub-button--add')]")
    # 付款方式 Element UI el-select（現金/VISA/MASTER 等）
    select_pay_way = (
        By.XPATH,
        "//td[@data-field-id='pay_way']//div[contains(@class,'el-select')]//input",
    )
    # 付款方式選項（Element UI li，contains 代號避「現  金」雙空白 exact 問題；visible dropdown scope）
    option_pay_way = (
        By.XPATH,
        "//div[contains(@class,'el-select-dropdown') and not(contains(@style,'display: none'))]"
        "//li[contains(@class,'el-select-dropdown__item')]"
        "[contains(normalize-space(),'%s')]",
    )
    # 信用卡特有欄位（選信用卡後動態長出，現金無此分支；純 text input 非 EasyUI）
    input_credit_nos = (By.XPATH, "//div[@data-field-id='credit_nos']//input")
    input_expira_mm = (By.XPATH, "//div[@data-field-id='expira_mmyy']//input[@placeholder='MM']")
    input_expira_yyyy = (
        By.XPATH,
        "//div[@data-field-id='expira_mmyy']//input[@placeholder='YYYY']",
    )
    # 付款金額（Syncfusion numeric，dfid 在 td 不在 div故 //div[...]找不到；[1]取 visible，Syncfusion 雙 input）
    # 單筆自動帶入應收免 type；多筆分攤需 type 改值
    input_pay_amt = (By.XPATH, "(//td[@data-field-id='pay_amt']//input)[1]")
    # 客戶簽帳(41) cust_cod combogrid textbox-text（Phase 2 CLI pom-out 驗證）。
    # [last()] 限縮避結帳 dialog 主畫面的 cust_cod「結帳對象」(id=cli-scope-temp)。
    # combogrid textbox-text not interactable，選公司用 JS（見 input_sign_company）
    input_sign_cust_cod = (
        By.XPATH,
        "(//div[@data-field-id='cust_cod' and not(@id='cli-scope-temp')]"
        "//input[contains(@class,'textbox-text')])[last()]",
    )
    # 付款方式 save（付款存入結帳 dialog pay_tot，dialog 關，無 alert）
    btn_save_payment = (By.XPATH, "//button[@data-field-id='r_w_pay_dt_1032']")
    # ----- #601 簽帳帶入驗證（dialog 存在判定 + 讀值 + 不結帳收尾）-----
    dialog_checkout = (
        By.XPATH,
        "//div[contains(@class,'panel-title') and normalize-space()='結帳']",
    )
    dialog_payment = (
        By.XPATH,
        "//div[contains(@class,'panel-title') and normalize-space()='請輸入付款方式']",
    )
    btn_close_payment_dialog = (
        By.XPATH,
        "//div[contains(@class,'panel-title') and normalize-space()='請輸入付款方式']"
        "/parent::div//a[contains(@class,'panel-tool-close')]",
    )
    btn_close_checkout_dialog = (
        By.XPATH,
        "//div[contains(@class,'panel-title') and normalize-space()='結帳']"
        "/parent::div//a[contains(@class,'panel-tool-close')]",
    )
    # 讀付款 dialog 帶入值（el-select input value = '41:客戶簽帳(要開)'）
    input_pay_way_value = (
        By.XPATH,
        "//td[@data-field-id='pay_way']//div[contains(@class,'el-select')]//input",
    )
    # 發票載具確定（儲存後 alert「確認附屬程式已打開 並 重整網頁」）
    btn_invoice_confirm = (By.XPATH, "//button[@data-field-id='printInVoiceSave']")
    # 列印帳單 dialog 關閉（=取消列印；panel-title parent scope）
    btn_close_print_bill = (
        By.XPATH,
        "//div[contains(@class,'panel-title') and normalize-space()='列印帳單']"
        "/parent::div//a[contains(@class,'panel-tool-close')]",
    )
    # el-message-box 取消按鈕（退房確認 alert 按取消不退房；alert-ok 無 --cancel 支援）
    btn_cancel_messagebox = (
        By.XPATH,
        "//div[contains(@class,'el-message-box')]//button[normalize-space()='取消']",
    )
    # el-message-box 確定按鈕（退房確認按確定=退房，狀態轉 Check Out；對稱 cancel 的 text 定位）
    btn_confirm_messagebox = (
        By.XPATH,
        "//div[contains(@class,'el-message-box')]//button[normalize-space()='確定']",
    )
    # el-message-box 訊息文字（多 <p> 組成，text_tip 雙層 p 只抓首 p；用此抓整段含是否退房）
    text_messagebox = (By.XPATH, "//div[contains(@class,'el-message-box__message')]")
    # 帳戶狀態 combobox（復原判斷 O/K，value「O : 開帳」/「K : 關帳」。
    # 住客帳維護 panel ancestor scope 唯一，排除入帳/轉帳子 dialog 的 placeholder 請選擇）
    text_account_status = (
        By.XPATH,
        "//div[contains(@class,'panel-title') and normalize-space()='住客帳維護單筆']"
        "/ancestor::div[contains(@class,'panel')]//input[@placeholder='請選擇']",
    )

    # ----- 發票載具 dialog / 發票明細（#497）-----
    # panel-title '發票載具' scope（cli-scope-temp 是 CLI 動態 id，session 間漂移不可用作 locator）
    # 統一編號（dialog 內首個 input class='input'，enabled）
    input_invoice_ubn = (
        By.XPATH,
        "(//div[contains(@class,'panel-title') and normalize-space()='發票載具']"
        "/ancestor::div[contains(@class,'panel')]//input[@class='input'])[1]",
    )
    # 載具類別（原生 select，Selenium Select 類操作。選後統編 DISABLED。option: NOTHING/CQ0001/3J0002）
    select_carrier_type = (
        By.XPATH,
        "//div[contains(@class,'panel-title') and normalize-space()='發票載具']"
        "/ancestor::div[contains(@class,'panel')]//select",
    )
    # 載具顯碼（select 父 field 的 following sibling field，label '載具顯碼'；選載具類別後 enabled）
    input_carrier_id = (
        By.XPATH,
        "//div[contains(@class,'panel-title') and normalize-space()='發票載具']"
        "/ancestor::div[contains(@class,'panel')]//select/ancestor::div[@class='field']"
        "/following-sibling::div[@class='field'][1]//input",
    )
    # 捐贈=是 radio label（Element UI radio，native click input 被 label 蓋；label id=selectDonationYes）
    rb_donate_yes = (
        By.XPATH,
        "//div[contains(@class,'panel-title') and normalize-space()='發票載具']"
        "/ancestor::div[contains(@class,'panel')]//label[@id='selectDonationYes']",
    )
    # 愛心碼（捐贈=是 後 enabled，dialog 內第 4 個 input class='input'）
    input_love_code = (
        By.XPATH,
        "(//div[contains(@class,'panel-title') and normalize-space()='發票載具']"
        "/ancestor::div[contains(@class,'panel')]//input[@class='input'])[4]",
    )
    # 列印證明聯=是 radio label（沒統編變體必需，否則擋「不印證明聯且無統編時需載具或愛心碼」）
    rb_print_proof_yes = (
        By.XPATH,
        "//div[contains(@class,'panel-title') and normalize-space()='發票載具']"
        "/ancestor::div[contains(@class,'panel')]//label[@id='selectPrintProofYes']",
    )
    # 已結帳總額入口（label following-sibling sub-button--more，同 btn_open_deposit_dialog 公式）
    btn_open_checkedout = (
        By.XPATH,
        "//label[normalize-space()='已結帳總額']/following-sibling::span[contains(@class,'sub-button--more')]",
    )
    # 發票明細按鈕（已結帳 dialog 內 uninvDetail）
    btn_invoice_detail = (By.XPATH, "//button[@data-field-id='uninvDetail']")
    # 發票明細欄位（DISABLED 顯示用，對應 #497 Postconditions）
    text_inv_nos = (By.XPATH, "//div[@data-field-id='uniinv_nos']//input")
    text_inv_amt = (By.XPATH, "//div[@data-field-id='uniinv_amt']//input")
    text_inv_ubn = (By.XPATH, "//div[@data-field-id='uni_cod']//input")
    text_inv_donate = (
        By.XPATH,
        "//div[@data-field-id='donatemark']//input[contains(@class,'textbox-value')]",
    )
    text_inv_love = (By.XPATH, "//div[@data-field-id='npoban']//input")
    text_inv_carrier_type = (
        By.XPATH,
        "//div[@data-field-id='carriertype']//input[contains(@class,'textbox-value')]",
    )
    text_inv_carrier_id1 = (By.XPATH, "//div[@data-field-id='carrierid1']//input")
    text_inv_carrier_id2 = (By.XPATH, "//div[@data-field-id='carrierid2']//input")
    # 發票明細視窗關閉（panel-title scope）
    btn_close_invoice_detail = (
        By.XPATH,
        "(//div[contains(@class,'panel-title') and normalize-space()='發票明細']"
        "/ancestor::div[contains(@class,'panel')])[1]//a[contains(@class,'panel-tool-close')]",
    )

    # 已結帳 grid 最新結帳 row 的序號 cell（click 選取最新發票；[last()]=序號最大=最新結帳）
    cell_latest_checkout = (
        By.XPATH,
        "(//div[contains(@class,'panel-title') and normalize-space()='已結帳']"
        "/ancestor::div[contains(@class,'panel')]//td[@field='co_times'])[last()]",
    )
    # 已結帳 grid pager 最後頁按鈕（結帳累積 >50 筆時 datagrid 分頁，最新結帳在末頁，
    # [last()] 只掃得到第一頁；點最後頁冪等——已在末頁時無反應）
    btn_checkedout_last_page = (
        By.XPATH,
        "//div[contains(@class,'panel-title') and normalize-space()='已結帳']"
        "/ancestor::div[contains(@class,'panel')]//*[contains(@class,'pagination-last')]",
    )
    # 重開發票按鈕（已結帳 dialog，PMS03100311090；co_list:L708）
    btn_reinvoice = (By.XPATH, "//button[@data-field-id='PMS03100311090']")
    # 已結帳 grid 發票號碼 cell（選中 row 的 uniinv_nos；frozen+regular 雙 table 致 match=2，
    # [last()] 取 regular data cell；重開前後 get 比對新舊號；co_list:L717）
    text_checkout_invoice_no = (
        By.XPATH,
        "(//div[contains(@class,'panel-title') and normalize-space()='已結帳']"
        "/ancestor::div[contains(@class,'panel')]//td[@field='uniinv_nos'])[last()]",
    )
    # 已結帳 dialog 下方 Table「付款方式名稱」值（#514 doSave 後驗證更改生效）；
    # th header（非 td），data 在 tbody/tr/td[1]/div；多筆付款多 row（find_elements 抓 list）
    table_paymethod_value = (
        By.XPATH,
        "//table[.//th[normalize-space()='付款方式名稱']]/tbody//tr/td[1]/div",
    )

    # ----- 沖訂金(00) setup：訂金單筆新增 dialog（#496 第 5 變體）-----
    # 住客帳維護「訂金編號」欄旁 [...]（sub-button--more）入口。
    # co_list.md L204 通用瀏覽按鈕公式：label text + following-sibling sub-button--more
    btn_open_deposit_dialog = (
        By.XPATH,
        "//label[text()='訂金編號']/following-sibling::span[contains(@class,'sub-button--more')]",
    )
    # 訂金付款方式（Element UI el-select，deposit_dt_pay_way td dfid）。
    # 與結帳 select_pay_way 同為 el-select 但不同 dfid（deposit_dt_pay_way 在訂金 dialog）
    select_deposit_dt_pay_way = (By.XPATH, "//td[@data-field-id='deposit_dt_pay_way']//input")
    # 訂金使用金額（Syncfusion numeric td dfid）
    input_deposit_dt_use_amt = (By.XPATH, "//td[@data-field-id='deposit_dt_use_amt']//input")
    # 訂金單筆新增 dialog save（panel-title scope）
    btn_save_deposit = (
        By.XPATH,
        "//div[contains(@class,'panel-title') and normalize-space()='訂金單筆新增']"
        "/ancestor::div[contains(@class,'panel')]//button[img[@alt='save']]",
    )
    # 結帳 dialog 付款方式 td（00 沖訂金時自動帶入，讀 td text 驗證）。
    # 與 select_pay_way 不同：手動選用 el-select input value；00 自動帶入讀 td text
    text_pay_way = (By.XPATH, "//td[@data-field-id='pay_way']")

    # ----- 分發票 / 多張發票（#731）-----
    # 分發票按鈕（結帳 dialog 內 invoice，直接開設定 dialog 無 alert；co_list:L468）
    btn_invoice = (By.XPATH, "//button[@data-field-id='invoice']")
    # 設定 dialog：發票張數（Syncfusion numeric，CLI type 有效）
    input_uniinv_count = (By.XPATH, "//div[@data-field-id='uniinv_count']//input")
    # 設定 dialog：金額均分 checkbox label（勾=均分；co_list:L606）
    cb_is_divided_equally = (By.XPATH, "//div[@data-field-id='is_divided_equally']//label")
    # 設定 dialog 儲存（開分發票 dialog；co_list:L607）
    btn_checkInvoiceNum = (By.XPATH, "//button[@data-field-id='checkInvoiceNum']")
    # 分發票 dialog 左欄張號 cell（click 選張，%s=張號；co_list:L622）
    cell_invoice_num = (By.XPATH, "//td[@field='num' and normalize-space()='%s']")
    # 分發票 dialog 明細單價 data cell（click 進 edit mode；[last()] 取 data 非 header）
    cell_unit_price = (By.XPATH, "(//td[@field='unit_price'])[last()]")
    # 分發票 dialog 明細單價 editor（click cell 進 edit 後出現；改值觸發 price 連動；co_list:L667）
    input_unit_price = (
        By.XPATH,
        "//td[@field='unit_price']//input[contains(@class,'textbox-text')]",
    )
    # 分發票 dialog 儲存（r_1050 第三度衝突，panel-title 分發票 scope；co_list:L673）
    btn_save_invoice_split = (
        By.XPATH,
        "//div[contains(@class,'panel-title') and normalize-space()='分發票']"
        "/../..//button[@data-field-id='r_1050']",
    )
    # 發票明細視窗品明細 grid row（逐張驗證用，選行→上方單張屬性刷新；%s=row index 0..N-1；co_list:L817）
    cell_invoice_detail_row = (
        By.XPATH,
        "//div[contains(@class,'panel-title') and normalize-space()='發票明細']"
        "/ancestor::div[contains(@class,'panel')]//tr[@datagrid-row-index='%s']"
        "/td[@field='uniinv_nos']",
    )
    # 逐張屬性（結構同 #497 發票載具 dialog，scope 改分發票 panel-title；Phase 4 pytest 驗）
    # 統一編號（原始總額後第一個 class=input；co_list:L634）
    input_split_ubn = (
        By.XPATH,
        "(//div[contains(@class,'panel-title') and normalize-space()='分發票']"
        "/ancestor::div[contains(@class,'panel')]//input[@class='input'])[1]",
    )
    # 載具類別（原生 select，3 option NOTHING/CQ0001/3J0002；co_list:L635）
    select_split_carrier_type = (
        By.XPATH,
        "//div[contains(@class,'panel-title') and normalize-space()='分發票']"
        "/ancestor::div[contains(@class,'panel')]//select",
    )
    # 載具顯碼（select 父 field 的 following sibling field；選載具類別後 enabled；co_list:L636）
    input_split_carrier_id = (
        By.XPATH,
        "//div[contains(@class,'panel-title') and normalize-space()='分發票']"
        "/ancestor::div[contains(@class,'panel')]//select/ancestor::div[@class='field']"
        "/following-sibling::div[@class='field'][1]//input",
    )
    # 捐贈=是 radio label（co_list:L641）
    rb_split_donate_yes = (
        By.XPATH,
        "//div[contains(@class,'panel-title') and normalize-space()='分發票']"
        "/ancestor::div[contains(@class,'panel')]//label[@id='selectDonationYes']",
    )
    # 愛心碼（捐贈=是後 enabled，第 4 個 class=input；co_list:L642）
    input_split_love_code = (
        By.XPATH,
        "(//div[contains(@class,'panel-title') and normalize-space()='分發票']"
        "/ancestor::div[contains(@class,'panel')]//input[@class='input'])[4]",
    )
    # 列印證明聯=是 radio（沒統編變體必需；co_list:L639）
    rb_split_print_proof_yes = (
        By.XPATH,
        "//div[contains(@class,'panel-title') and normalize-space()='分發票']"
        "/ancestor::div[contains(@class,'panel')]//label[@id='selectPrintProofYes']",
    )
