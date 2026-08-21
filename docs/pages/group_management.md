# 團體管理（PMS0310040）

> 路徑：出納 → 團體管理
> 程式代碼：PMS0310040
> SPA 導航：`//button[normalize-space()='接待']` → `//span[@data-field-id='PMS0310040']`（注意：實際在出納模組下）

---

## 佈局

```
團體管理(PMS0310040)
├── [搜尋區] ─ 入住日期(ci_dat)、退房日期(co_dat)、公帳號(master_nos)、團號(group_nos)、訂房卡號(ikey)、關聯單號(link_nos)、訂房狀態(order_sta)
│   └── 搜尋(PMS0310040_doSearch)、清除(PMS0310040_doClear)、切換(PMS0310040_toggle)
└── [列表 Grid] ─ EasyUI DataGrid，9 欄
    └── 點選列 + 團體明細 → 團體明細 Panel
        ├── [資訊區] ─ 訂房卡號/團號/公帳號/入住/退房日期/導遊資訊/訂房備註（多數 DISABLED）
        ├── [金額區] ─ 團帳總額(group_tot)、訂金編號/餘額、大人/小孩/總人數、FOC
        ├── [Tab: 已入住] ─ Grid（9 欄：勾選/房號/序/住客姓名/狀態/餘額/預付款餘額/C/O提醒/退房日期）
        ├── [Tab: 未入住] ─ 📌 未切換
        └── [操作按鈕] ─ 清子房間/改房價/退房日期/櫃台備品(disabled)/住客帳維護/轉帳/訂房卡/帳單列印/住客名單/團體清單/團體簽認單/房租總額/預估款轉入
            └── [退房日期] → 改退房日 Panel
                ├── 新退房日期(new_co_dat)
                ├── Radio: ROOM(單一房號) / IKEY(訂房卡全部房號)
                ├── Grid（5 欄：勾選/房號/住客姓名/入住日期/原退房日）
                └── 儲存按鈕（橘色磁碟片）
```

## 框架分布

| 區塊 | 框架 | 判斷依據 |
|------|------|---------|
| 搜尋區 | Syncfusion + Element UI | DatePicker + `data-field-id` |
| 列表 Grid | EasyUI DataGrid | `datagrid-row-*` |
| 團體明細 Panel | EasyUI Panel + Syncfusion | `panel-tool-close` + NumericTextBox |
| 改退房日 Panel | EasyUI Panel + Syncfusion | `panel-tool-close` + DatePicker |

## 搜尋區

| 元素 | 類型 | Locator | 備註 |
|------|------|---------|------|
| 入住日期 | Syncfusion DatePicker | `//div[@data-field-id='ci_dat']//input` | |
| 退房日期 | Syncfusion DatePicker | `//div[@data-field-id='co_dat']//input` | |
| 公帳號 | input | `//div[@data-field-id='master_nos']//input` | |
| 團號 | input | `//div[@data-field-id='group_nos']//input` | |
| 訂房卡號 | input | `//div[@data-field-id='ikey']//input` | |
| 關聯單號 | input | `//div[@data-field-id='link_nos']//input` | |
| 訂房狀態 | Element UI dropdown | `//div[@data-field-id='order_sta']//input` | N:未入住, O:已入住, I:今日到達, A:全部, C:退房 |
| 搜尋 | button | `//button[@data-field-id='PMS0310040_doSearch']` | |
| 清除 | button | `//button[@data-field-id='PMS0310040_doClear']` | |
| 切換 | button | `//button[@data-field-id='PMS0310040_toggle']` | |
| 團體明細 | button | `//button[normalize-space()='團體明細']` | 需先選取資料列 |

## 列表 Grid（9 欄）

| 欄位 | field 屬性 | 中文標題 |
|------|-----------|---------|
| master_nos | master_nos | 公帳號 |
| group_nos | group_nos | 訂房名稱/團號 |
| order_sta | order_sta | 訂房狀態 |
| ikey | ikey | 訂房卡號 |
| guide_nam | guide_nam | 導遊 |
| guide_tel | guide_tel | 導遊聯絡電話 |
| guide_room | guide_room | 導遊房號 |
| ci_dat | ci_dat | 入住日期 |
| co_dat | co_dat | 退房日期 |

**定位**：`//td[@field='%s']`

## 團體明細 Panel

> 由選取 Grid 資料列 + 點擊「團體明細」觸發

### 資訊欄位（多數 DISABLED）

