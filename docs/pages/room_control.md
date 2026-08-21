# 房控管理（PMS0410010）

> 路徑：房務 → 房控管理
> 程式代碼：PMS0410010
> SPA 導航：`//button[normalize-space()='房務']` → `//span[@data-field-id='PMS0410010']`

---

## 佈局

```
房控管理(PMS0410010)
├── [搜尋區] ─ 房號(room_nos)、房型(room_cod)、排房狀況(assign_sta)、電話勿擾(dnd_cod)、瑕疵房(oos_sta)、待檢查(check_sta)、棟別(build_nos)、拆併床(bed_sta)、房控勿擾(dnd)
│   └── 搜尋(PMS0410010_doSearch)、清除(PMS0410010_doClear)、切換(PMS0410010_toggle)
├── [狀態統計列] ─ OC/OD/DOC/DOD/VC/VD/OOO/OOS/S/All 按鈕（可點擊篩選）
├── [樓層導航] ─ ALL, 1F~15F 連結
├── [視圖切換] ─ 大圖示/列表 切換、房控連線
└── [房間卡片區] ─ Vue 元件，每個房間一張卡片
    └── 點擊房間卡片 → 功能選項 Panel
        ├── 清掃 → 清掃房間 Panel
        ├── 清掃樓層 → 清掃樓層 Dialog (Syncfusion)
        ├── 修理/參觀 → 修理/參觀 Panel
        ├── 修理樓層 → 修理樓層 Dialog (Syncfusion)
        ├── 查詢修理/參觀 → 📌 未展開
        ├── 瑕疵房 → 瑕疵房設定 Panel
        ├── 拆併床 → 📌 未展開
        └── 房務入帳 → ⚠️ 未驗互動（需 OC 房間才啟用）
```

## 框架分布

| 區塊 | 框架 | 判斷依據 |
|------|------|---------|
| 搜尋區 | Syncfusion + Element UI 混合 | `data-field-id` + Element UI dropdown |
| 狀態統計列 | Vue | 自訂元件 |
| 樓層導航 | HTML `<a>` | `<a>` 連結 |
| 房間卡片區 | Vue | `data-v-*` 屬性 |
| 功能選項 | EasyUI Panel | `panel-tool-close` |
| 清掃房間 | EasyUI Panel | `panel-tool-close` |
| 修理/參觀 | EasyUI Panel | `panel-tool-close` |
| 瑕疵房設定 | EasyUI Panel | `panel-tool-close` |
| 修理樓層 | Syncfusion Dialog + EasyUI | `e-dlg-header` + EasyUI combobox |

## 搜尋區

| 元素 | 類型 | Locator | 備註 |
|------|------|---------|------|
| 房號 | input | `//div[@data-field-id='room_nos']//input` | |
| 房型 | Element UI dropdown | `//div[@data-field-id='room_cod']//input` | |
| 排房狀況 | Element UI dropdown | `//div[@data-field-id='assign_sta']//input` | |
| 電話勿擾 | Element UI dropdown | `//div[@data-field-id='dnd_cod']//input` | |
| 瑕疵房 | Element UI dropdown | `//div[@data-field-id='oos_sta']//input` | |
| 待檢查 | Element UI dropdown | `//div[@data-field-id='check_sta']//input` | |
| 棟別 | Element UI dropdown | `//div[@data-field-id='build_nos']//input` | |
| 拆併床 | Element UI dropdown | `//div[@data-field-id='bed_sta']//input` | |
| 房控勿擾 | Element UI dropdown | `//div[@data-field-id='dnd']//input` | |
| 搜尋 | button | `//button[@data-field-id='PMS0410010_doSearch']` | |
| 清除 | button | `//button[@data-field-id='PMS0410010_doClear']` | |
| 切換 | button | `//button[@data-field-id='PMS0410010_toggle']` | |

## 狀態統計按鈕

| 代碼 | Locator | 意義 |
|------|---------|------|
| OC | `//button[starts-with(normalize-space(),'OC:')]` | Occupied Clean |
| OD | `//button[starts-with(normalize-space(),'OD:')]` | Occupied Dirty |
| DOC | `//button[starts-with(normalize-space(),'DOC:')]` | Due Out Clean |
| DOD | `//button[starts-with(normalize-space(),'DOD:')]` | Due Out Dirty |
| VC | `//button[starts-with(normalize-space(),'VC:')]` | Vacant Clean |
| VD | `//button[starts-with(normalize-space(),'VD:')]` | Vacant Dirty |
| OOO | `//button[starts-with(normalize-space(),'OOO:')]` | Out of Order |
| OOS | `//button[starts-with(normalize-space(),'OOS:')]` | Out of Service |
| S | `//button[starts-with(normalize-space(),'S:')]` | 參觀中 |
| All | `//button[starts-with(normalize-space(),'All:')]` | 全部 |

## 樓層導航

`//a[normalize-space()='2F']` — 格式：ALL, 1F~15F

## 房間卡片

| 定位 | Locator | 備註 |
|------|---------|------|
| 房間卡片（可見樓層） | `//div[@class='tab-content' and not(@style='display: none;')]//div[@class='card--room']//span[normalize-space()='%s']` | 需限定可見 tab-content |
| 房間方塊（讀取狀態用） | `//div[@slot='reference' and descendant::span[normalize-space()='%s']]` | 有住客的房間才有 slot=reference |
| 邊框顏色判斷 | `style.borderColor` | 綠色=乾淨、紅色=髒房、青色=修理、洋紅=參觀、灰色=瑕疵房 |

