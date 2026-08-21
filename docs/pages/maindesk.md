# 綜合櫃檯（PMS0210020）

> 路徑：接待 → 綜合櫃檯
> 程式代碼前綴：PMS0210020

---

## 佈局

```
綜合櫃檯
├── [搜尋區] ─ 兩排搜尋欄位（第二排預設收合）+ 搜尋/清除/展開按鈕
├── [工具列] ─ 大圖示切換 + 房控連線 + 注意事項 + 房間狀態統計按鈕
├── [樓層篩選] ─ 左側垂直 tab（ALL/NF/1F~20F/111F/222F）
├── [房間卡片區] ─ Vue 卡片 grid + 底部分頁器
└── [房間細節 Panel] ─ 點擊房間卡片後開啟（EasyUI Panel），內容依房態不同
    ├── [VC 空房模式]
    │   ├── [操作按鈕列] ─ Walk In / Day use / 拆併床 / 清掃房間
    │   ├── [房間資訊區] ─ 房號、清掃人員、瑕疵原因、房間特色
    │   ├── [訂房資訊區] ─ 注意事項、訂房公司、大人/小孩、公帳號、訂房來源、市場類別
    │   ├── [訂房備註] ─ textarea + DND/住房掛帳 checkbox
    │   └── [關閉按鈕] ─ EasyUI panel-tool-close
    └── [OC 住客模式]（額外區塊）
        ├── [住客功能列] ─ 兩排按鈕（訂房卡/關聯單號/指定訂金/改退房日/改房價/換房/預計退房時間/清掃房間/拆併床/櫃台備品/交換機/製卡/取消公帳號/住房掛帳）+ 編輯模式
        ├── [住客 Grid] ─ 住客姓名/預授權/餘額/Note/交辦/提醒/留言/失物/接送/No Info/房租/服務費/住客備註/車號
        └── [入退房資訊] ─ CI日期/CI人員/預計退房日/CO人員/系統CI日期/系統CO日期
```

## 框架分布

| 區塊 | 框架 | 判斷依據 |
|------|------|---------|
| 搜尋區（大部分欄位） | Syncfusion EJ2 | `data-field-id`、`e-` class |
| 搜尋區（訂房公司 acust_cod） | jQuery EasyUI | `_easyui_textbox_input1`、combogrid（6 grid columns） |
| 工具列 | 標準 HTML | `<button>` 無框架特徵 |
| 樓層篩選 | Vue 自訂 | `li.tab-menu-item` |
| 房間卡片區 | Vue 自訂 | `.card--room`、`data-v-` attributes |
| 房間細節 Panel | EasyUI + Syncfusion 混合 | Panel 外框 = EasyUI（`.panel-tool-close`）；內部欄位混用 |
| Panel — VC 操作按鈕 | Syncfusion | `data-field-id="r_PMS0210025_xxxx_open"` |
| Panel — OC 住客功能列 | Syncfusion | `data-field-id="openXxxDialog"` / `r_1050` 等 |
| Panel — OC 住客 Grid | EasyUI DataGrid | `datagrid-row-index`、欄位用 `@field` |
| Panel — OC 住客 Grid 操作 icon | Syncfusion + 標準 HTML | `data-field-id="editGuest"` / `addGuest` / `appendSingleRow` |
| Panel — 清掃人員/房間特色 | jQuery EasyUI | `_easyui_textbox_input2~5`（VC）/ `8~9`（OC） |
| Panel — 大人/小孩 | Syncfusion | `numerictextbox_0/1`（VC）/ `2/3`（OC） |
| Panel — OC 入退房資訊 | Syncfusion | `data-field-id="ci_dat"` 等 |

## 元素清單

### 搜尋區

| 元素 | 類型 | Locator | 備註 |
|------|------|---------|------|
| 房型 | select | `//div[@data-field-id='room_cod']//input` | Syncfusion DropDownList |
| 勿擾 | select | `//div[@data-field-id='dnd_cod']//input` | Syncfusion DropDownList |
| 訂房卡號 | input | `//div[@data-field-id='ikey']//input` | |
| 住客姓名 | input | `//div[@data-field-id='alt_nam']//input` | |
| 房號 | input | `//div[@data-field-id='room_nos']//input` | |
| 關聯單號 | input | `//div[@data-field-id='link_nos']//input` | |
| 公帳號 | input | `//div[@data-field-id='master_nos']//input` | |
| 棟別 | select | `//div[@data-field-id='build_nos']//input` | 第二排，預設收合 |
| 房間特色 | select | `//div[@data-field-id='character_rmk']//input` | 第二排 |
| 排房狀況 | select | `//div[@data-field-id='assign_sta']//input` | 第二排 |
| 車號 | input | `//div[@data-field-id='car_nos']//input` | 第二排 |
| 可入住天數 | select | `//div[@data-field-id='walkin_days']//input` | 第二排 |
| 拆併床 | select | `//div[@data-field-id='bed_sta']//input` | 第二排 |
| 訂房公司 | input | `//div[@data-field-id='acust_cod']//input` | **EasyUI combogrid**，不能直接 type |
| 搜尋 | button | `//button[@data-field-id='PMS0210020_doSearch']` | 帶程式代碼前綴 |
| 清除 | button | `//button[@data-field-id='PMS0210020_doClear']` | |
| 展開/收合 | button | `//button[@data-field-id='PMS0210020_toggle']` | 切換第二排顯示 |

**參數化**：`//div[@data-field-id='%s']//input`（適用所有 Syncfusion 搜尋欄位）

### 工具列

| 元素 | 類型 | Locator | 備註 |
|------|------|---------|------|
| 大圖示切換 | button | `//button[normalize-space()='大圖示']` | |
| 房控連線 | button | `//button[normalize-space()='房控連線']` | |
| 注意事項 | button | `//button[normalize-space()='注意事項']` | |
| 狀態計數 | button | `//button[contains(normalize-space(),'%s:')]` | 參數傳狀態碼（OC/VC/...），按鈕結構為 `<button><span/><label>OC: 25</label></button>`，數字是動態值 |

