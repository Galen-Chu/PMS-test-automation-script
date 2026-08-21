# C/O 清單（PMS0310020）

> 路徑：出納 → C/O 清單
> 程式代碼前綴：PMS0310020

---

## 佈局

```
C/O 清單
├── [搜尋區] — 7 欄 + 搜尋/清除按鈕
├── [Tab] — In house / Check Out
├── [Grid] — 17 欄住客列表
└── [住客帳維護按鈕] — co_Button，開啟「住客帳維護單筆」子系統

住客帳維護單筆（PMS0310011）
├── [資訊欄位] — 訂房卡號/房號/姓名/入住退房日期/住客帳狀態/未收總額/已結帳總額等
├── [工具列] — 17 個功能按鈕
├── [帳夾 Tab] — 消費款項 Grid（22 欄）
└── [...瀏覽按鈕] — 9 個 sub-button--more（已結帳總額/訂金編號/預授權/客房備註等）

子 Dialog 清單：
├── 開班（PMS0310060）— 出納前置，所有帳務操作的前置條件
├── 入帳 — 新增消費款項
├── 帳夾管理 — 帳夾間移動消費款項
├── 轉帳項目選擇 — 轉帳第一步（選消費項目）
├── 轉帳帳夾選擇 — 轉帳第二步（選目標房號+帳夾）
├── 訂金單筆新增 — 綁訂訂金
├── 單筆拆帳 — 拆帳（需先選 Grid 行）
│   └── 請輸入拆分方式 — Syncfusion DDL + 金額輸入
├── 分帳規則 — 帳夾分帳設定
├── 指定訂金 — 指定訂金到帳夾
├── 預估款維護（PMS0310011_1010）— 預估款項管理
├── 註銷 — 註銷消費款項
├── 開關帳 — toggle 開帳/關帳
├── 結帳（PMS0310011）— 結帳流程
│   ├── 付款方式 dialog — 新增付款（由 sub-button--add 觸發）
│   ├── 發票載具 dialog — 結帳時自動彈出
│   └── 列印帳單 dialog — 發票確認後彈出
└── 已結帳（PMS0310031）— 已結帳記錄管理
    ├── [工具列] — 8 個操作按鈕
    ├── [搜尋區] — 客戶姓名/房號/訂房卡號/訂房公司/客房備註/退房提醒
    └── [Grid] — 25 欄結帳記錄
```

## 框架分布

| 區塊 | 框架 | 判斷依據 |
|------|------|---------|
| 搜尋區（大部分） | Syncfusion EJ2 | `data-field-id`、syncfusion 數量 570 |
| 搜尋區（訂房公司） | jQuery EasyUI | `_easyui_textbox_input` |
| Tab | 標準 div | `tab-inHouse_Tab` / `tab-checkedOut_Tab` |
| Grid | EasyUI DataGrid | `datagrid-row-*` ID pattern |
| 開班 dialog | Element UI + Syncfusion | `el-select` (廳別) + Syncfusion (班別) |
| 住客帳維護單筆 | Syncfusion + EasyUI 混合 | Syncfusion numerictextbox + EasyUI textbox |
| 入帳 panel | EasyUI + Syncfusion + Element UI | 三框架混合 |
| 帳夾管理 | EasyUI | pure EasyUI |
| 轉帳項目選擇 | EasyUI | pure EasyUI |
| 轉帳帳夾選擇 | EasyUI + Syncfusion | EasyUI select + Syncfusion |
| 訂金單筆新增 | Element UI + Syncfusion | `el-select` + Syncfusion numeric |
| 單筆拆帳 | Syncfusion | pure Syncfusion DDL + input |
| 分帳規則 | EasyUI + Syncfusion | EasyUI combobox + Grid |
| 指定訂金 | EasyUI | EasyUI combobox |
| 預估款維護 | EasyUI + Element UI | EasyUI input + Element UI |
| 註銷 | EasyUI | pure EasyUI |
| 結帳 | EasyUI + Syncfusion | `data-field-id` + Syncfusion numeric |
| 付款方式 | Element UI + Syncfusion + EasyUI | `el-select`(pay_way) + Syncfusion(pay_amt) |
| 發票載具 | EasyUI + Syncfusion | `<select>`(載具類別) + Syncfusion(發票金額) |
| 列印帳單 | EasyUI + Syncfusion | `<select>`(template) + Syncfusion(份數) |
| 已結帳 | EasyUI + Syncfusion | 混合 |

