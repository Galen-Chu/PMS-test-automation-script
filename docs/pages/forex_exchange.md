# 外幣匯兌維護（PMS0310050）

> 路徑：出納 → 外幣匯兌維護
> 程式代碼：PMS0310050
> SPA 導航：`//button[normalize-space()='出納']` → `//span[@data-field-id='PMS0310050']`
> ⚠️ 需先完成開班作業才能使用

---

## 佈局

```
外幣匯兌維護(PMS0310050)
├── [搜尋區] ─ 兌換日期(batchDate)、房號(roomNumber)、幣別(fmoneyCode)、姓名(fullName)、班別(shiftCode)、新增者(insertUser)、訂房卡號(ikey)、外幣金額(fmoneyAmt)、證件號碼(idCode)、銷售點(rsptCode)
│   └── 搜尋(PMS0310050_doSearch)、清除(PMS0310050_doClear)、切換(PMS0310050_toggle)
├── [操作列] ─ 作廢、補印水單、新增(橘色加號)、編輯
└── [列表 Grid] ─ EasyUI DataGrid，10 欄（勾選/兌換日期/外幣金額/幣別/姓名/狀態/訂房卡號/備註/房號/班別）
    └── 點擊新增 → 外幣匯兌維護 Panel（新增/編輯表單）
```

## 框架分布

| 區塊 | 框架 | 判斷依據 |
|------|------|---------|
| 搜尋區 | Syncfusion + Element UI | DatePicker + Element UI dropdown |
| 列表 Grid | EasyUI DataGrid | `datagrid-row-*`、editable checkbox |
| 新增/編輯 Panel | EasyUI Panel + Syncfusion | `panel-tool-close` + NumericTextBox |

## 搜尋區

| 元素 | data-field-id | 類型 | Locator | 備註 |
|------|---------------|------|---------|------|
| 兌換日期 | batchDate | Syncfusion DatePicker | `//div[@data-field-id='batchDate']//input` | |
| 房號 | roomNumber | input | `//div[@data-field-id='roomNumber']//input` | |
| 幣別 | fmoneyCode | Element UI dropdown | `//div[@data-field-id='fmoneyCode']//input` | AUD/CAD/CNY/EUR/GBP/HKD/JPY/KRW/SGD... |
| 姓名 | fullName | input | `//div[@data-field-id='fullName']//input` | |
| 班別 | shiftCode | input | `//div[@data-field-id='shiftCode']//input` | |
| 新增者 | insertUser | input | `//div[@data-field-id='insertUser']//input` | |
| 訂房卡號 | ikey | input | `//div[@data-field-id='ikey']//input` | |
| 外幣金額 | fmoneyAmt | input | `//div[@data-field-id='fmoneyAmt']//input` | |
| 證件號碼 | idCode | input | `//div[@data-field-id='idCode']//input` | |
| 銷售點 | rsptCode | input | `//div[@data-field-id='rsptCode']//input` | |

## 操作列

| 元素 | Locator | 備註 |
|------|---------|------|
| 搜尋 | `//button[@data-field-id='PMS0310050_doSearch']` | |
| 清除 | `//button[@data-field-id='PMS0310050_doClear']` | |
| 切換 | `//button[@data-field-id='PMS0310050_toggle']` | |
| 作廢 | `//button[normalize-space()='作廢']` | 需勾選資料列 |
| 補印水單 | `//button[normalize-space()='補印水單']` | |
| 新增 | `//button[img/@alt='add']` | 橘色加號 |
| 編輯 | `//button[img/@alt='edit']` | |

## 列表 Grid（10 欄）

| 欄位 | field | 中文標題 | 備註 |
|------|-------|---------|------|
| ck | ck | 勾選 | editable |
| batchDate | batchDate | 兌換日期 | |
| fmoneyAmt | fmoneyAmt | 外幣金額 | |
| fmoneyCode | fmoneyCode | 幣別 | |
| fullName | fullName | 姓名 | |
| fxStatus | fxStatus | 狀態 | |
| ikey | ikey | 訂房卡號 | |
| remark | remark | 備註 | |
| roomNumber | roomNumber | 房號 | |
| shiftCode | shiftCode | 班別 | |