### 樓層篩選

| 元素 | 類型 | Locator | 備註 |
|------|------|---------|------|
| 樓層項目 | li | `//li[contains(@class,'tab-menu-item') and normalize-space()='%s']` | ALL/NF/1F~20F/111F/222F |

### 房間卡片區

| 元素 | 類型 | Locator | 備註 |
|------|------|---------|------|
| 卡片容器 | div | `//div[@class='card-wrap']` | 包含所有卡片 |
| 單一卡片 | div | `//div[@class='card--room']` | 72 張/頁（實際數量視篩選） |
| 房號 | span + h4 | `//span[@class='card-title' and normalize-space()='%s']` 或 `//h4[contains(@class,'card-title') and normalize-space()='%s']` | 參數化，兩者都有 `card-title` class（實測 h4 和 span 各 7 個，2026-05-21 確認） |
| 分頁器 | — | 底部 `1 2 3 ... 31 >` | 共 31 頁 |

**卡片邊框顏色對照**（由 border style 判斷房態）：

| 顏色 | RGB | 推測狀態 |
|------|-----|---------|
| 亮綠 | `rgb(53, 251, 14)` | VC（Vacant Clean） |
| 淡藍 | `rgb(166, 213, 237)` | OC（Occupied） |
| 青色 | `rgb(0, 255, 217)` | OOO / DSU |
| 粉紅 | `rgb(253, 148, 255)` | S（特殊狀態） |

### 房間細節 Panel — 共用欄位

| 元素 | 類型 | Locator | 備註 |
|------|------|---------|------|
| 拆併床 | button | `//button[@data-field-id='openMergeBedDialog']` | |
| 清掃房間 | button | `//button[@data-field-id='openCleanRoomDialog']` | |
| 房號（顯示） | input | `//div[@data-field-id='room_nos']//input` | DISABLED |
| 清掃人員 | select | `//div[@data-field-id='clean_cod']//input` | **EasyUI** textbox，DISABLED |
| 瑕疵原因 | textarea | `//div[@data-field-id='osreson_rmk']//textarea` | DISABLED |
| 房間特色 | select | `//div[@data-field-id='character_rmk']//input` | **EasyUI** textbox |
| 注意事項 | textarea | `//div[@data-field-id='notice_rmk']//textarea` | DISABLED，有展開按鈕 |
| 訂房公司 | input | `//div[@data-field-id='acust_nam']//input` | DISABLED |
| 大人 | input | `//div[@data-field-id='adult_qnt']//input` | Syncfusion numerictextbox |
| 小孩 | input | `//div[@data-field-id='child_qnt']//input` | Syncfusion numerictextbox |
| 公帳號 | input | `//div[@data-field-id='master_nos']//input` | DISABLED |
| 訂房來源 | select | `//div[@data-field-id='source_typ']//input` | **EasyUI** textbox |
| 市場類別 | select | `//div[@data-field-id='guest_typ']//input` | **EasyUI** textbox |
| 訂房備註 | input | `//div[@data-field-id='order_rmk']//input` | DISABLED |
| 注意事項展開 | button | `//div[@data-field-id='open_notice_rmk']//button` | DISABLED |
| 訂房備註展開 | button | `//div[@data-field-id='open_order_rmk']//button` | DISABLED |
| 關閉 | a | `//a[contains(@class,'panel-tool-close')]` | scan 盲區，EasyUI `<a>` 元素 |

### 房間細節 Panel — VC 空房專屬

| 元素 | 類型 | Locator | 備註 |
|------|------|---------|------|
| Walk In | button | `//button[@data-field-id='r_PMS0210025_1010_open']` | 子程式前綴，開「櫃台入住」dialog |
| Day use | button | `//button[@data-field-id='r_PMS0210025_1020_open']` | 子程式前綴，開同一個「櫃台入住」dialog（days DISABLED） |

### 房間細節 Panel — OC 住客專屬

#### 住客功能列（兩排按鈕）

| 元素 | 類型 | Locator | 備註 |
|------|------|---------|------|
| 訂房卡 | button | `//button[@data-field-id='openBookingCard']` | |
| 關聯單號 | button | `//button[@data-field-id='open_Link_nos_table']` | |
| 指定訂金 | button | `//button[@data-field-id='designationDeposit']` | |
| 改退房日 | button | `//button[@data-field-id='r_1050']` | |
| 改房價 | button | `//button[@data-field-id='openChangeRate']` | |
| 換房 | button | `//button[@data-field-id='openChangeRoomDialog']` | |
| 預計退房時間 | button | `//button[@data-field-id='openLateCODialog']` | |
| 櫃台備品 | button | `//button[@data-field-id='openGoodDialog']` | id=PMS02100201110 |
| 交換機 | button | `//button[@data-field-id='openPBXDialog']` | |
| 製卡 | button | `//button[@data-field-id='openCardDialog']` | |
| 取消公帳號 | button | `//button[@data-field-id='assignMasterNos']` | |
| 住房掛帳 | button | `//button[normalize-space()='住房掛帳']` | 無 data-field-id |
| 編輯模式 | button | `//button[@data-field-id='doChangeMode']` | 筆形 icon，右上角 |
| 移除住客 | button | `//button[@data-field-id='removeSingleRow']` | DISABLED |

**參數化**：`//button[@data-field-id='%s']`（適用所有住客功能按鈕）

#### 住客 Grid

**表頭操作**：

| 元素 | 類型 | Locator | 備註 |
|------|------|---------|------|
| 新增住客行 | span | `//span[@data-field-id='appendSingleRow']` | 表頭 `+` icon |
| 開啟訂房 dialog | span | `//span[@data-field-id='open_PMS0210010_dialog']` | 表頭 `...` icon |

**行內操作欄位**（每行住客一組，外層 `<td>` 的 data-field-id 是欄位名，內層子元素的 data-field-id 是操作類型）：