## 元素清單

### 搜尋區

| 元素 | 類型 | Locator | 備註 |
|------|------|---------|------|
| 房號 | input | `//div[@data-field-id='guest_mn.room_nos']//input` | |
| 公帳號 | input | `//div[@data-field-id='guest_mn.master_nos']//input` | |
| 關聯單號 | input | `//div[@data-field-id='order_mn.link_nos']//input` | |
| 訂房卡號 | input | `//div[@data-field-id='guest_mn.ikey']//input` | |
| 姓名 | input | `//div[@data-field-id='guest_mn.alt_nam']//input` | |
| 團號 | input | `//div[@data-field-id='order_mn.group_nos']//input` | |
| 訂房公司 | input | `//div[@data-field-id='guest_mn.acust_cod']//input` | **EasyUI** |
| 搜尋 | button | `//button[@data-field-id='PMS0310020_doSearch']` | 帶程式代碼前綴 |
| 清除 | button | `//button[@data-field-id='PMS0310020_doClear']` | |
| 住客帳維護 | button | `//button[@data-field-id='co_Button']` | 需先選取 Grid 行 |

**參數化**：`//div[@data-field-id='guest_mn.%s']//input` 或 `//div[@data-field-id='order_mn.%s']//input`

### Tab

| 元素 | 類型 | Locator | 備註 |
|------|------|---------|------|
| In house | div | `//div[@id='tab-inHouse_Tab']` | 預設 |
| Check Out | div | `//div[@id='tab-checkedOut_Tab']` | 退房後的記錄 |

### Grid（In house）

17 欄：ikey, room_nos, room_ser, link_nos, alt_nam, eco_tim, balance_amt, guest_sta, acust_nam, ci_dat, ci_tim, show_cod, cust_nam, uni_cod, uni_title, cust_cod, cust_dispalay

**定位**：`//td[@field='%s']`

### 住客帳維護單筆（PMS0310011）

#### 功能按鈕

| 元素 | 類型 | Locator | 狀態 | 備註 |
|------|------|---------|------|------|
| 讀卡 | button | `//button[@data-field-id='readCard']` | enabled | |
| 單筆拆帳 | button | `//button[@data-field-id='split']` | enabled | 需先選 Grid 行 |
| 分帳規則 | button | `//button[@data-field-id='r_1020']` | enabled | |
| 指定訂金 | button | `//button[@data-field-id='r_1130']` | enabled | |
| 預估款維護 | button | `//button[@data-field-id='r_PMS0310011_1010']` | enabled | 子程式前綴 |
| 帳夾管理 | button | `//button[@data-field-id='r_1030']` | enabled | |
| 入帳 | button | `//button[@data-field-id='r_1040']` | enabled | |
| 轉帳 | button | `//button[@data-field-id='r_1050']` | enabled | |
| 註銷 | button | `//button[@data-field-id='r_1060']` | enabled | |
| 開關帳 | button | `//button[@data-field-id='r_1090']` | enabled | toggle：開帳↔關帳 |
| 列印帳單 | button | `//button[@data-field-id='r_PMS0310011_1080']` | enabled | 子程式前綴 |
| 結帳 | button | `//button[@data-field-id='r_PMS0310011_1100']` | enabled | 子程式前綴 |
| 相關房號 | button | `//button[@data-field-id='r_1120']` | enabled | |
| 房務入帳 | button | `//button[@data-field-id='r_1070']` | DISABLED | |
| 齊來卡優惠券 | button | `//button[normalize-space()='齊來卡優惠券']` | enabled | 無 data-field-id |
| 住房掛帳 | button | `//button[normalize-space()='住房掛帳']` | DISABLED | 無 data-field-id |

**參數化**：`//button[@data-field-id='%s']`

#### 資訊欄位

