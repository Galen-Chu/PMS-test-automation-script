# C/I 清單（PMS0210060）

> 路徑：接待 → C/I清單
> 程式代碼：PMS0210060
> SPA 導航：`//button[normalize-space()='接待']` → `//span[@data-field-id='PMS0210060']`

---

## 佈局

```
C/I清單(PMS0210060)
├── [搜尋區] ─ 入住日期(checkinDate)、速查(quickSearch)、住客姓名(guestName)、房號(roomNos)、網訂編號(rvreserveNos)
│   └── 查詢模式(querySets)、設定(querySetsSettingButtohn)、搜尋(searchButton)、清除(clearButton)、下拉選單(dropdownButton)
├── [操作列] ─ 入住(r_1010)、取消入住(r_1020)、訂房卡(openPMS0110041)、排房(openPMS0210030)、製卡(r_make_card)、Queue(doQueue)、匯出 Excel(excelExport)
└── [列表 Grid] ─ Syncfusion Grid，32 欄（訂房卡號、狀態、住客姓名、C/I日期...）
    └── 點選列 + 入住 → Check In Dialog
```

## 框架分布

| 區塊 | 框架 | 判斷依據 |
|------|------|---------|
| 搜尋區 | Syncfusion | `data-field-id` 屬性、DatePicker、textbox |
| 操作列 | Syncfusion | `data-field-id` 屬性、button |
| 列表 Grid | Syncfusion Grid | `.e-gridcontent .e-row`、`td[@field]` |
| Check In Dialog | Syncfusion Dialog + EasyUI + Syncfusion 混合 | dialog + EasyUI textbox(combobox) + Syncfusion NumericTextBox |

## 搜尋區

| 元素 | 類型 | Locator | 備註 |
|------|------|---------|------|
| 入住日期 | Syncfusion DatePicker | `//div[@data-field-id='checkinDate']//input` | |
| 速查 | input | `//div[@data-field-id='quickSearch']//input` | placeholder="搜尋: 訂房公司, 聯絡人, 公司名稱, 訂房卡號, 訂房名稱/團號, 網訂編號" |
| 住客姓名 | input | `//div[@data-field-id='guestName']//input` | |
| 房號 | input | `//div[@data-field-id='roomNos']//input` | |
| 網訂編號 | input | `//div[@data-field-id='rvreserveNos']//input` | |
| 查詢模式 | Syncfusion Dropdown | `//div[@data-field-id='querySets']` | 目前只有「一般模式」 |
| 設定 | button | `//div[@data-field-id='querySetsSettingButtohn']//button` | data-field-id 拼字錯誤 (Buttohn) |
| 搜尋 | button | `//div[@data-field-id='searchButton']//button` | |
| 清除 | button | `//div[@data-field-id='clearButton']//button` | |
| 下拉選單 | button | `//div[@data-field-id='dropdownButton']//button` | 展開更多篩選欄位 |

### 篩選欄位（dropdownButton 展開後）

| 元素 | data-field-id | 類型 | 預設值 | 備註 |
|------|---------------|------|--------|------|
| 住客狀態 | checkinStatus | Syncfusion DDL | N:未入住 | 選項：N:未入住 / Y:已入住 / all:全部。開啟：click `//div[@data-field-id='checkinStatus']`。選項元素：`<li>`，用 `//li[normalize-space()='%s']` 選取（非 BaseLocator 的 dropdownbase pattern） |
| 訂房卡號 | ikey | input | | |
| 訂房公司 | acustCode | input | | |
| 關聯單號 | linkNos | input | | |
| 房號 | roomCode | input | | |
| 使用房型 | useCode | input | | |
| 計價房型 | groupNos | input | | |
| 住客類型 | guestType | input | | |
| 來源 | sourceType | input | | |
| 身份識別 | identifyCode | input | | |
| 聯絡人電話 | attenPhone | input | | |

## 操作列

| 元素 | data-field-id | Locator | 備註 |
|------|---------------|---------|------|
| 入住 | r_1010 | `//div[@data-field-id='r_1010']//button` | 核心操作：開啟入住 Check In Dialog |
| 取消入住 | r_1020 | `//div[@data-field-id='r_1020']//button` | 需已入住篩選 + 選取已入住 row → 開啟取消入住 Check In Dialog |
| 訂房卡 | openPMS0110041 | `//div[@data-field-id='openPMS0110041']//button` | |
| 排房 | openPMS0210030 | `//div[@data-field-id='openPMS0210030']//button` | |
| 製卡 | r_make_card | `//div[@data-field-id='r_make_card']//button` | |
| Queue | doQueue | `//div[@data-field-id='doQueue']//button` | |
| 匯出 Excel | excelExport | `//div[@data-field-id='excelExport']//button` | |

## 列表 Grid（32 欄）