| 欄位名 | td data-field-id | 內層元素 | 內層 data-field-id | 定位方式 |
|--------|-----------------|---------|-------------------|---------|
| 住客姓名 | `alt_nam` | input | — | `//td[@data-field-id='alt_nam']//input` |
| 預授權 | `precredit_amt` | label | `openPreauth` | `//td[@data-field-id='precredit_amt']` |
| 餘額 | `unpaid_amt` | label | `cashierGstLedger_Single` | `//td[@data-field-id='unpaid_amt']` |
| Note | `notes` | i | `editGuest` | `//td[@data-field-id='notes']` |
| 交辦 | `todo_list` | span | `addGuest` | `//td[@data-field-id='todo_list']` |
| 提醒 | `reminder` | span | `addGuest` | `//td[@data-field-id='reminder']` |
| 留言 | `message` | i | `editGuest` | `//td[@data-field-id='message']` |
| 失物 | `lost` | i | `editGuest` | `//td[@data-field-id='lost']` |
| 接送 | `transfer` | span | `addGuest` | `//td[@data-field-id='transfer']` |
| No Info | `no_info` | — | — | `//td[@data-field-id='no_info']` |
| 房租 | `rent_amt` | — | — | `//td[@data-field-id='rent_amt']` |
| 服務費 | `serv_amt` | — | — | `//td[@data-field-id='serv_amt']` |
| 住客備註 | `fo_remark` | input (Element UI) | — | `//td[@data-field-id='fo_remark']//input`（`el-input__inner`，編輯模式 ENABLED） |
| 車號 | — | span + input (Element UI) | `openCarNosDialog` | `//span[@data-field-id='openCarNosDialog']`（span）/ `//td` 內 `el-input`（顯示值） |

**參數化**：`//td[@data-field-id='%s']`（適用行內操作欄位，比內層 addGuest/editGuest 穩定且唯一）

**注意**：內層 `addGuest` 出現在交辦/提醒/接送等多欄，`editGuest` 出現在 Note/留言/失物等多欄。直接用內層 data-field-id 定位會命中多個元素，**必須用外層 `<td>` 的 data-field-id 來區分欄位**。

**Grid 顯示欄位**（EasyUI DataGrid，用 `@field` 定位）：

| 欄位 | field | 說明 |
|------|-------|------|
| 姓名 | `alt_nam` | |
| 狀態 | `cust_sta` | |
| 證件號碼 | `id_cod` | |
| 生日 | `birth_dat` | |
| 公司名稱 | `comp_nam` | |
| 行動電話 | `mobile_nos` | |
| 住家電話 | `home_tel` | |
| 來訪次數 | `visit_nos` | |

#### 入退房資訊（OC 才顯示）

| 元素 | 類型 | Locator | 備註 |
|------|------|---------|------|
| 住客姓名 | input | `//div[@data-field-id='alt_nam']//input` | **EasyUI**，DISABLED（Panel 內） |
| No Info | select | `//div[@data-field-id='no_info']//input` | **EasyUI**，DISABLED |
| 房租 | input | `//div[@data-field-id='rent_amt']//input` | DISABLED |
| 服務費 | input | `//div[@data-field-id='serv_amt']//input` | DISABLED |
| CI 日期 | input | `//div[@data-field-id='ci_dat']//input` | DISABLED |
| CI 人員 | input | `//div[@data-field-id='ci_usr']//input` | DISABLED |
| 預計退房日 | input | `//div[@data-field-id='aco_dat']//input` | DISABLED |
| CO 人員 | input | `//div[@data-field-id='co_usr']//input` | DISABLED |
| 系統 CI 日期 | input | `//div[@data-field-id='aci_sys_dat']//input` | DISABLED |
| 系統 CO 日期 | input | `//div[@data-field-id='aco_sys_dat']//input` | DISABLED |

## 操作備註

### 房間卡片（scan 盲區）
- 房間卡片是 Vue 自訂元件（`.card--room`），**scan 不會列出**。需用 `//span[@class='card-title' and normalize-space()='房號']` 或 JS `document.querySelectorAll('.card--room')` 操作。
- 點擊卡片用 JS fallback（`Clicked (JS)` 表示普通 click 失敗）。

### Syncfusion dialog 內的 data-field-id
- Syncfusion dialog 內元素的 `data-field-id` 掛在外層 `<div>` wrapper 上，不在 `<textarea>` / `<button>` / `<input>` 本身。定位時用 `//div[@data-field-id='xxx']//textarea` 而非 `//textarea[@data-field-id='xxx']`。
- 已確認適用：車號 dialog（`carNos`、`confirmButton`）

### EasyUI 行為
- **Panel 關閉是 `<a>` 元素**：`//a[contains(@class,'panel-tool-close')]`，scan 主掃描不會抓到，`scan -a` 或 Clickable 區段才會出現。
- **EasyUI combobox / textbox**：搜尋區的「訂房公司」和 Panel 內的清掃人員/房間特色/訂房來源/市場類別都是 EasyUI，不能用 `type` 直接設值，需用 combogrid 流程（click 展開 → 搜尋 → 選取）。

### 按鈕前綴
- 搜尋區三個按鈕帶程式代碼前綴：`PMS0210020_doSearch`、`PMS0210020_doClear`、`PMS0210020_toggle`。
- VC Panel 操作按鈕帶子程式前綴：`r_PMS0210025_1010_open`（Walk In）、`r_PMS0210025_1020_open`（Day use）。
- OC Panel 住客功能按鈕多為 `openXxxDialog` 命名，僅 `r_1050`（改退房日）帶子程式前綴。