| 元素 | 類型 | Locator | 狀態 |
|------|------|---------|------|
| 訂房卡號 | input | DISABLED | 顯示用 |
| 房號 | input | DISABLED | 顯示用 |
| 姓名 | input | DISABLED | 顯示用 |
| 入住日期 | input | DISABLED | 顯示用 |
| 退房日期 | input | DISABLED | 顯示用 |
| 車號 | input | DISABLED | 顯示用 |
| 住客帳狀態 | input | DISABLED | 顯示用 |
| 訂房公司 | input | DISABLED | 顯示用 |
| 未收總額 | numeric | `//input[@id='numerictextbox_2933']` | enabled |
| 已結帳總額 | numeric | `//input[@id='numerictextbox_2934']` | enabled + [...] 瀏覽 |
| 訂金編號 | input | DISABLED + [...] 瀏覽 | |
| 預授權 | numeric | `//input[@id='numerictextbox_2935']` | enabled + [...] 瀏覽 |
| 客房備註 | input | DISABLED + [...] 瀏覽 | |
| 退房提醒 | input | DISABLED | |
| 住房掛帳 | checkbox | `//input[@name='form-field-checkbox']` | DISABLED |

**瀏覽按鈕定位**：`//label[text()='%s']/following-sibling::span[contains(@class,'sub-button--more')]`

#### 消費款項 Grid（帳夾 Tab）

22 欄：athena_id, hotel_cod, acct_dat, bill_dat, item_nos, item_nam, item_qnt, item_tot, detail_sta, ins_usr, rspt_cod, iroom_nos, shift_cod, remark1~4 及其 value 欄, upd_dat, acct_nos

**Tab 定位**：`//div[@id='tab-1']`

### 開班（PMS0310060）— 出納前置

| 元素 | 類型 | Locator | 狀態 | 備註 |
|------|------|---------|------|------|
| 日期 | input | `//div[@data-field-id='shop_dat']//input` | DISABLED | 營業日期 |
| 廳別 | select | `//div[@data-field-id='rspt_cod']//input` | enabled | **Element UI el-select** |
| 使用者 | input | `//div[@data-field-id='open_man']//input` | DISABLED | |
| 班別 | input | `//div[@data-field-id='shift_cod']//input` | enabled | |
| 密碼 | password | `//div[@data-field-id='s99_user.usr_pwd']//input` | enabled | |
| 確認 | button | `//button[@data-field-id='PMS0310060_r_1011']` | enabled | |

**開班測試資料**：廳別=`FO : 飯店櫃檯`、班別=`a`、密碼=`autotest`

**Element UI select 操作**：需用 JS 先開 dropdown 再選項（CLI 兩步之間下拉會消失）

### 入帳

| 元素 | 類型 | Locator | 備註 |
|------|------|---------|------|
| 消費代號 | Element UI el-select | `//div[@class='panel-title' and text()='入帳']/parent::div/following-sibling::div//div[contains(@class,'el-select')]//input` | ⚠️ CLI 需連續操作，中間不能做其他指令 |
| 單價 | Syncfusion numeric | `(//div[@class='panel-title' and text()='入帳']/parent::div/following-sibling::div//input[contains(@id,'numerictextbox_')])[1]` | |
| 數量 | number input | | |
| 小計 | Syncfusion numeric | | |
| 內部備註 | text input | | |
| 帳單備註 | text input | | |
| 帳單日期 | date input | | |
| save | img button | `//div[@class='panel-title' and text()='入帳']/parent::div/following-sibling::div//img[@alt='save']` | |

**入帳流程**：選消費代號 → 設金額 → save。用「1001 : 房租」最單純（不觸發付款方式 dialog）

**Element UI select 操作**：click input → **立即** click 選項（`(//div[contains(@class,'el-select-dropdown') and not(contains(@style,'display: none'))]//span[text()='選項文字']/parent::li)[last()]`），兩步之間不能做其他操作

**Grid (11 欄)**：acct_nos, item_nos, item_nam, item_amt, item_qnt, item_tot, room_nos, folio_nos, remark3, remark4, bill_dat

### 帳夾管理