| 欄位 | field 屬性 | 中文標題 |
|------|-----------|---------|
| ikey | ikey | 訂房卡號 |
| ikeySeq | ikeySeq | 序號 |
| orderStatus | orderStatus | 狀態 |
| vip | vip | VIP |
| rvreserveNos | rvreserveNos | 網訂編號 |
| linkNos | linkNos | 關聯單號 |
| roomNos | roomNos | 房號 |
| cleanStatus | cleanStatus | 清掃狀況 |
| groupNos | groupNos | 訂房名稱/團號 |
| guestStatus | guestStatus | 住客狀態 |
| guestName | guestName | 住客姓名 |
| queueTime | queueTime | Q-Time |
| checkinDate | checkinDate | 入住日期 |
| checkoutDate | checkoutDate | 退房日期 |
| rateCodeName | rateCodeName | 房價名稱 |
| roomCode | roomCode | 使用房型 |
| useCode | useCode | 計價房型 |
| acustName | acustName | 訂房公司 |
| attenName | attenName | 聯絡人 |
| ciSer | ciSer | 住客序號 |
| assignLock | assignLock | 鎖定排房 |
| attenMobile | attenMobile | 聯絡人手機 |
| attenOfficeTel | attenOfficeTel | 聯絡人公司電話 |
| attenHomeTel | attenHomeTel | 聯絡人住家電話 |
| attenFaxNos | attenFaxNos | 聯絡人傳真 |
| attenEMail | attenEMail | 聯絡人e-mail |
| totalAmount | totalAmount | 總金額 |
| days | days | 天數 |
| adultQuantity | adultQuantity | 大人 |
| childQuantity | childQuantity | 小孩 |
| guestQuantity | guestQuantity | 總人數 |
| identifyName | identifyName | 身份識別 |

**定位**：`//td[@field='%s']`

## Check In Dialog（Syncfusion Dialog）

> 由點選 Grid 資料列 + 點擊「入住」觸發

### Dialog 表單

| 元素 | data-field-id | 類型 | 狀態 | 備註 |
|------|---------------|------|------|------|
| 訂房卡號 | ikey | input | DISABLED | |
| 網訂編號 | rvreserve_nos | input | DISABLED | |
| 訂房名稱/團號 | group_nos | input | DISABLED | |
| 訂房公司 | acust_nam | input | DISABLED | |
| 公帳號 | master_nos | input | DISABLED | |
| 公帳狀態 | master_sta | EasyUI textbox/combobox | DISABLED | |
| 訂房備註 | order_rmk | textarea | DISABLED | |
| 房租總額 | rent_tot | Syncfusion NumericTextBox | enabled | |
| 服務費總額 | serv_tot | Syncfusion NumericTextBox | enabled | |
| 其他費用總額 | other_tot | Syncfusion NumericTextBox | enabled | |
| 總金額 | total_amt | Syncfusion NumericTextBox | enabled | |

### Dialog 按鈕（未入住 tab）

⚠️ Dialog 內部按鈕的 `data-field-id` 直接在 `<button>` 上，非 wrapper `<div>`。Locator 用 `//button[@data-field-id='xxx']` 而非 `//div[@data-field-id='xxx']//button`。

| 按鈕 | data-field-id | Locator | 狀態 | 備註 |
|------|---------------|---------|------|------|
| 入住 | r_1011 | `//button[@data-field-id='r_1011']` | enabled | 執行入住 |
| C/I公帳號 | set_master_nos | `//button[@data-field-id='set_master_nos']` | DISABLED | 需勾選資料列後啟用 |
| 修改訂房卡 | r_1013 | `//button[@data-field-id='r_1013']` | enabled | |
| 排房 | r_1014 | `//button[@data-field-id='r_1014']` | enabled | |
| 旅客登記卡簽名 | openRcardPreviewDialog | `//button[@data-field-id='openRcardPreviewDialog']` | enabled | |
| 掃描 | openScanDialog | `//button[@data-field-id='openScanDialog']` | enabled | |
| 旅客登記卡列印 | — | — | DISABLED | |
| 旅客登記卡螢幕簽名 | openRcardPDFDialog | `//button[@data-field-id='openRcardPDFDialog']` | DISABLED | |

### Dialog 按鈕（已入住 tab — 僅 r_1010 入住 dialog）

與未入住 tab 差異：
- **移除**：入住(r_1011)、C/I公帳號(set_master_nos)、排房(r_1014)
- **新增**：房間細節(openRoomDetailDialog)

### Tab: 未入住（tab-NotCi / pane-NotCi / NotCiPanel）

HTML table（頁面第 4 個 table），14 欄（含 checkbox 欄），非 Syncfusion Grid。
- **Panel scope**：`//div[@id='NotCiPanel']` — 用於限定 checkbox 範圍