### Panel 狀態變異（VC vs OC）
- **VC（空房）**：顯示 Walk In / Day use 按鈕，無住客 Grid，欄位大多空白。
- **OC（住客）**：Walk In / Day use 消失，改為 14 個住客功能按鈕（兩排）+ 住客 Grid + 入退房資訊。拆併床/清掃房間兩個按鈕在兩種狀態下都有。
- **住客 Grid 行內操作**：每行住客有 editGuest（編輯 icon）、addGuest（新增 icon）、預授權/餘額（可點擊 label），以及交辦/提醒/留言/失物/接送等功能 icon（`✓` = 已有資料、`+` = 新增）。
- **Grid icon 重複實例**：editGuest / addGuest 在 DOM 中各出現 3 次（1 guest 時），定位特定行需結合 `datagrid-row-index`。
- **入退房資訊需捲動**：ci_dat / ci_usr / aco_dat 等欄位在 Panel 下方，需捲動才能看到，但 scan 可抓到（掃描整個 DOM）。
- **EasyUI ID 偏移**：同一個 `data-field-id` 在 VC 和 OC 下的 EasyUI textbox input ID 不同（如 clean_cod 在 VC 是 `_easyui_textbox_input2`，在 OC 是 `_easyui_textbox_input8`），使用 `data-field-id` locator 較穩定。

### 樓層篩選
- 左側樓層列表是 `li.tab-menu-item`，非標準按鈕或連結，scan 不會掃到。

### 房態顏色
- 卡片邊框顏色在**內層 `<div>` 的 inline style**（非外層 `.card--room`）：`border: 4px solid rgb(...)`
- 結構：`.card--room > div[style*="border"]`
- 需 JS 讀取判斷房態
- ⚠️ 實測發現有顏色為 OC（rgb 166,213,237）但 Panel 開啟後顯示 VC 行為的情況，可能是卡片渲染與後端狀態不同步

---

## 深度探索（2026-05-16）

### 編輯模式（doChangeMode）

點擊筆形按鈕進入編輯模式：

| 變化 | 說明 |
|------|------|
| `doChangeMode` → `doSave` | 筆形按鈕消失，出現儲存按鈕（`data-field-id="doSave"`） |
| 14 個功能按鈕 + 住房掛帳 → DISABLED | 編輯模式下所有住客功能按鈕不可點 |
| `open_notice_rmk`、`open_order_rmk` → ENABLED | 注意事項/訂房備註展開按鈕可用 |
| `guest_typ` → 可編輯 | EasyUI textbox 解鎖 |
| `source_typ` → **狀態依賴** | 有些房 ENABLED、有些仍 DISABLED（可能與訂房來源是否已設定有關） |
| `fo_remark`、`no_info`、`alt_nam`（Panel 內） → 可編輯 | alt_nam 出現新 EasyUI textbox |
| 新出現 `roomDetailGrid` input | Grid 搜尋欄位 |
| `openPreauth`、`cashierGstLedger_Single` → GONE | Grid label 消失 |
| **openCarNosDialog → 可操作** | 一般模式無效，編輯模式開「車號」Syncfusion dialog |
| **Grid icon 行為變化** | message/lost 從 `editGuest`(i) 變為 `addGuest`(span)，notes 不變 |
| Escape 無效 | 不能用 Escape 退出編輯模式 |
| **關閉 Panel = 取消** | 關閉 Panel 不會跳確認儲存，直接丟棄變更 |

**編輯模式可操作項目**（完整清單）：

| 操作 | 類型 | 結果 |
|------|------|------|
| `open_notice_rmk` | 展開按鈕 | 開「注意事項」EasyUI panel：`noticeContent` textarea + `doSaveNoticeRmk` 確定 + close |
| `open_order_rmk` | 展開按鈕 | 開「訂房備註」EasyUI panel：textarea + 確定 + close |
| `openCarNosDialog` | Grid span | 開「車號」Syncfusion dialog：`//div[@data-field-id='carNos']//textarea` + `//div[@data-field-id='confirmButton']//button` + `//button[@title='關閉']` |
| `fo_remark` | input (Element UI) | 直接編輯住客備註（Grid 內，`//td[@data-field-id='fo_remark']//input`，UI 顯示名稱「住客備註」） |
| `no_info` | EasyUI select | 直接編輯 No Info |
| `alt_nam`（Panel 內） | EasyUI input | 直接編輯住客姓名 |
| `guest_typ` | EasyUI select | 直接編輯市場類別 |
| `adult_qnt` / `child_qnt` | numeric | 直接編輯大人/小孩數（一般模式也可） |
| `roomDetailGrid` | search input | Grid 搜尋欄位 |
| `doSave` | button | 儲存變更 |
| 關閉 Panel | panel-tool-close | 丟棄全部變更 |

**編輯模式下 Grid 操作**：

| 操作 | 編輯模式行為 | 備註 |
|------|------------|------|
| `appendSingleRow`（+） | ✅ 新增空白住客行 | diff 偵測不到（DataGrid 行級變化非 diff 追蹤範圍） |
| `removeSingleRow`（-） | ✅ 移除住客行 | 新增行出現後 ENABLED（一般模式 DISABLED） |
| notes / todo_list / message / lost / transfer | ❌ click 無效 | scan 顯示 clickable 但 diff 確認零變化 |
| `open_PMS0210010_dialog` | ❌ click 無效 | |

**diff 偵測能力**：已修正 — diff 現在追蹤 total table row count，appendSingleRow 新增行可偵測（`total grid 15 → 18 (+3)`）。也追蹤 clickable 元素的 parent td context（如 `label:openPreauth (in precredit_amt)`）。

### OC 功能按鈕 Dialog 結構

#### 訂房卡（openBookingCard）→ Syncfusion dialog

**巨型子系統**，157 元素 + 64 grid columns。純 Syncfusion。