| 元素 | 類型 | 備註 |
|------|------|------|
| 帳夾 dropdown | EasyUI combobox | `placeholder="請選擇"` |
| 移動 | button | DISABLED（需先選取消費+帳夾） |
| 指定訂金 | button | enabled |
| add | img button | `img_alt: add` |
| remove | img button | `img_alt: remove` |
| save | img button | `img_alt: save` |

**消費款項 Grid (16 欄)**：ck (checkbox), acct_dat, item_nam, item_qnt, item_tot, bill_dat, iroom_nos, remark4, folio_nam, ccust_nam, cust_cod, pay_way, uni_cod, uni_title, cal_acu, folio_nos

### 轉帳項目選擇

| 元素 | 類型 | 備註 |
|------|------|------|
| 帳夾 dropdown | EasyUI combobox | `placeholder="請選擇"` |
| 轉出金額小計 | input | DISABLED |
| 轉帳 | button | 點擊後進入「轉帳帳夾選擇」第二步 |

**Grid (15 欄)**：ck (checkbox), acct_dat, bill_dat, item_nam, item_qnt, item_tot, detail_sta, ins_usr, rspt_cod, iroom_nos, shift_cod, remark3, remark1, remark4, upd_dat

### 轉帳帳夾選擇（第二步）

| 元素 | 類型 | Locator | 狀態 | 備註 |
|------|------|---------|------|------|
| 轉帳對象 | radio group | `//div[@data-field-id='choose']//input` | enabled | 3 選項 |
| 相同訂房卡 | radio | `//div[@data-field-id='choose']//label[contains(.,'1 : 相同訂房卡')]` | enabled | |
| 全部房號 | radio | `//div[@data-field-id='choose']//label[contains(.,'2 : 全部房號')]` | enabled | |
| 選擇房號 | radio | `//div[@data-field-id='choose']//label[contains(.,'3 : 選擇房號')]` | enabled | |
| 房號 | input | `//div[@data-field-id='room_nos']//input` | enabled | 選擇房號時用 |
| 帳夾 | select | `<select>` | enabled | EasyUI |
| 轉帳 | button | `//button[normalize-space()='轉帳']` | enabled | ⚠️ 不可逆 |

**Grid (3 欄)**：room_nos, alt_nam, folio_nam

### 單筆拆帳（請輸入拆分方式）

| 元素 | 類型 | Locator | 狀態 | 備註 |
|------|------|---------|------|------|
| 拆分方式 | Syncfusion DDL | `//div[@data-field-id='splitRule']//input` | enabled | 筆數/百分比/金額 |
| 拆分值 | input | `//div[@data-field-id='splitValue']//input` | enabled | |
| 確定 | button | `//div[@data-field-id='confirmButton']//button` | enabled | |
| 關閉 | button | `//button[@title='關閉']` | enabled | |

**拆分方式選項**：AVERAGE:筆數, PERCENT:百分比, AMOUNT:金額

**操作流程**：先選取消費款項 Grid 行 → 點拆帳按鈕 → 選拆分方式 → 輸入值 → 確定

### 訂金單筆新增

| 元素 | 類型 | Locator | 狀態 |
|------|------|---------|------|
| 訂金編號 | input | `//div[@data-field-id='deposit_nos']//input` | DISABLED |
| 姓名 | input | `//div[@data-field-id='deposit_mn_alt_nam']//input` | enabled |
| 電話 | input | `//div[@data-field-id='deposit_mn_tel_nos']//input` | enabled |
| 訂金大類 | select | `//div[@data-field-id='deposit_mn_type1_cod']//input` | enabled, EasyUI |
| 發票開立方式 | select | `//div[@data-field-id='deposit_mn_uniinv_sta']//input` | enabled, EasyUI |
| 訂金備註 | input | `//div[@data-field-id='deposit_mn_remark1']//input` | enabled |
| 付款方式 | select | `//div[@data-field-id='deposit_dt_pay_way']//input` | enabled, EasyUI |
| 使用金額 | numeric | `//div[@data-field-id='deposit_dt_use_amt']//input` | enabled |
| 備註 | input | `//div[@data-field-id='deposit_dt_remark1']//input` | enabled |
| save | img button | `img_alt: save` | enabled |

### 分帳規則

