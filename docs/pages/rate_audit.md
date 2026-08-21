# 房價稽核表（PMS0510020）

> 路徑：夜核 → 房價稽核表
> 程式代碼：PMS0510020
> SPA 導航：`//button[normalize-space()='夜核']` → `//span[@data-field-id='PMS0510020']`

---

## 佈局

```
房價稽核表(PMS0510020)
├── [搜尋區] ─ 查詢日期(search_date)、排序(sort_culums)、類別(guest_way)、金額為零不顯示(noshow_zero)
│   └── 搜尋(undefined_doSearch)、清除(undefined_doClear)、匯出(export)
└── [報表 Grid] ─ EasyUI DataGrid（查詢後顯示結果）
```

## 框架分布

| 區塊 | 框架 | 判斷依據 |
|------|------|---------|
| 搜尋區 | Syncfusion + Element UI | DatePicker + Element UI dropdown |
| 報表 Grid | EasyUI DataGrid | `datagrid-row-*` |

## 搜尋區

| 元素 | data-field-id | 類型 | Locator | 備註 |
|------|---------------|------|---------|------|
| 查詢日期 | search_date | Syncfusion DatePicker | `//div[@data-field-id='search_date']//input` | 必填（*標記） |
| 排序 | sort_culums | Element UI dropdown | `//div[@data-field-id='sort_culums']//input` | by_ikey(依訂房卡), by_room_nos(依房號), by_rate_cod(依房價代號), by_master_... |
| 類別 | guest_way | Element UI dropdown | `//div[@data-field-id='guest_way']//input` | F:散客, G:團體, C:商務 |
| 金額為零不顯示 | noshow_zero | checkbox | `//div[@data-field-id='noshow_zero']//input` | |
| 搜尋 | button | `//button[@data-field-id='undefined_doSearch']` | data-field-id 含 undefined 前綴 |
| 清除 | button | `//button[@data-field-id='undefined_doClear']` | |
| 匯出 | button | `//button[img/@alt='export']` | |

## 操作備註

- **查詢流程**：選擇類別（F/G/C）→ 點搜尋（藍色放大鏡）→ 報表顯示結果
- **data-field-id 前綴**：報表頁面通用問題，搜尋/清除按鈕使用 `undefined_` 前綴
- **報表 Grid**：查詢後動態產生，空查詢時 Grid 為空