| 欄位序號 | 中文標題 | 顯示範例 | 備註 |
|---------|---------|---------|------|
| 0 | 選擇 | ☐ | `//input[@name='form-field-checkbox']`，每行一個 |
| 1 | 清掃狀態 | C : 乾淨 / D : 髒房 | |
| 2 | 房號 | 301 | |
| 3 | 住客狀態 | Arrival | |
| 4 | 住客姓名 | Card CO List A | |
| 5 | 入住日期 | 2024/01/05 | |
| 6 | 退房日期 | 2024/01/06 | |
| 7 | 房價代號 | Normal:現場訂房含早 | |
| 8 | 計價房型 | SPT | |
| 9 | 使用房型 | SPT / SPD | |
| 10 | 房租單價 | 7,900 | |
| 11 | 服務費 | 0 | |
| 12 | 瑕疵房 | N / Y | |
| 13 | 瑕疵原因 | (文字) | |

**Checkbox 定位**（推薦）：`//div[@id='NotCiPanel']//input[@name='form-field-checkbox']`
- 使用 NotCiPanel scope 比 `(//table)[4]` 更穩定
- 多房間時可用 `(//div[@id='NotCiPanel']//input[@name='form-field-checkbox'])[N]`
- ⚠️ **NotCiPanel 預設勾選從 Grid 點選的住客**：該筆會被排到 NotCiPanel 第一行並自動勾選（`checked=true`）。單筆入住時不需額外 click checkbox；多筆全選時需勾選其餘未勾的
- 操作前先查 `get_attribute("checked")`，已是目標狀態就跳過，未達標才 click

**選取行**：勾選 checkbox 後按「入住」(r_1011) 執行入住。

### Tab: 已入住（tab-Ci）

Grid 欄位（7 欄）：

| 欄位 | 中文標題 |
|------|---------|
| cleanStatus | 清掃狀態 |
| roomNos | 房號 |
| guestStatus | 住客狀態 |
| guestName | 住客姓名 |
| checkinDate | 入住日期 |
| checkoutDate | 退房日期 |
| balanceAmt | 住客帳餘額 |

## 製卡 Dialog（EasyUI Panel）

> 由入住成功後自動觸發（Alert「住客入住成功」→ 確定 → 開啟）

### Dialog 表單

| 元素 | data-field-id | 類型 | 狀態 | 備註 |
|------|---------------|------|------|------|
| 房號 | room_nos | input | DISABLED | |
| 人數 | adult_qnt | Syncfusion NumericTextBox | enabled | |
| 訂房卡退房時間 | order_eco_tim | input | DISABLED | |
| 預計退房時間 | room_eco_tim | input | DISABLED | |
| 房卡有效時間 | eco_tim | input | enabled | |
| 張數 | default_make_card_quantity | input | enabled | |

### Dialog 按鈕

| 按鈕 | Locator | 狀態 | 備註 |
|------|---------|------|------|
| 新卡 | `//button[normalize-space()='新卡']` | enabled | |
| 複製卡 | `//button[normalize-space()='複製卡']` | enabled | |
| 讀卡 | `//button[normalize-space()='讀卡']` | enabled | |

### Dialog Grid（11 欄）

| 欄位 | 中文標題 |
|------|---------|
| athena_id | athena_id |
| hotel_cod | hotel_cod |
| ins_usr | ins_usr |
| ikey | 訂房卡號 |
| room_nos | 房號 |
| guest_nam | 姓名 |
| action_rmk | 動作 |
| begin_dat | 製卡日期 |
| end_dat | 退房日期 |
| mifare_nos | 卡號 |
| ins_dat | 新增日期 |

### Dialog 關閉

- Close 按鈕：`(//a[contains(@class,'panel-tool-close')])[last()]`（製卡為最上層 panel 時適用）
- 製卡 + Check In 雙 panel 疊加時需注意 close 順序

### Dialog 關閉（Check In）

- Close 按鈕：`(//div[contains(@class,'panel-title') and contains(.,'check In')]/..//a[contains(@class,'panel-tool-close')])[last()]`（panel-title scope，入住後場景 match=1 且 visible）
- ⚠️ 取消入住後 panel-title scope 的 close 按鈕會變 hidden（0x0），需遍歷 `//a[contains(@class,'panel-tool-close')]` 找第一個 visible 的
- ⚠️ 不可用無 scope 的 `//a[contains(@class,'panel-tool-close')]` 做 find_element——入住後 match=6（5 hidden），Selenium 取 DOM 首個會打到 hidden

## 取消入住 Dialog（由 r_1020 觸發）

> 入口：checkinStatus 篩選「已入住」→ 選取已入住 row → 點擊 toolbar 取消入住(r_1020)
> 與入住 dialog 是不同入口，功能不同