**佈局**：
```
訂房卡 Dialog
├── [標題] — 館別 + 訂房卡號
├── [Tabs] — 彙總 / 明細 / Profile Notes
├── [工具列] — 12 個動作按鈕
│   ├── 排房 (doOpenRoomAssignDialog)
│   ├── 訂房確認書 (doOpenReportDialog)
│   ├── 檢視 R 卡 (doOpenImageRcardPrintDialog)
│   ├── 訂房明細 (doOpenDtDetailDialog)
│   ├── 簡訊 (doOpenSMSDialog)
│   ├── E-mail (doOpenEmailDialog)
│   ├── 分帳規則 (doOpenSubAccountDialog)
│   ├── 旅客登記卡 (doOpenReportRcard)
│   ├── Pre-CheckIn (doOpenPreCheckIn)
│   ├── 備品批次 (doOpenBatchSpareInsert)
│   ├── 線上繳款單 (doOpenPayFolioDialog)
│   └── 儲存/另存/複製/變更記錄 (save/saveAndCreate/copy/doOpenChangeLogDialog)
├── [客戶資訊] — altName, acustCode, saluteCode, statusCode, vipStatus, groupNos...
├── [聯絡資訊] — mobileNos, email, officeTel, attenName
├── [訂房設定] — fixedOrder, isPrtrent, telTce, dndCode, confirmStatus, masterStatus, preCi (checkboxes)
├── [費用摘要] — sumRentTotal, sumServTotal, sumOtherTotal, sumAddExtraTotal, generalTotal, orderDeposit, banlanceAmount
├── [明細 Grid] — 64 columns（orderStatus/ciDate/days/coDate/rateCode/useCode/roomCode/roomNos/guestName...）
│   └── 每行有 Edit / Delete 按鈕
├── [彈窗按鈕 "..."] — altNameBtn, acustCodeBtn, attenName, officeTel, orderRemark, linkNosDialog, roomStatusDialog, masterNosDialog, guideDialog, ptvDialog, focDialog, banlanceAmount
└── [關閉] — `//button[@title='關閉']`
```

**Tab 結構差異**（2026-05-16 補掃）：

| Tab | 切換 Locator | Buttons | Textareas | Interactive Roles | 特徵 |
|-----|-------------|---------|-----------|-------------------|------|
| 彙總 | `//div[@id='tab-Summary']` | 29 | 3 | 28 | Grid 顯示匯總（groupRentTotal 等），有 Edit/Delete |
| 明細 | `//div[@id='tab-Detail']` | 29 | 5 | 38 | Grid 顯示逐筆（roomNos/guestName/ciDate），有 Edit/Delete |
| Profile Notes | `//div[@id='tab-Profile']` | 27 | 2 | 13 | 最精簡，Grid 僅 altName + requestRemark，無 Edit/Delete |

三 tab 共用：toolbar（12 按鈕）、header 欄位（31 inputs）、64 grid columns 定義、關閉按鈕。

**關鍵欄位**（大部分 DISABLED）：
- `altName` span — 住客姓名（可點擊帶 altNameBtn 瀏覽按鈕）
- `acustCode` span — 訂房公司
- `orderRemark` textarea — 訂房備註（ENABLED）
- `attenName` input — 接洽人（ENABLED）
- `orderStatus` span — 訂單狀態（如「今日到達」）

#### 關聯單號（open_Link_nos_table）→ EasyUI panel

簡單 panel，5 元素：
- 關聯單號 input（DISABLED）
- 相關房號 button
- save button
- `sub-button--add` span（新增）
- panel-tool-close

#### 指定訂金（designationDeposit）→ 觸發「開班」前置

不是直接開訂金 dialog，而是**出納開班前置條件** — 子程式 `PMS0310060`：
- `shop_dat`（營業日期，DISABLED）
- `rspt_cod`（收款站點）
- `open_man`（開班人員，DISABLED）
- `shift_cod`（班別）
- `s99_user.usr_pwd`（密碼）
- 確認按鈕 `PMS0310060_r_1011`

#### 改退房日（r_1050）→ EasyUI panel + Syncfusion 混合

15 元素 + 5 grid columns：
- `new_co_dat`（新退房日，date picker）
- `filter` radio 二選一：ROOM（單一房號）/ IKEY（訂房卡全部房號）
- Grid 列出受影響房間（room_nos / alt_nam / ci_dat / eco_dat + ck checkbox）
- save button

#### 改房價（openChangeRate）→ EasyUI panel + Syncfusion

29 元素 + 12 grid columns。需在房租**尚未入帳**時才能操作（已入帳會跳 Alert 阻擋）。

**欄位**：

| 元素 | 類型 | Locator | 狀態 | 備註 |
|------|------|---------|------|------|
| 住客姓名 | input | `//div[@data-field-id='alt_nam']//input` | DISABLED | 顯示用 |
| 核准人 | input | `//div[@data-field-id='disc_usr']//input` | ENABLED | |
| 原因 | input | `//div[@data-field-id='reason_rmk']//input` | ENABLED | |
| 房價名稱 | input | `//div[@data-field-id='ratecod_nam']//input` | DISABLED | 帶瀏覽按鈕 |
| 計價房型名稱 | input | `//div[@data-field-id='usecod_nam']//input` | DISABLED | |
| 原加價費 | input | `//div[@data-field-id='oadd_extra_fee']//input` | DISABLED | EasyUI |
| 房價代碼 | input | `//div[@data-field-id='rate_cod']//input` | DISABLED | EasyUI |
| 新計價房型 | input | `//div[@data-field-id='use_cod']//input` | ENABLED | EasyUI |
| 新加價費 | input | `//div[@data-field-id='add_extra_fee']//input` | ENABLED | EasyUI |
| 訂房來源名 | input | `//div[@data-field-id='source_nam']//input` | DISABLED | |
| 市場類別名 | input | `//div[@data-field-id='guest_sna']//input` | DISABLED | |
| 訂房來源 | input | `//div[@data-field-id='source_typ']//input` | DISABLED | EasyUI |
| 市場類別 | input | `//div[@data-field-id='guest_typ']//input` | ENABLED | EasyUI |

**功能按鈕**：

| 按鈕 | Locator | 備註 |
|------|---------|------|
| 以下同價 | `//button[normalize-space()='以下同價']` | 批次套用到後續日期 |
| 儲存 | 第 2 個 button（無特徵） | |
| 房價瀏覽 | `//div[@data-field-id='ratecod_nam_button']//button` | |