## 功能選項 Panel（EasyUI）

> 由點擊房間卡片觸發

| 按鈕 | Locator | 備註 |
|------|---------|------|
| 清掃 | `//button[normalize-space()='清掃']` | |
| 清掃樓層 | `//button[normalize-space()='清掃樓層']` | |
| 修理/參觀 | `//button[normalize-space()='修理/參觀']` | |
| 修理樓層 | `//button[normalize-space()='修理樓層']` | |
| 查詢修理/參觀 | `//button[normalize-space()='查詢修理/參觀']` | 📌 未展開 |
| 瑕疵房 | `//button[normalize-space()='瑕疵房']` | |
| 拆併床 | `//button[normalize-space()='拆併床']` | 📌 未展開 |
| 房務入帳 | `//button[normalize-space()='房務入帳']` | ⚠️ OC 房間才 enabled |

## 清掃房間 Panel

| 元素 | 類型 | Locator | 備註 |
|------|------|---------|------|
| 房號 | input (read-only) | `//label[normalize-space()='房號']/following-sibling::input` | |
| 清掃狀態 | input (read-only) | `//label[normalize-space()='清掃狀態']/following-sibling::input` | |
| 設定乾淨 | button | `//button[normalize-space()='設定乾淨']` | |
| 設定髒房 | button | `//button[normalize-space()='設定髒房']` | |
| 待檢查 | button | `//button[normalize-space()='待檢查']` | |

## 修理/參觀 Panel

| 元素 | data-field-id | 類型 | Locator | 備註 |
|------|---------------|------|---------|------|
| 房號 | room_nos | input | `//div[@data-field-id='room_nos']//input` | |
| 類別 | repair_typ | EasyUI combobox | `//div[@data-field-id='repair_typ']//input` | R:修理, S:參觀 |
| 開始日期 | start_dat | Syncfusion DatePicker | `//div[@data-field-id='start_dat']//input` | |
| 結束日期 | end_dat | Syncfusion DatePicker | `//div[@data-field-id='end_dat']//input` | |
| 修理/參觀原因 | reason_rmk | textarea | `//div[@data-field-id='reason_rmk']//textarea` | |
| 儲存 | — | button (img) | `//button[img/@alt='save']` | 橘色磁碟片 |

## 修理樓層 Dialog

| 元素 | data-field-id | 類型 | Locator | 備註 |
|------|---------------|------|---------|------|
| 樓層 | floor_nos | EasyUI combobox | `//div[@data-field-id='floor_nos']//input` | |
| 從 | start_dat | Syncfusion DatePicker | `//div[@data-field-id='start_dat']//input` | |
| 至 | end_dat | Syncfusion DatePicker | `//div[@data-field-id='end_dat']//input` | |
| 修理原因 | reason_rmk | input | `//div[@data-field-id='reason_rmk']//input` | |
| 房間勾選 | — | checkbox (26個) | `//input[@name='form-field-checkbox']` | 依樓層篩選 |
| 修理 | button | `//button[normalize-space()='修理']` | |

Grid（Table #1）：房型 | 房號
Grid（Table #2）：狀態 | 房號 | 原因

## 瑕疵房設定 Panel

| 元素 | 類型 | Locator | 備註 |
|------|------|---------|------|
| 狀態顯示 | label | `//label[contains(@class,'text-red')]` | 顯示 N : OOS |
| 理由 | textarea | `//textarea` | 輸入瑕疵原因 |
| 設定 | button | `//button[normalize-space()='設定']` | |
| 清除 | button | `//button[normalize-space()='清除']` | 清除瑕疵設定 |

## 操作備註

- **房間卡片選擇**：必須用 `//div[@class='tab-content' and not(@style='display: none;')]//div[@class='card--room']//span[normalize-space()='%s']` 限定可見樓層 tab
- **房間狀態判斷**：透過邊框顏色（`style.borderColor`）判斷 — 綠色=乾淨、紅色=髒房、青色=修理、洋紅=參觀、灰色=瑕疵房
- **功能選項啟用規則**：「房務入帳」按鈕只有 OC（Occupied Clean）房間才 enabled，其餘房間為 disabled
- **EasyUI Panel close**：`[last()]` 在單層 panel 時可靠，多層疊加時可能被 BLOCKED
- **⚠️ 禁止 JS remove()**：用 `element.remove()` 清除 panel/mask 會破壞 Vue 事件處理器，導致後續操作全部失效。如需清除遮擋，只能用 `style.display='none'`
- **頁面刷新**：不能用 `nav` 刷新 SPA 頁面（會使 session 失效），需透過 SPA 選單重新導航
- **data-field-id 前綴**：搜尋區按鈕使用 `PMS0410010_` 前綴

### ⚠️ 未驗互動

- 房務入帳 dialog 內容（需 OC 房間觸發）
- 清掃樓層 dialog 完整操作流程
- 查詢修理/參觀 dialog

### 📌 未展開

- 拆併床 dialog（openRoomDetailDialog 相關）
- 查詢修理/參觀 dialog
- 大圖示/列表視圖切換的差異