| 元素 | data-field-id | 類型 | 狀態 |
|------|---------------|------|------|
| 訂房卡號 | ikey | input | DISABLED |
| 團號 | group_nos | input | DISABLED |
| 公帳號 | master_nos | input | DISABLED |
| 入住日期 | ci_dat | Syncfusion DatePicker | DISABLED |
| 退房日期 | co_dat | Syncfusion DatePicker | DISABLED |
| 導遊姓名 | guide_nam | input | DISABLED |
| 導遊手機 | guide_tel | input | DISABLED |
| 導遊房間 | guide_room | input | DISABLED |
| 訂房備註 | order_rmk | textarea | DISABLED |
| 訂金編號 | deposit_nos | input | DISABLED |
| 訂金餘額 | deposit_tot | input | DISABLED |
| FOC | foc_amt | input | DISABLED |

### 可編輯欄位

| 元素 | data-field-id | 類型 |
|------|---------------|------|
| 團帳總額 | group_tot | Syncfusion NumericTextBox |
| 大人 | adult_qnt | Syncfusion NumericTextBox |
| 小孩 | child_qnt | Syncfusion NumericTextBox |
| 總人數 | total_qnt | Syncfusion NumericTextBox |

### 操作按鈕

| 按鈕 | Locator | 狀態 | 備註 |
|------|---------|------|------|
| 清子房間 | `//button[normalize-space()='清子房間']` | enabled | 案例 #501 |
| 改房價 | `//button[normalize-space()='改房價']` | enabled | |
| 退房日期 | `//button[normalize-space()='退房日期']` | enabled | 案例 #471，開啟改退房日 Panel |
| 櫃台備品 | `//button[normalize-space()='櫃台備品']` | DISABLED | |
| 住客帳維護 | `//button[normalize-space()='住客帳維護']` | enabled | |
| 轉帳 | `//button[normalize-space()='轉帳']` | enabled | |
| 訂房卡 | `//button[normalize-space()='訂房卡']` | enabled | |
| 帳單列印 | `//button[normalize-space()='帳單列印']` | enabled | |
| 住客名單 | `//button[normalize-space()='住客名單']` | enabled | |
| 團體清單 | `//button[normalize-space()='團體清單']` | enabled | |
| 團體簽認單 | `//button[normalize-space()='團體簽認單']` | enabled | |
| 房租總額 | `//button[normalize-space()='房租總額']` | enabled | |
| 預估款轉入 | `//button[normalize-space()='預估款轉入']` | enabled | |

### Tab: 已入住（tab-Ci）

Grid 欄位（9 欄）：

| 欄位 | field | 中文 | 備註 |
|------|-------|------|------|
| ck | ck | 勾選 | editable |
| room_nos | room_nos | 房號 | |
| room_ser | room_ser | 序 | |
| alt_nam | alt_nam | 住客姓名 | |
| guest_sta | guest_sta | 狀態 | |
| item_tot | item_tot | 餘額 | |
| prepay_amt | prepay_amt | 預付款餘額 | |
| co_rmk | co_rmk | C/O提醒 | |
| aco_dat | aco_dat | 退房日期 | |

### Tab: 未入住（tab-NotCi）

📌 未切換探索

## 改退房日 Panel

> 由團體明細 Panel 內點擊「退房日期」觸發

| 元素 | data-field-id | 類型 | Locator | 備註 |
|------|---------------|------|---------|------|
| 新退房日期 | new_co_dat | Syncfusion DatePicker | `//div[@data-field-id='new_co_dat']//input` | |
| 篩選模式 | filter | radio | `//div[@data-field-id='filter']//input` | ROOM(單一房號) / IKEY(訂房卡全部房號) |
| 儲存 | — | button (img) | `//button[img/@alt='save']` | 橘色磁碟片 |

Grid（5 欄）：ck(editable) | room_nos(房號) | alt_nam(住客姓名) | ci_dat(入住日期) | eco_dat(原退房日)

## 操作備註

- **團體明細入口**：需先在列表 Grid 選取一筆資料列，再按「團體明細」按鈕
- **改退房日流程**：退房日期 → 選新日期 → 選 ROOM 或 IKEY 模式 → 勾選 Grid 行 → 儲存
- **清子房間流程**：在已入住 tab 勾選已退房子房間 → 清子房間 → 退房完成
- **訂房狀態選項**：N(未入住), O(已入住), I(今日到達), A(全部), C(退房)
- **data-field-id 前綴**：搜尋區按鈕使用 `PMS0310040_` 前綴
- **Panel close**：`[last()]` 通常可正常關閉單層 panel，多層時需 JS click

### ⚠️ 未驗互動

- 清子房間實際操作（不可逆）
- 改房價 dialog
- 改退房日儲存（不可逆）
- 各報表按鈕（帳單列印/住客名單/團體清單/團體簽認單/房租總額）

### 📌 未展開

- 未入住 tab (tab-NotCi)
- 改房價 dialog
- 住客帳維護/轉帳/訂房卡 子 dialog
- 預估款轉入 dialog