**Grid**（12 columns）：batch_dat / order_rat / rate_cod / use_cod / rent_amt / serv_amt / add_extra_amt / add_on_amt / other_rent_amt / other_serv_amt / source_typ / guest_typ

**關閉**：`(//a[contains(@class,'panel-tool-close')])[last()]`

#### 換房（openChangeRoomDialog）→ EasyUI panel

7 元素：
- `room_nos` input（新房號）
- 2 個 EasyUI textbox（DISABLED）
- textarea（換房備註）
- save button + close

#### 預計退房時間（openLateCODialog）→ EasyUI panel + Syncfusion

12 元素：
- `doSave` button
- 3 個 date/time input（2 DISABLED + 1 可編輯的退房時間）
- EasyUI textbox
- textarea（備註）
- `upd_dat`/`upd_usr`（異動紀錄，DISABLED）

#### 清掃房間（openCleanRoomDialog）→ EasyUI panel

6 元素，非常簡單：
- 2 個 input（DISABLED）
- 3 個 button（1 DISABLED）
- close link

#### 拆併床（openMergeBedDialog）→ **Syncfusion dialog**（非 EasyUI）

21 元素 + 4 grid columns：
- 3 個 dropdown（房型/床型相關）
- 1 個 text input
- Grid：roomCodeName / floorNumber / roomNumber / bedStatus
- checkbox（全選/單選）
- textarea
- **關閉方式**：`//button[@title='關閉']`（不是 panel-tool-close）

#### 櫃台備品（openGoodDialog）→ EasyUI panel

23 元素 + 19 grid columns：
- 庫存查詢 button
- Grid 欄位豐富：itemCode / rentalStartDate / checkoutDate / amount / appraiseIns / todoInsert / todoDeptCode / appraiseUnitAmount / appraiseItemAmount / serialId / creator / createTime...
- 副 Grid：date / itemTotal / usageAmount / inventory
- id=`PMS02100201110`（子程式代碼）

#### 交換機（openPBXDialog）→ EasyUI panel + Syncfusion

25 元素 + 9 grid columns：
- 5 個功能按鈕：設置晨呼 / 關閉電話 / 設定限撥 / 設定勿擾 / 語言設定
- 欄位：`room_mn.room_nos`、`lang_cod`、`room_mn.ci_dat`、`room_mn.co_dat`、`mcall_dat`、`mcall_tim`
- Grid：mcall_dat / mcall_tim / trans_pbx_sta / mcall_sta / ins_dat / ins_usr / upd_dat / upd_usr

#### 製卡（openCardDialog）→ EasyUI panel + Syncfusion

26 元素 + 11 grid columns：
- 3 個功能按鈕：新卡 / 複製卡 / 讀卡
- 欄位：room_nos / adult_qnt / order_eco_tim / room_eco_tim / eco_tim / default_make_card_quantity
- Grid：ikey / room_nos / guest_nam / action_rmk / begin_dat / end_dat / mifare_nos / ins_dat

#### 取消公帳號 / 指定公帳號（assignMasterNos）→ **Syncfusion dialog**（toggle 按鈕）

**行為依狀態切換**：
- 有公帳號時 → 按鈕文字「取消公帳號」→ Alert 確認 → 直接執行取消（⚠️ 破壞性操作）
- 無公帳號時 → 按鈕文字「指定公帳號」→ 開 Syncfusion dialog

指定公帳號 dialog，8 元素：
- `filterOption` radio（篩選選項）
- `masterNos` input + 瀏覽 span
- `masterNosIkey` input
- `custNam` input
- `saveButton`
- **關閉方式**：`//button[@title='關閉']`

#### 住房掛帳 → **Syncfusion dialog**

3 元素，極簡：
- `chargeInFolio` span（是/否 toggle）
- `saveButton`
- **關閉方式**：`//button[@title='關閉']`

### Grid 行內操作 Dialog

| 操作 | 點擊元素 | 結果 |
|------|---------|------|
| Note | `//td[@data-field-id='notes']//i` | 開「Profile Notes」EasyUI panel（5 ���素：textarea + 儲存 + add/remove span + close） |
| 交辦 | `//td[@data-field-id='todo_list']//span` | 開「交辦事項編輯」EasyUI panel（22 元素） |
| 預授權 | `//td[@data-field-id='precredit_amt']//label` | 開「預授權」EasyUI panel（16 元素 + 11 grid columns） |
| 餘額 | `//td[@data-field-id='unpaid_amt']//label` | 觸發「開班」前置（同指定訂金） |
| 接送 | `//td[@data-field-id='transfer']` | 開「接送服務編輯」EasyUI panel（45 元素 + 6 grid columns） |
| 車號 | `//span[@data-field-id='openCarNosDialog']` | 一般模式無效果，**編輯模式下**開 Syncfusion dialog |

**交辦事項編輯 Dialog**：
- room_nos / ikey / alt_nam（DISABLED 顯示欄位）
- status_rmk / key_nos / begin_dat / end_dat / proc_sta / dept_cod（操作欄位）
- todo_rmk textarea
- open_order_card / search_todo_rmk 按鈕
- ins_dat / ins_usr / upd_dat / upd_usr（異動紀錄）

**預授權 Dialog**：
- roomNos / altNam（顯示）
- Grid 11 columns：precreditDat / payWay / creditNos / expiraDat / preauthCod / precreditAmt / insDat / insUsr / updDat / updUsr

#### 接送服務編輯（transfer）→ EasyUI panel + Syncfusion 混合

45 元素 + 6 grid columns。框架：EasyUI(2) + Syncfusion(35)。

**操作欄位**：

