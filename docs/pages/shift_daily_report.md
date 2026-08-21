# 交班日報表（PMS03R0010）

> 路徑：出納 → 交班日報表
> 程式代碼：PMS03R0010
> 頁面類型：報表查詢頁（查詢條件 + PDF iframe）

---

## 佈局

```
交班日報表
├── [查詢條件區] ─ 單排查詢欄位 + 查詢/清除按鈕
├── [匯出按鈕] ─ 右側橘色下載 icon
└── [報表區] ─ iframe#reportIframe，查詢後載入 Chrome 內建 PDF viewer
    └── PDF 內容（伺服器端生成，URL 帶 JWT accessToken）
```

## 框架分布

| 區塊 | 框架 | 判斷依據 |
|------|------|---------|
| 查詢條件（日期/班別/結帳者） | Syncfusion EJ2 | `data-field-id`、input 結構 |
| 查詢條件（廳別/列印項目/查詢依據） | **Element UI** | `el-select-dropdown__list`、`el-scrollbar`；`ddl-options` 偵測不到此類下拉 |
| 查詢/清除按鈕 | Syncfusion | `data-field-id="undefined_doSearch"` / `"undefined_doClear"` |
| 匯出按鈕 | Syncfusion | `data-field-id="export"` |
| 報表區 | Chrome PDF viewer | `<iframe id="reportIframe">` 指向 `.pdf` URL |

## 元素清單

### 查詢條件區

| 元素 | 類型 | Locator | 框架 | 備註 |
|------|------|---------|------|------|
| 查詢日期 | input | `//div[@data-field-id='batch_dat']//input` | Syncfusion | 必填，預設今天日期 |
| 廳別 | select | `//div[@data-field-id='rspt_cod']//input` | **Element UI** | 必填；展開用 `//div[@data-field-id='rspt_cod']//i` 點 icon |
| 查詢班別 | input | `//div[@data-field-id='shift_cod']//input` | Syncfusion | 選填 |
| 結帳者 | input | `//div[@data-field-id='co_usr']//input` | Syncfusion | 選填 |
| 列印項目 | select | `//div[@data-field-id='print_type']//input` | **Element UI** | **必填**（預設「S：服務項目」，清掉後查詢會失敗） |
| 查詢依據 | select | `//div[@data-field-id='income_type']//input` | **Element UI** | 預設「1：入帳收入」 |

### Element UI 下拉選項操作

```
# 展開下拉（⚠️ 必須點 input，不能點 icon）
click -x "//div[@data-field-id='{field}']//input"

# 選擇選項（文字比對）
click -x "//ul[contains(@class,'el-select-dropdown__list')]//span[normalize-space()='{option_text}']"
```

> **陷阱**：部分 Element UI select 啟用了 clearable。點 `//i`（icon）在有值時會**清掉已選值**而非展開下拉。
> 點 `//input` 則安全 — 無論有無值都能正確展開。rspt_cod 無此問題（未啟用 clearable），print_type 和 income_type 會被清掉。

**廳別選項**（33 個，含）：1:1, CA01:跳棋餐廳, FO:客房櫃檯, REST:餐廳, 123:行政樓層, PD:列印消費明細, NEW:新櫃台 ...

**列印項目選項**：M:交易類別, S:服務項目

**查詢依據選項**：1:入帳收入, 2:沖銷收入

### 操作按鈕

| 元素 | 類型 | Locator | 備註 |
|------|------|---------|------|
| 查詢 | button | `//button[@data-field-id='undefined_doSearch']` | 放大鏡 icon |
| 清除 | button | `//button[@data-field-id='undefined_doClear']` | 垃圾桶 icon |
| 匯出 | button | `//button[@data-field-id='export']` | 橘色下載 icon；⚠️ 未驗互動（會觸發檔案下載） |

### 報表區

| 元素 | 類型 | Locator | 備註 |
|------|------|---------|------|
| 報表 iframe | iframe | `//iframe[@id='reportIframe']` | 查詢前不存在；查詢後動態載入 |

## 報表內容讀取

Chrome 內建 PDF viewer 使用原生插件渲染，**DOM 裡沒有文字內容**，無法用 XPath/Selenium 直接讀取。

### 推薦方案：Python requests 下載 + pdfplumber 解析

```python
import io, requests, pdfplumber

# 1. 從 iframe src 取得 PDF URL
pdf_url = driver.execute_script(
    "var f = document.getElementById('reportIframe'); return f ? f.src : null;"
)

# 2. 直接從測試機 HTTP GET（不經過 Grid）
resp = requests.get(pdf_url, timeout=30, verify=False)

# 3. 解析 PDF 文字
with pdfplumber.open(io.BytesIO(resp.content)) as pdf:
    text = "\n".join(page.extract_text() or "" for page in pdf.pages)
```

**PDF URL 結構**：`/pms/node/public/{報表名}_{廳別}_{使用者}_{timestamp}.pdf?_rand={rand}&accessToken={JWT}`

- JWT 有效期約 30 分鐘，查詢後立即讀取即可
- PDF 大小實測約 38KB（單頁空報表），不經過 Grid 無大小限制問題
- 實測耗時：下載 0.17s + 解析 0.01s = 0.18s

### 備用方案：瀏覽器 fetch + base64 回傳

適用於 PDF URL 不在 iframe src 中的情況（如 blob URL）。base64 回傳走 WebDriver 協定，大檔可能有大小限制風險。

### 提取文字範例

```
德安資訊股份有限公司 2026/05/18 23:10
交班日報表 Page 1 of 1
中分類==全部
一 今天的代支 0
十 今日的零用錢 0
一 外幣匯兌 0
合計 0
作廢的發票號碼 開立發票 0 張
作廢發票 0 張
製表者: a25005 Jimmy.Chang
查詢條件: 查詢依據: 入帳收入 列印項目: 服務項目 廳別: 入帳收入 查詢日期: 2026/05/16
```

## 操作備註

1. **Element UI 下拉已支援**：`ddl-options` 已可偵測 `el-select-dropdown`（標記 `elementui`）。DOM 結構：`div.el-select-dropdown > div.el-scrollbar__wrap > ul.el-select-dropdown__list > li > span`
2. **clearable 陷阱**：部分 Element UI select 的 `<i>` icon 在有值時點擊會清掉值。展開下拉應點 `//input` 而非 `//i`
3. **廳別必填**：不選廳別直接查詢無法產出報表
4. **列印項目實質必填**：有預設值「S：服務項目」但清空後查詢失敗，搭配 clearable 陷阱容易誤清
4. **iframe 動態生成**：查詢前 `reportIframe` 不存在，需等查詢完成後才能取 src
5. **PDF URL 含敏感 token**：iframe src 中的 accessToken 是完整 JWT，測試程式碼/日誌中注意不要外洩
6. **Export 按鈕**：⚠️ 未驗互動，推測為下載 Excel/PDF，檔案落在 Grid 節點