| 元素 | 類型 | Locator | 狀態 | 備註 |
|------|------|---------|------|------|
| 公帳號狀態 | select | `//div[@data-field-id='master_sta']//input` | enabled | EasyUI combobox |
| 房號 | input | `//div[@data-field-id='room_nos']//input` | DISABLED | |
| 套用分帳代號 | button | `//button[normalize-space()='套用分帳代號']` | enabled | |
| 全選 | button | `//button[normalize-space()='全選']` | enabled | |
| add | button | `//button[child::img[@alt='add']]` | enabled | |
| save | button | `//button[child::img[@alt='save']]` | enabled | |
| 瀏覽房號 | button | `//div[@data-field-id='room_nos_btn']//button` | enabled | |

**Grid (8 欄)**：folio_nam, ccust_nam, cust_cod, pay_way, uni_cod, uni_title, cal_acu, folio_nos

### 指定訂金

| 元素 | 類型 | Locator | 狀態 | 備註 |
|------|------|---------|------|------|
| 訂金編號 | input | `//div[@data-field-id='deposit_nos']//input` | enabled | EasyUI |
| 訂金帳夾 | select | `//div[@data-field-id='dps_folio_nos']//input` | enabled | EasyUI combobox |
| save | button | `//button[child::img[@alt='save']]` | enabled | |

### 預估款維護（PMS0310011_1010）

| 元素 | 類型 | Locator | 狀態 | 備註 |
|------|------|---------|------|------|
| 重新讀取 | button | `//button[normalize-space()='重新讀取']` | enabled | |
| 批次新增 | button | `//button[normalize-space()='批次新增']` | enabled | |
| 轉至住客帳 | button | `//button[normalize-space()='轉至住客帳']` | enabled | |
| save | button | `//button[child::img[@alt='save']]` | enabled | |
| remove | button | `//button[child::img[@alt='remove']]` | enabled | |
| add | button | `//button[child::img[@alt='add']]` | enabled | |
| 序號 | input | | DISABLED | |
| 住客姓名 | input | | DISABLED | |
| 住客備註 | input | | DISABLED | |

### 註銷

| 元素 | 類型 | Locator | 狀態 | 備註 |
|------|------|---------|------|------|
| 儲存 | button | `//button[normalize-space()='儲存']` | enabled | ⚠️ 不可逆 |
| 轉帳註銷列表 | button | `//button[normalize-space()='轉帳註銷列表']` | enabled | |

**Grid**：含 checkbox 可勾選要註銷的消費項目

### 開關帳

點擊後直接彈確認 alert（是否要關帳？），無獨立 dialog。toggle 行為：開帳↔關帳。

### 結帳（PMS0310011）

#### 主 dialog

| 元素 | 類型 | Locator | 狀態 | 備註 |
|------|------|---------|------|------|
| 分發票 | button | `//button[@data-field-id='invoice']` | enabled | |
| 結帳 | button | `//button[@data-field-id='checkout']` | enabled | 觸發結帳流程 |
| 清除付款 | button | `//button[@data-field-id='clear']` | enabled | |
| 結帳對象類別 | select | `//div[@data-field-id='cust_typ']//input` | enabled | EasyUI combobox |
| 結帳對象 | input | `//div[@data-field-id='cust_cod']//input` | enabled | |
| 統一編號 | input | `//div[@data-field-id='uni_cod']//input` | enabled | |
| 發票抬頭 | input | `//div[@data-field-id='uni_title']//input` | enabled | |
| 買受人地址 | input | `//div[@data-field-id='buyer_add']//input` | enabled | |
| 前檯備註 | input | `//div[@data-field-id='front_desk_remark']//input` | enabled | |
| 應收合計 | numeric | `//input[@data-field-id='bill_tot']` | DISABLED | |
| 已付金額 | numeric | `//input[@data-field-id='pay_tot']` | DISABLED | |
| 未付金額 | numeric | `//input[@data-field-id='balance_amt']` | DISABLED | |
| 新增付款方式 | clickable | `//div[contains(@class,'sub-button--add')]` | enabled | 觸發「請輸入付款方式」dialog |

**結帳流程**：關帳確認(alertOK) → 設結帳對象/統編等 → 新增付款方式 → 結帳 → 發票載具 → 列印帳單