| 元素 | 類型 | Locator | 狀態 | 備註 |
|------|------|---------|------|------|
| 接/送 | EasyUI combobox | `//div[@data-field-id='pickup_typ']//input` | ENABLED | 選項：`A : 接`、`L : 送` |
| 日期 | date | `//div[@data-field-id='schedule_dat']//input` | ENABLED | 有日曆 icon（`//i`） |
| 時間 | time | `//div[@data-field-id='schedule_tim']//input` | ENABLED | 有時間 icon（`//i`） |
| 費用 | numeric | `//div[@data-field-id='appraise_amt']//input` | ENABLED | `numerictextbox_10` |
| 班次 | input | `//div[@data-field-id='schedule_nos']//input` | ENABLED | 有瀏覽按鈕（`schedule_nos_button`） |
| 車種 | EasyUI combobox | `//div[@data-field-id='car_typ']//input` | ENABLED | |
| 地點 | input | `//div[@data-field-id='spot']//input` | ENABLED | |
| 公司 | input | `//div[@data-field-id='cust_nam']//input` | ENABLED | |
| 連絡人 | input | `//div[@data-field-id='atten_nam']//input` | ENABLED | |
| 電話 | input | `//div[@data-field-id='tel1_nos']//input` | ENABLED | |
| 大人 | numeric | `//div[@data-field-id='adult_qnt']//input` | ENABLED | |
| 小孩 | numeric | `//div[@data-field-id='child_qnt']//input` | ENABLED | |
| 備註 | input | `//div[@data-field-id='remark1']//input` | ENABLED | |
| 指定住客序號 | numeric | `//div[@data-field-id='ikey_seq_nos']//input` | ENABLED | |

**顯示欄位**（DISABLED）：

| 元素 | 類型 | Locator | 備註 |
|------|------|---------|------|
| 指定住客 | EasyUI textbox | `//div[@data-field-id='ci_ser']//input` | |
| 住客帳狀態 | EasyUI textbox | `//div[@data-field-id='guest_sta']//input` | |
| VIP | EasyUI textbox | `//div[@data-field-id='vip_sta']//input` | |
| 房號 | input | `//div[@data-field-id='room_nos']//input` | |
| 訂房卡號 | input | `//div[@data-field-id='ikey']//input` | |
| 入住日期 | date | `//div[@data-field-id='ci_dat']//input` | |
| 退房日期 | date | `//div[@data-field-id='co_dat']//input` | |
| 新增日期 | date | `//div[@data-field-id='ins_dat']//input` | |
| 新增者 | input | `//div[@data-field-id='ins_usr']//input` | |
| 修改日期 | date | `//div[@data-field-id='upd_dat']//input` | |
| 修改者 | input | `//div[@data-field-id='upd_usr']//input` | |

**功能按鈕**：

| 按鈕 | Locator | 備註 |
|------|---------|------|
| 批次新增 | `//button[normalize-space()='批次新增']` | 📌 未展開（不確定開什麼 dialog） |
| 簡訊 | `//button[normalize-space()='簡訊']` | DISABLED，📌 未驗互動 |
| 儲存 | `(//button[child::img[@alt='save']])[last()]` | ✅ 已驗（儲存成功 Alert） |
| 新增 | `(//button[child::img[@alt='add']])[last()]` | ✅ 已驗（清空表單 + ENABLE pickup_typ） |

**Grid**（EasyUI DataGrid，6 columns）：pickup_typ / schedule_dat / schedule_nos / schedule_tim / car_nam / spot

**住客 Grid**（EasyUI DataGrid）：姓名 / 住客帳狀態 / 訂房卡號 / 序號 / 房號 / 入住日期 / 退房日期

**關閉**：`(//a[contains(@class,'panel-tool-close')])[last()]`

**操作備註**：
- 選擇接/送時，日期會自動切換（接 = 入住日、送 = 退房日）
- `appraise_amt`、`adult_qnt`、`child_qnt` 是 Syncfusion NumericTextBox，CLI type（send_keys）不更新 value。測試程式碼用 `set_transport_service(fee='100')` 設值，需確認底層實作
- 自動入帳 checkbox（Element UI）：已入住房間測試時，接/送兩種模式下都是 `is-disabled`，無法勾選。啟用條件不明（可能與滾房租日期或入住狀態有關）
- 編輯模式下開此 dialog 後，房間細節 Panel 的 `panel-tool-close[last()]` 會變 0x0，需用 `[1]` 關閉

**⚠️ 既有程式碼用 label-based locator**（`//label[normalize-space()='%s']/following-sibling::div//input`），但 scan 結果顯示此 dialog 有完整的 `data-field-id`。label-based locator 可能是早期寫的，data-field-id 版本更穩定。

### 工具列

| 按鈕 | 點擊結果 | 備註 |
|------|---------|------|
| 大圖示 | 切換卡片大小，Table rows 52→3 | toggle 按鈕，再點恢復 |
| 注意事項 | 無可見 dialog 開啟 | scan -d 抓到的是底層 OC Panel，非新 dialog |
| 房控連線 | 無可見 dialog 開啟 | 同上 |

### Dialog 關閉方式彙整

| 類型 | 關閉方式 | 適用 dialog |
|------|---------|------------|
| EasyUI Panel | `(//a[contains(@class,'panel-tool-close')])[last()]` | 關聯單號、改退房日、換房、預計退房時間、清掃房間、櫃台備品、交換機、製卡、開班、交辦、**櫃台入住（Walk In/Day use）**、Profile Notes |
| Syncfusion Dialog | `//button[@title='關閉']` | 訂房卡、拆併床、指定公帳號、住房掛帳、**車號（編輯模式）** |
| 出納前置（開班） | 同 EasyUI Panel | 指定訂金、餘額 |

### 出納前置（開班 PMS0310060）

以下操作都會先觸發「開班」dialog，需要先完成出納開班才能繼續：
- 指定訂金（designationDeposit）
- 餘額 Grid label（cashierGstLedger_Single）

### 已知問題

- ~~`改房價`~~ 已解：EasyUI panel + Syncfusion，29 元素 + 12 grid columns（需房租未入帳）
- ~~`Note`~~ 已解：開「Profile Notes」EasyUI panel（textarea + add/remove + save）
- ~~`車號`~~ 已解：一般模式無效果，**編輯模式下**開 Syncfusion dialog（carNos textarea + hidden input + confirmButton）。`get_car_nos()` 讀 hidden input 取值
- `注意事項` / `房控連線` 工具列按鈕點擊無可見 dialog，可能是背景動作或需特定條件
- 大圖示模式下 Table rows 從 52 降到 3，分頁器顯示 0 of 0（可能是 panel 開啟導致計算異常）