**定位**：`//td[@field='%s']`

## 新增/編輯 Panel（外幣匯兌維護）

### DISABLED 欄位

| 元素 | data-field-id | 中文 | 類型 |
|------|---------------|------|------|
| fxNumber | fxNumber | 水單號碼 | input |
| rsptCode | rsptCode | 銷售點 | input |
| shiftCode | shiftCode | 班別 | input |
| batchDate | batchDate | 兌換日期 | input |
| fxStatus | fxStatus | 水單狀態 | EasyUI combobox |
| ikey | ikey | 訂房卡號 | input |
| insertDate | insertDate | 新增日期 | input |
| insertUser | insertUser | 新增者 | input |
| updateDate | updateDate | 修改日期 | input |
| updateUser | updateUser | 修改者 | input |

### 可編輯欄位

| 元素 | data-field-id | 中文 | 類型 | Locator |
|------|---------------|------|------|---------|
| roomNumber | roomNumber | 房號 | EasyUI combobox | `//div[@data-field-id='roomNumber']//input` |
| fullName | fullName | 姓名 | EasyUI combobox | `//div[@data-field-id='fullName']//input` |
| countryCode | countryCode | 國籍 | EasyUI combobox | `//div[@data-field-id='countryCode']//input` |
| idCode | idCode | 證件號碼 | input | `//div[@data-field-id='idCode']//input` |
| birthday | birthday | 生日 | Syncfusion DatePicker | `//div[@data-field-id='birthday']//input` |
| cashType | cashType | 兌換種類 | EasyUI combobox | `//div[@data-field-id='cashType']//input` |
| fmoneyCode | fmoneyCode | 幣別 | EasyUI combobox | `//div[@data-field-id='fmoneyCode']//input` |
| remark | remark | 備註 | input | `//div[@data-field-id='remark']//input` |
| fmoneyAmt | fmoneyAmt | 外幣金額 | NumericTextBox | `//div[@data-field-id='fmoneyAmt']//input` |
| buyRate | buyRate | 匯率 | NumericTextBox | `//div[@data-field-id='buyRate']//input` |
| totalAmt | totalAmt | 兌換總額 | NumericTextBox | `//div[@data-field-id='totalAmt']//input` |
| serviceAmt | serviceAmt | 手續費 | NumericTextBox | `//div[@data-field-id='serviceAmt']//input` |
| tmoneyAmt | tmoneyAmt | 兌換淨額 | NumericTextBox | `//div[@data-field-id='tmoneyAmt']//input` |
| noteNumber | noteNumber | 支票/鈔票號碼 | textarea | `//div[@data-field-id='noteNumber']//textarea` |

### 按鈕

| 按鈕 | Locator | 狀態 | 備註 |
|------|---------|------|------|
| 作廢 | `//button[normalize-space()='作廢']` | DISABLED | 新增模式下不可用 |
| 儲存 | `//button[img/@alt='save']` | enabled | 橘色磁碟片 |

## 操作備註

- **新增流程**：橘色加號 → 填姓名 → 選幣別 → 輸入外幣金額/手續費 → 儲存 → 「新增成功 是否列印水單？」提示
- **人民幣 vs 非人民幣**：案例 #481(非人民幣) 和 #484(人民幣) 流程相同，僅幣別選擇不同
- **開班前置**：首次進入需先開班（廳別=FO、班別=a、密碼=autotest）
- **幣別選項**：AUD(澳幣), CAD(加幣), CNY(人民幣), EUR(歐元), GBP(英鎊), HKD(港幣), JPY(日幣), KRW(韓幣), SGD...
- **EasyUI combobox 操作**：房號/姓名/國籍/兌換種類/幣別 都是 EasyUI combobox，需用 click + 選項方式操作