### Dialog 按鈕

⚠️ 此 Dialog **無 tab 結構**（與入住 dialog 不同），直接顯示已入住資料列。dfid 同樣直接在 `<button>` 上。

| 按鈕 | data-field-id | Locator | 狀態 | 備註 |
|------|---------------|---------|------|------|
| 取消入住 | r_1021 | `//button[@data-field-id='r_1021']` | enabled | 勾選 checkbox 後可用 |
| 旅客登記卡列印 | — | — | DISABLED | |
| 旅客登記卡螢幕簽名 | openRcardPDFDialog | `//button[@data-field-id='openRcardPDFDialog']` | DISABLED | |

### 取消入住選項 Dialog（EasyUI + Element UI）

> 由勾選 checkbox → r_1021 觸發

| 元素 | 定位 | 類型 | 預設值 | 備註 |
|------|------|------|--------|------|
| 一併取消排房 | `(//label[contains(@class,'checkbox') and contains(.,'取消排房')])[last()]` | Element UI checkbox | checked | 取消勾選可保留排房 |
| 房間改成髒房 | `(//label[contains(@class,'checkbox') and contains(.,'改成髒房')])[last()]` | Element UI checkbox | checked | 取消勾選保持房間清潔狀態 |
| 確定 | `//button[normalize-space()='確定']` | button | — | |
| 關閉 | `//a[contains(@class,'panel-tool-close')]` | link | — | |

## 操作備註

- **入住流程（已驗證）**：點選主 Grid 資料列 → 入住(r_1010) → Check In Dialog 開啟 → 在未入住 tab 勾選 checkbox → 入住(r_1011) → Alert「住客入住成功」→ 確定 → 製卡 Dialog
- **髒房/瑕疵房入住**：若勾選的資料列含髒房，入住前先跳警告 Alert「提示以下房號為��房 XXX,不可執行入住」→ 確定 → 再跳「住客入住成功」→ 確定 → 製卡 Dialog。可入住的房間仍會成功入住
- **入住後狀態變化**：主 Grid 的 orderStatus 變為「I: 今日到達」；未入住 tab 中該列消失，出現在已入住 tab（guestStatus 變「In House」）
- **Alert 確定按鈕**：頁面有多個 `//button[normalize-space()='確定']`（含隱藏的），CLI 自動 skip hidden elements 點擊可見的。實測 skip 5 hidden → clicking #6
- **製卡 Dialog 關閉**：`(//a[contains(@class,'panel-tool-close')])[last()]` 可正常關閉
- **Check In Dialog 關閉**：`//a[contains(@class,'panel-tool-close')]` 正常關閉（2026-05-22 驗證）
- **Syncfusion Grid 選取**：點擊 `//td[@field='roomNos' and normalize-space()='202']` 會觸發整行 cell active（32 個 .e-rowcell.e-active），非傳統 row selected。CLI diff 可偵測 grid:selected/deselected
- **取消入住流程（已驗證 2026-05-23）**：checkinStatus 切「Y:已入住」→ 搜尋 → 選取已入住 row → r_1020 → 取消入住 Dialog → 勾選 checkbox → r_1021 → 取消入住選項 Dialog → 取消勾選「一併取消排房」和「房間改成髒房」→ 確定 → Alert「住客取消入住成功」→ 確定 → 關閉 Dialog
- **取消入住後 close 按鈕**：`(//a[contains(@class,'panel-tool-close')])[last()]` 為 hidden（0x0），需用 `(//a[contains(@class,'panel-tool-close')])[3]` 或 JS click
- **⚠️ 取消入住選項預設全勾**：兩個 Element UI checkbox 預設都是 checked（取消排房 + 改髒房），不取消勾選會導致需要重新排房和房間變髒
- **checkinStatus 篩選**：預設「N:未入住」，已入住的房間不會出現在列表中。要操作取消入住需切換到「Y:已入住」
- **多筆入住**：可勾選多筆資料列同時入住；若有髒房會跳出警告，成功入住房間仍跳製卡視窗
- **data-field-id 拼字錯誤**：`querySetsSettingButtohn`（應為 Button）
- **初始 Alert**：首次載入可能跳出「提示NO_GRIDREF」警告，按「確定」關閉

### ⚠️ 未驗互動

- 房間細節(openRoomDetailDialog) 的 dialog 內容
- 修改訂房卡(r_1013) 的 dialog 內容
- 掃描(openScanDialog) 的 dialog 內容
- 旅客登記卡簽名(openRcardPreviewDialog) 的 dialog 內容

### 📌 未展開

- querySets 設定 dialog
- Check In Dialog 內的子 dialog（排房、修改訂房卡、房間細節）
- 製卡 Dialog 的實際製卡操作（新卡/複製卡/讀卡）