### 櫃台入住（Walk In / Day use）→ EasyUI panel + Syncfusion

**共用同一個 dialog**，32 元素。子程式 `PMS0210025`。

| 元素 | 類型 | Locator | Walk In | Day use |
|------|------|---------|---------|---------|
| 住客姓名 | input | `//div[@data-field-id='alt_nam']//input` | ENABLED | ENABLED |
| 房價代碼 | input | `//div[@data-field-id='rate_cod']//input` | DISABLED | DISABLED |
| 訂房公司 | input | `//div[@data-field-id='acust_cod']//input` | ENABLED | ENABLED |
| 天數 | input | `//div[@data-field-id='days']//input` | **ENABLED** | **DISABLED** |
| 退房日 | input | `//div[@data-field-id='co_dat']//input` | DISABLED | DISABLED |
| 房型 | input | `//div[@data-field-id='use_cod']//input` | ENABLED | ENABLED |
| 行動電話 | input | `//div[@data-field-id='mobile_nos']//input` | ENABLED | ENABLED |
| 車號 | input | `//div[@data-field-id='car_nos']//input` | ENABLED | ENABLED |
| 房租合計 | input | `//div[@data-field-id='rent_tot']//input` | ENABLED | ENABLED |
| 服務費合計 | input | `//div[@data-field-id='serv_tot']//input` | ENABLED | ENABLED |
| 房型代碼 | input | `//div[@data-field-id='room_cod']//input` | DISABLED | DISABLED |
| E-mail | input | `//div[@data-field-id='e_mail']//input` | ENABLED | ENABLED |
| 大人 | input | `//div[@data-field-id='adult_qnt']//input` | ENABLED | ENABLED |
| 小孩 | input | `//div[@data-field-id='child_qnt']//input` | ENABLED | ENABLED |
| FO 備註 | input | `//div[@data-field-id='fo_remark']//input` | ENABLED | ENABLED |
| 退房備註 | input | `//div[@data-field-id='co_rmk']//input` | ENABLED | ENABLED |
| 加價費 | input | `//div[@data-field-id='add_extra_fee']//input` | ENABLED | ENABLED |
| 訂房來源 | input | `//div[@data-field-id='source_typ']//input` | DISABLED | DISABLED |
| 市場類別 | input | `//div[@data-field-id='guest_typ']//input` | DISABLED | DISABLED |
| 房租 | input | `//div[@data-field-id='rent_amt']//input` | ENABLED | ENABLED |
| 服務費 | input | `//div[@data-field-id='serv_amt']//input` | ENABLED | ENABLED |
| 其他費用 | input | `//div[@data-field-id='other_tot']//input` | ENABLED | ENABLED |
| 加價金額 | input | `//div[@data-field-id='add_extra_amt']//input` | ENABLED | ENABLED |
| 小計 | input | `//div[@data-field-id='sub_tot']//input` | ENABLED | ENABLED |

**功能按鈕**：

| 按鈕 | 狀態 | 備註 |
|------|------|------|
| 旅客登記卡 | DISABLED | 需先填寫住客資料 |
| **Check In** | ENABLED | ⚠️ 不可逆操作 |
| 製卡 | DISABLED | |
| 螢幕簽名 | DISABLED | |
| 住客姓名瀏覽 | ENABLED | `//div[@data-field-id='searchAltNam']//button` |
| 房價代碼瀏覽 | ENABLED | `//div[@data-field-id='searchRateCod']//button` |

**退房日曆**：`//div[@data-field-id='co_dat']//i`（日曆 icon，僅 Walk In 可用）

**關閉**：`(//a[contains(@class,'panel-tool-close')])[last()]`

**Walk In vs Day use 唯一差異**：`days` 欄位 enabled/disabled。Day use 固定一天所以鎖定天數。

---

## 未驗證區域（2026-05-21）

> 以下區域已記錄結構但尚未用 CLI 實測操作。標記來源：Phase C 回顧。

| 區域 | 狀態 | 備註 |
|------|------|------|
| 搜尋區欄位（type/select/search） | 📌 未驗互動 | 只用過 OC 狀態按鈕篩選 |
| 訂房卡 dialog（openBookingCard） | 📌 未驗互動 | 結構文件有記錄（157 元素），未實測 |
| 關聯單號 dialog | 📌 未驗互動 | |
| 指定訂金 / 開班前置 | 📌 未驗互動 | 需要出納開班 |
| 改退房日 dialog | 📌 未驗互動 | |
| 改房價 dialog | 📌 未驗互動 | |
| 換房 dialog | 📌 未驗互動 | |
| 預計退房時間 dialog | 📌 未驗互動 | |
| 清掃房間 dialog | 📌 未驗互動 | |
| 拆併床 dialog | 📌 未驗互動 | |
| 櫃台備品 dialog | 📌 未驗互動 | |
| 交換機 dialog | 📌 未驗互動 | |
| 製卡 dialog | 📌 未驗互動 | |
| 指定/取消公帳號 dialog | 📌 未驗互動 | |
| 住房掛帳 dialog | 📌 未驗互動 | |
| 接送 — 批次新增 | 📌 未展開 | 不確定開什麼 dialog |
| 接送 — Grid 行選取後表單更新 | 📌 未驗互動 | |
| 接送 — adult_qnt / child_qnt | 📌 未驗互動 | 預期與 appraise_amt 同為 NumericTextBox 缺口 |
| 櫃台入住（Walk In / Day use） | 📌 未驗互動 | ⚠️ 不可逆操作 |
| Note / 交辦 / 預授權 Grid 行內操作 | 📌 未驗互動 | 結構文件有記 dialog 結構 |