#### 付款方式 dialog（請輸入付款方式）

| 元素 | 類型 | Locator | 狀態 | 備註 |
|------|------|---------|------|------|
| 付款方式 | Element UI el-select | `//td[@data-field-id='pay_way']//div[contains(@class,'el-select')]//input` | enabled | 需連續 click 操作 |
| 金額 | Syncfusion numeric | `//div[@data-field-id='pay_amt']//input` | enabled | |
| save | button | `//button[@data-field-id='r_w_pay_dt_1032']` | enabled | img_alt: save |

**付款方式選項**：00:沖訂金, 10:現  金, 18:彰銀, 31:VISA卡, 32:MASTER信用卡, 33:cash-re, 34:AE信用卡 等

#### 發票載具 dialog

| 元素 | 類型 | Locator | 狀態 | 備註 |
|------|------|---------|------|------|
| 統一編號 | input | | enabled | |
| 發票金額 | Syncfusion numeric | `//input[@id='numerictextbox_2945']` | enabled | |
| 載具類別 | select | `<select>` | enabled | 不選擇/自然人憑證/手機條碼 |
| 載具顯碼 | input | | enabled | |
| 買受人 | input | | DISABLED | |
| 買受人地址 | input | | enabled | |
| 列印證明聯 | radio | `//input[@name='selectPrintProofYes/No']` | enabled | 是/否 |
| 列印明細表 | radio | `//input[@name='selectPrintDetailYes/No']` | enabled | 是/否 |
| 是否捐贈 | radio | `//input[@name='selectDonationYes/No']` | enabled | 是/否 |
| 愛心碼 | textarea | | enabled | |
| 確定 | button | `//button[@data-field-id='printInVoiceSave']` | enabled | |

#### 列印帳單 dialog

| 元素 | 類型 | Locator | 狀態 | 備註 |
|------|------|---------|------|------|
| 樣板 | select | `//div[@data-field-id='template']//input` | enabled | EasyUI combobox |
| 列印份數 | Syncfusion numeric | `//div[@data-field-id='copy_qnt']//input` | enabled | |
| 帳單類型 | radio group | `//div[@data-field-id='type']//input` | enabled | 6 種類型 |
| 預覽列印 | button | `//button[normalize-space()='預覽列印']` | enabled | |
| 列印 | button | `//button[normalize-space()='列印']` | enabled | |
| export | button | `//button[img[@alt='export']]` | enabled | |

**帳單類型選項**：common(標準帳單), date_guest(日期/住客), date_guest_item(日期/住客/項目), date_item(日期/項目), date_sum(日期加總), date_transaction_type(日期/交易類別)

### 已結帳（PMS0310031）

#### 功能按鈕

| 元素 | 類型 | Locator | 備註 |
|------|------|---------|------|
| 帳單列印 | button | `//button[@data-field-id='r_PMS0310031_1030']` | |
| 結帳還原 | button | `//button[@data-field-id='r_PMS0310031_1010']` | ⚠️ 不可逆 |
| 轉帳註銷列表 | button | `//button[@data-field-id='r_PMS0310031_1080']` | |
| 預估款 | button | `//button[@data-field-id='PMS03100311040']` | |
| 發票明細 | button | `//button[@data-field-id='uninvDetail']` | |
| 更改付款方式 | button | `//button[@data-field-id='editPayMent']` | |
| 重開發票 | button | `//button[@data-field-id='PMS03100311090']` | |
| 重分發票 | button | `//button[@data-field-id='PMS03100311100']` | |

#### 搜尋區

| 元素 | 類型 | Locator | 狀態 |
|------|------|---------|------|
| 客戶姓名 | input | `//div[@data-field-id='alt_nam']//input` | DISABLED |
| 房號 | input | `//div[@data-field-id='room_nos']//input` | enabled, EasyUI dropdown |
| 訂房卡號 | input | `//div[@data-field-id='ikey']//input` | DISABLED |
| 訂房公司 | input | `//div[@data-field-id='acust_nam']//input` | DISABLED |
| 客房備註 | input | `//div[@data-field-id='fo_remark']//input` | DISABLED |
| 退房提醒 | input | `//div[@data-field-id='co_rmk']//input` | DISABLED |
| 瀏覽按鈕 | button | `//div[@data-field-id='searchAltNam']//button` 等 | 5 個搜尋瀏覽 |

#### Grid（25 欄）

co_times, co_dat, co_tim, co_rspt_cod, co_shift, co_usr, item_tot, uniinv_nos, item_nam, acct_dat, item_nos, item_qnt, have_child, rspt_cod, ins_usr, shift_cod, bill_dat, remark3, remark4, remark1 及多個隱藏欄位

**定位**：`//td[@field='%s']`

## 操作備註

### Grid 行選取
- C/O 清單 Grid 是 EasyUI DataGrid，行 ID 格式：`gid_{id}_datagrid-row-r{num}-1-0`
- **選取方式**：click 有值的 td cell，如 `click -x "//td[@field='room_nos' and normalize-space()='526']"`。frozen table 的 td 不可互動，需點 regular body table 中有資料的 cell
- diff 可偵測行選取（`SELECTION grid:selected/deselected row`）
- scan 不列出 DataGrid 行：需用 `find -x "//tr[contains(@class,'datagrid-row')]"` 找行

### 開班前置
- 所有帳務操作（住客帳維護→結帳/入帳/轉帳等）**都需要先完成開班**
- 未開班時點住客帳維護 → 自動跳出開班 dialog → 開班成功後自動進入住客帳維護單筆
- 開班是 session 級別，一次開班後後續操作不需重複

### Element UI 下拉（開班廳別、入帳消費代號）
- Element UI `el-select`，非 Syncfusion DropDownList
- **CLI 可以兩步操作**：click input 開下拉 → 立即 click 選項（`(//div[contains(@class,'el-select-dropdown') and not(contains(@style,'display: none'))]//span[text()='選項文字']/parent::li)[last()]`）
- ⚠️ 兩步之間不能做其他操作（如 find/describe），��則下拉會消失
- `ddl-options` 已支援 Element UI `el-select-dropdown` 偵測，輸出會標記 `elementui` framework
- 選項文字含全形字元：是「櫃**檯**」不是「櫃**台**」
- 同時存在多個 `el-select-dropdown`（sidebar 選單 vs 頁面內選單），需用 `[last()]` 或 `not(contains(@style,'display: none'))` 篩選

### 結帳流程
- 點結帳 → 先彈「提示是否要關帳？」alert（alertOK 確認）→ 關帳成功 → 進入結帳 dialog
- 結帳 dialog 內：設結帳對象/統編 → 點 sub-button--add 新增付款方式 → 選付款方式+金額 → save
- 付款方式 save 後 → 點結帳按鈕 → 彈發票載具 dialog → 確定 → 彈列印帳單 dialog
- 列印帳單關閉後 → 結帳 dialog 關閉 → 彈「此房間退房日期: YYYY/MM/DD 無須付款項目,是否退房？」alert
- 確認退房 → 完成
- 無未收款項時直接跳「無須付款項目,是否退房？」alert

### Dialog 關閉方式彙整

| 類型 | 關閉方式 | 適用 dialog |
|------|---------|------------|
| EasyUI Panel | `(//a[contains(@class,'panel-tool-close')])[last()]` | 帳夾管理、轉帳項目選擇、入帳、訂金單筆新增、已結帳 |
| Syncfusion Dialog | `//button[@title='關閉']` | 結帳 📌 待確認 |

### diff 盲區
- DataGrid 行選取：click 不觸發 DOM 變化
- 開班確認：click 確認後的 dialog/alert 跳轉有時不被 diff 偵測
- 訂金單筆新增開啟：diff 偵測為 dialog 但 button click 順序可能不同

### 子程式邊界
- PMS0310020 — C/O 清單（主頁面）
- PMS0310060 — 開班（出納前置）
- PMS0310011 — 住客帳維護單筆（工具列按鈕前綴 r_PMS0310011_*）
- PMS0310031 — 已結帳（按鈕前綴 r_PMS0310031_*/PMS0310031*）

### 未展開區域
- 重開發票/重分發票/更改付款方式/發票明細 子 dialog — 需在已結帳選取行後操作
- 齊來卡優惠券 — 未探索
