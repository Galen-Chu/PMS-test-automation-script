# CLI 工具知識庫

> 整合自 CLI Guide、cli-research/ 研究文件與 ATHENA-DOM.md，作為 CLI 探索與自動化開發的單一參考來源。
> Qase CLI 工具另有獨立說明文件：`tools/qase-cli-knowledge.md`

---

## 一、CLI 能力現況

### 快速呼叫

專案內有兩個 wrapper，都是呼叫 selenium_cli.py：

| Wrapper | 環境 | 用法 |
|---------|------|------|
| `tools/cli` | AI（Claude Code / WSL bash） | `tools/cli scan --all -d "scope名"` |
| `tools\cli.bat` | 人（Windows PowerShell / cmd） | `tools\cli.bat scan --all -d "scope名"` |

**AI 一律用 `tools/cli`**（bash script），不需要 powershell.exe 包裝，引號只需一層 bash 規則。
以下範例統一用 `tools/cli` 寫法。

### 啟動方式

```
# 開新 Chrome（Selenium Hub URL 自動從 pytest.ini 讀取）
python tools/selenium_cli.py connect

# 接管已開的 Chrome（需先用 --remote-debugging-port=9222 啟動）
python tools/selenium_cli.py attach

# 手動指定 Hub（覆蓋預設值）
python tools/selenium_cli.py connect --hub http://localhost:4444

# Edge 版本（加 --edge）
python tools/selenium_cli.py connect --edge
python tools/selenium_cli.py attach --edge
```

### 參數解析優先序

CLI 指令的參數按以下順序解析（高優先蓋低）：
1. 命令列參數（`--hub`、`--username` 等）
2. 環境變數（`$SELENIUM_HUB` 等）
3. `pytest.ini` 的 `[pytest] env` 區段

已支援此機制的指令：`connect`、`login`、`restore-session`。
大部分情況下裸跑指令即可，pytest.ini 已有預設值。

### 指令總覽

| 類別 | 指令 | 用途 |
|------|------|------|
| 連線 | connect, attach, close | 啟動/附加/關閉瀏覽器 session |
| 導航 | nav, back | URL 導航（僅限外部頁面）、返回 |
| Session | save-session, restore-session, login | 保存/還原 cookie+sessionStorage、自動登入(含驗證碼 OCR) |
| 操作 | click, type, key, hover | 點擊、輸入、送鍵、懸停 |
| 查詢 | scan, find, get, text, attr, describe, diff, grid-headers, labels, ddl-options | 掃描元素、查找、讀值、狀態摘要、狀態比對、Grid 欄位名稱、UI 標籤文字、DDL 選項 |
| 產出 | pom-out | 將已驗證操作輸出為 locator + page method 程式碼 |
| 除錯 | shot, js, source, a11y | 截圖、執行 JS、保存原始碼、accessibility tree |
| 瀏覽器 | tabs, switch, url, title, wait | 分頁管理、等待元素 |

### 常用指令語法

```
# 頁面狀態
describe                          # 頁面摘要（heading、dialog、表格行數）
grid-headers                      # 列出所有 Grid/Table 的欄位 header 文字（用於確認 UI 顯示名稱）
labels                            # 列出所有 UI 標籤文字（span.truncate，用於確認中文欄位名稱）
labels -d                         # 限定 dialog scope
labels -d "名稱"                  # 限定指定 dialog
labels -p "panel"                 # 限定 EasyUI panel
ddl-options                       # 列出當前開啟的 DDL/combobox popup 選項（需先 click 開啟 DDL）
url / title                       # 當前 URL / 標題
tabs                              # 列出所有分頁

# 探索
scan                              # 全頁掃描互動元素 + XPath 建議
scan -d                           # 限定最上層 dialog（auto-detect，取 z-index 最高）
scan -d "名稱"                    # 限定指定 dialog
scan -p "panel"                   # 限定 EasyUI panel
scan -a                           # 含 links + labels
scan --vue                        # 掃描 Vue 自訂元件（data-v-* + 互動 class pattern）
find -x "xpath"                   # 找元素並顯示屬性
find -c "css"                     # CSS selector
diff                              # 第一次=存基準線，第二次=比對差異（追蹤 dialog/panel/tab/rows/popups 變化）

# 操作
click -x "xpath"                  # 點擊（scrollIntoView + retry 3 次，失敗報 BLOCKED + 元素/page 診斷）
click -x "xpath" --js             # 強制 JS click（繞過原生 click 檢查，僅在確認需要時使用）
click -x "xpath" --diff           # 點擊 + 自動比對前後差異（等同 diff → click → diff 三步合一）
type -x "xpath" -t "text"        # 輸入文字（預設先清空，失敗報 ERROR + 元素狀態診斷）
type -x "xpath" -t "text" --append # 不清空，追加輸入（同樣附帶失敗診斷）
type -x "xpath" -t "text" --enter  # 輸入後送 Enter
key enter/tab/escape              # 送特殊鍵（全域）
key escape -x "xpath"             # 送鍵到指定元素
hover -x "xpath"                  # 滑鼠懸停
wait -x "xpath" --timeout 10     # 等待元素出現

# Locator 來源（所有操作/查詢指令通用）
-x "xpath"                        # XPath
-c "css"                          # CSS selector
-xf file.txt                      # 從檔案讀 XPath（解決 shell 引號問題）

# pom-out（操作成功後產出 locator + page method）
pom-out --init --case 438 --title "住客新增車號"  # 初始化暫存檔
pom-out open_car_nos              # 自動加前綴（click→btn_/click_、type→input_/input_、get→text_/get_）
pom-out btn_confirm confirm_xxx   # 兩個參數 = 自訂 locator name + method name（override）
pom-out --show                    # 顯示暫存檔內容
pom-out --clear                   # 清空暫存檔

# 導航
nav <url>                         # URL 導航（僅用於非 SPA 頁面）
back                              # 上一頁
switch <index>                    # 切換分頁

# 除錯
shot --name xxx                   # 截圖（全頁）
shot -x "xpath" --name xxx        # 截圖（指定元素）
js "code"                         # 執行 JS
a11y                              # Accessibility tree
```

### 覆蓋度（vs 測試腳本操作模式）

**約 70% 可直接覆蓋**，已驗證的操作：
- 選單展開/頁面導航 → click data-field-id
- 搜尋/篩選 → type + click
- Tab 切換 → click tab id
- 工具列操作 → click data-field-id button
- Panel 關閉 → click title='關閉'
- 讀值 → get 指令

### 主要缺口

| 缺口 | 嚴重度 | 現況 | 替代方案 |
|------|--------|------|---------|
| EasyUI 設值不觸發 Vue | 高 | jQuery setValue 繞過 Vue observer | 無可靠方案，需研究 |
| Element UI v-model 綁定 | 高 | native setter + dispatchEvent 無效 | Selenium send_keys 可行，但 scrollable grid 內需先 scroll |
| 內建斷言機制 | 中 | 無 assert 指令 | js 讀值 + 人工比對 |
| Syncfusion popup 設值 | 中 | send_keys 不觸發篩選 | js dispatchEvent（已有 pattern） |
| EasyUI datagrid 列選取 | 中 | click cell 可觸發 row selection，diff 已可偵測 | 用 `//tr[contains(@class,'datagrid-row')][N]/td[@field='xxx']` 點擊，`click --diff` 驗證 |

---

## 二、三框架操作手冊

### 快速辨識

| 框架 | DOM 特徵 | scan 覆蓋 | 設值風險 |
|------|---------|----------|---------|
| **Syncfusion EJ2** | `data-field-id`、`e-` prefix class、`role="dialog"` | 正常 | 🟢 低 |
| **jQuery EasyUI** | `panel-title`、`datagrid-` prefix、`combobox-item` | 漏 `<a>` close | 🟡 中 |
| **Element UI** | `el-` prefix class、`el-scrollbar` | 漏 `<i>` icon | 🔴 高 |

### Syncfusion（主力框架）

**一般操作**：`type` 直接成功，Vue binding 正常觸發。

**DropDownList / SelectGrid 操作流程**（訂房公司等帶篩選的下拉）：
```
# 1. 開啟 DDL（click e-ddl span，不是 input）
click -x "//div[@data-field-id='acustCode']//span[contains(@class,'e-ddl')]"

# 2. 輸入篩選（popup 內的 filter input）
type -x "//input[contains(@class,'e-input-filter')]" -t "關鍵字"

# 3. 確認篩選結果
ddl-options                                                    # 列出選項文字 + 數量

# 4. 點擊選取（篩選後的 list item）
click -x "//li[contains(@class,'e-list-item')]"           # 只剩 1 筆時
click -x "//li[contains(text(),'目標文字')]"              # 多筆時用文字定位

# 4. DDL 自動關閉，值已選入
```

注意事項：
- 搜尋區和 dialog 可能有同名 `data-field-id` 的 DDL，用 `[last()]` 取 dialog 內的
- `type` 的 send_keys 可正常觸發篩選（訂房卡 acustCode 已驗證）
- 篩選可能是 server-side，結果數量不一定比全部少
- `diff` 可偵測 DDL 展開：`POPUPS dropdown/popup 1 → 2 (+1)`

### jQuery EasyUI

**Combogrid 搜尋**：
```
type -x input -t "keyword" --clear → key enter → js click 選取
```

**Textbox 設值**：結構特殊，visible input 被 hidden input 遮擋。
- 先嘗試 CLI type → 失敗 → JS setValue → 驗證 Vue binding
- ⚠️ jQuery setValue 可能不觸發 Vue observer

**Combobox**：visible `input.textbox-text` 可用 CLI type → `.combo-arrow` 開下拉 → js click 選項

**Panel 關閉**：scan 漏 `<a>`，用 `find -x "//a[contains(@class,'panel-tool-close')]"`

**DataGrid**：
- **列選取**：click cell 可觸發 row selection（`datagrid-row-selected` class），`click --diff` 可偵測行選取變化
- 穩定定位方式：用 `//td[@field='room_nos' and normalize-space()='526']`（按欄位值定位）或 `(//tr[contains(@class,'datagrid-row')])[N]/td[@field='xxx']`（按索引定位）
- ⚠️ **不要用 `tr` 的 `id` 做 locator**：`gid_641_datagrid-row-r5-2-0` 中的 grid ID 和 row index 是動態生成的，頁面重新載入或資料變化後會失效
- 搜尋篩選：頂部搜尋欄可用
- 底色偵測：`rgb(252, 237, 218)` = 合約價
- frozen+regular table 產生多個同 field td，前幾個常是 0x0（click 自動跳過）

**Panel/Window**：
- 不使用 `role=dialog`，accessibility tree 看不到
- 辨識：`.panel.window:visible` 或 `.panel-title`
- 關閉後 DOM 不移除（display:none），殘留 panel+mask 會阻擋後續操作 → 需切頁重置

**按鈕前綴**：data-field-id 可能帶程式代碼（如 `PMS0210020_doSearch`）

### Element UI

**el-input 設值**：優先 Selenium type（send_keys），不要用 JS native setter。
- JS native setter + dispatchEvent('input') 不觸發 Vue data 更新
- Syncfusion textarea 正常，三框架 Vue 綁定機制不同

**scrollable grid 內 el-input**：元素可能不在 viewport，需先 JS scroll into view

**關閉 icon**：scan 漏 `<i>`，用 `find -x "//i[contains(@class,'el-icon-close')]"`

---

## 三、scan 盲區與補強

scan 預設掃描 `input/button/select/textarea`，以下需額外處理：

| 元素類型 | 框架 | 定位方式 |
|---------|------|---------|
| `<a>` close 連結 | EasyUI | `//a[contains(@class,'panel-tool-close')]` |
| `<i>` icon | Element UI | `//i[contains(@class,'el-icon-close')]` |
| `<span>` 按鈕 | 通用 | `//span[contains(@class,'button-add--s')]` |
| `<label>` 可點擊 | 通用 | `//label[@data-field-id='xxx']` |
| `<button><img>` 圖示 | 通用 | `//button[child::img[@alt='save']]` |
| `<div>` grid cell | EasyUI | `//td[@field='xxx']` |
| Vue 自訂元件 | Vue | `scan --vue`（class 含 card/item/tab/menu 等 pattern） |

**已補強**：
- `scan --all`：加入 `<a>` 和 `<label>` 掃描
- `scan --tag`：過濾指定 tag 類型
- `scan --vue`：掃描帶 `data-v-` 屬性且 class 含互動 pattern（card/item/tab/menu/option 等）或 cursor:pointer 的非標準元素，輸出 `[Vue Components]` 區段。同 class 只取一個代表，避免重複
- `[Clickable]` 區段：自動掃描 `<a>` close/tool、`<i>` icon、`<span>` button、`<label>` 可點擊
- `[Interactive Roles]` 區段：掃描帶 role 屬性的非標準元素

**`scan --vue` 判讀**：
- class 含 `card`/`item`/`list` → 通常是容器，但如果有 `cursor:pointer` 或 `@click` 則整個容器可點擊（如 `.card--room`）
- class 含 `btn`/`action`/`trigger` → 互動元素，記錄到元素清單
- 同 class 多個實例 → 參數化候選（`%s` 佔位）
- 無法從 class 判斷 → 用 `find -x` 確認是否有 click handler 或 cursor style

---

## 四、已知陷阱

| 陷阱 | 說明 | 處理方式 |
|-----|------|---------|
| Syncfusion popup blur | 手動點瀏覽器視窗關閉 popup | CLI 操作不觸發 blur |
| Hub session 超時 | 5 分鐘無活動斷線 | 長操作穿插 describe |
| 多 panel close | 多 panel 時 close 需用 index | `(//a[...panel-tool-close...])[N]` |
| EasyUI textbox 不可互動 | CLI type 報 "not interactable" | 結構特殊，JS setValue 不觸發 Vue |
| td 多匹配隱藏元素 | frozen+regular table 多個同 field td | click 自動跳過 0x0 元素 |
| 面板關閉 DOM 殘留 | display:none 但 mask 阻擋操作 | 切頁重置 |
| SPA 選單原地跳轉失敗 | `a.sub-menu-item` 的 CLI click 不觸發 Vue router | 改用 `openBlankToXXX` 開新分頁 |
| js return 行為不一致 | 回傳值有時被包成 JSON 物件 | 讀值後先 typeof 確認 |
| 按鈕條件性消失 | doChangeMode 在編輯模式後不出現 | 操作前先 describe 確認狀態 |
| 瀏覽器原生 UI | Chrome 密碼提示等 OS 層級 UI | Chrome options 源頭禁掉，不要 DOM 操作 |
| Dialog 關閉分兩類 | EasyUI Panel 用 `<a>` close，Syncfusion Dialog 用 `<button>` close | 先試 `//button[@title='關閉']`（Syncfusion），再試 `(//div[contains(@class,'panel-title') and text()='名稱']/ancestor::div[contains(@class,'panel')])[1]//a[contains(@class,'panel-tool-close')]`（EasyUI，限定 scope） |
| Element UI el-select | click input 開下拉後，下拉會在下次操作時消失 | click input 後**立即** click 選項，中間不能做 find/describe 等其他操作。選項 XPath：`(//div[contains(@class,'el-select-dropdown') and not(contains(@style,'display: none'))]//span[text()='選項文字']/parent::li)[last()]` |
| EasyUI Panel close [last()] 陷阱 | 多 panel 堆��時 `[last()]` 可能關錯 panel | 用 panel title 限定：`(//div[contains(@class,'panel-title') and text()='入帳']/ancestor::div[contains(@class,'panel')])[1]//a[contains(@class,'panel-tool-close')]` |
| Alert 預設取消 | 探索時 Alert 可能是破壞性操作確認 | 一律先點「取消」，只做 find 不做確認；記錄 Alert 內容到文件 |
| Toggle 按鈕 | 按鈕文字/行為依狀態變化（如 指定/取消公帳號） | 操作前先讀按鈕 text 確認當前狀態 |

---

## 五、導航與環境

### Session 管理（標準流程）

**首次建立 session**：
```
1. connect（或 connect --hub http://localhost:4444）
2. login --username X --password X --base-url ... --redirect-url ... [--company "公司名"]
```
login 成功後自動存 session（cookies + sessionStorage → browser_session.json），不需手動 save-session 或進入 PMS。

**之後每次探索**：
```
1. connect（或 connect --hub http://localhost:4444）
2. restore-session  ← 注入 session 後自動讀 WEB_URL + ENV_NUM 跳到 PMS landing page
3. 透過 SPA 選單導航到目標頁面
```

restore-session 會從 pytest.ini 讀 WEB_URL + ENV_NUM 直接導航到 PMS，不依賴 save-session 時的 URL。換環境只要重新 login 即可。

### SPA 內部導航

⚠️ **在 PMS SPA 裡面禁止用 `nav <url>` 跳頁**。直接 URL 導航會導致 session 狀態不一致（heading 不更新、頁面內容錯誤、「請重新登入」）。`nav` 只用於外部頁面（登入頁等非 SPA 頁面）。

PMS 左側選單結構：頂層是 `<button data-dropdown="模組名">`（模組），展開後子項目每個功能是 `<a class="sub-menu-item">`，內含：

| 元素 | 定位 | 行為 |
|------|------|------|
| `<span>` 功能名稱 | `//span[normalize-space()='功能名']` | **click 可觸發 SPA 路由切換**（同頁，不開新分頁） |
| `<a>` openBlank | `data-field-id="openBlankToXXX"` | 開新分頁載入完整頁面（備用方案） |

導航步驟（優先用 SPA 路由，與測試專案一致）：
```
1. click 頂層模組按鈕：//button[@data-dropdown='接待']
2. click 功能名稱 span：//span[normalize-space()='綜合櫃檯']
3. describe 確認已到目標頁面
```

備用方案（SPA 路由失敗時）：用 openBlank 開新分頁 → `tabs` → `switch`。

### QA 環境差異

- 登入後有「選公司」步驟（公司環境沒有），login 指令支援 `--company` 參數
- EIP 首頁的 PMS 入口是 `<a>` 文字連結，不是 `.systemcardtest` 卡片

### JS 使用原則

導航和操作都優先用 CLI，JS 只在最後手段時使用。原因：過度依賴 JS 會掩蓋 CLI 能力缺口。

| 用途 | 判斷 |
|------|------|
| js 讀值 | ✅ 合理 |
| js 操作元素 | ⛔ 先嘗試 CLI，失敗後記錄缺口再用 JS |
| js 處理 scan 盲區 | ⚠️ 可接受，但要記錄 scan 漏了什麼 |

---

## 六、設計原則

**CLI 與專案框架兼容**：CLI 探索的操作方式要能直接轉化為腳本。CLI API 語義必須跟專案 Selenium helper 保持一致，底層邏輯要用專案可複用的方式寫。

**為什麼**：CLI 的定位是 prototype → 轉化為腳本。阻抗不匹配會增加轉化成本。

---

## 七、diff 指令

### 用途

偵測操作前後的頁面狀態變化。特別適合：
- 探索 click 後不知道發生了什麼（dialog 出現？欄位解鎖？欄位值被改了？）
- 編輯模式切換時哪些元素變化
- Grid 行數增減偵測
- 報表查詢後 iframe 是否載入
- Element UI clearable 陷阱——值被清掉時立刻看到

### 使用方式

**快捷方式（推薦）**：用 `--diff` flag 直接掛在操作指令上，一步完成基準線+操作+比對：

~~~
click -x "xpath" --diff              # 存基準線 → click → 等 0.3s → 比對差異
click -x "xpath" --diff --wait 15    # 同上，但用顯示等待最多 15 秒（每 0.5s 輪詢，偵測到變化立即回傳）
~~~

`--wait` 適用於非同步操作（查詢報表、儲存等需要等待後端回應的場景）。不加 `--wait` 時只等 0.3 秒，適合即時反應的操作（開 dialog、切 tab）。

`--diff` 是泛用 wrapper（`_with_diff`），未來其他狀態變更指令也會支援。

**手動方式**：分別呼叫 diff 指令，適合多步驟操作或需要自己控制等待時機的場景：

~~~
diff                # 第一次呼叫 → 存基準線（印出元素數、dialog 名稱、row count）
# ... 做操作（多步驟 / type + click 組合等）...
# ... 等待非同步操作完成 ...
diff                # 第二次呼叫 → 比較差異（印出變化後刪除基準線）
~~~

第二次呼叫後基準線自動刪除，第三次呼叫會重新存基準線。

**場景選擇**：

| 場景 | 建議方式 |
|------|---------|
| 點按鈕開 dialog / 切 tab | `click --diff` |
| 查詢報表、儲存等非同步操作 | `click --diff --wait 15` |
| 多步驟操作（先填欄位再送出） | 手動 `diff` → 操作 → `diff` |

### 追蹤項目

| 追蹤項 | 偵測方式 | 輸出格式 |
|--------|---------|---------|
| Dialog / Panel 出現消失 | 比對可見 dialog/panel 名稱集合 | `NEW dialog:名稱` / `GONE panel:名稱` |
| Alert | 比對 alert 文字 | `ALERT: 文字內容` |
| Tab 切換 | 比對 active tab 文字 | `TAB: 彙總 → 明細` |
| 元素出現/消失 | 比對 `data-field-id` 元素集合 | `NEW button:doSave` / `GONE button:doChangeMode` |
| 元素啟用/禁用 | 比對 disabled 狀態 | `ENABLED: x, y, z` / `DISABLED: a, b, c` |
| **欄位值變化** | 比對 `textContent` / `value` | `batch_dat [查詢日期] (input): 2026/05/16 → 2026/05/19` |
| Table row count | 比對 EasyUI / Syncfusion / total row 數量 | `ROWS: total grid 15 → 18 (+3)` |
| Popup 開關 | 比對 `.e-popup-open` 數量 | `POPUPS: dropdown/popup 0 → 1 (+1)` |
| Grid 行選取 | 比對 `datagrid-row-selected` / `.e-row.e-active` / `.my-row-selected` 行 ID 集合 | `SELECTION grid:selected row 564, deselected row 563` |
| **iframe 出現/消失/src 變化** | 比對可見 iframe 的 id 和 src | `NEW iframe:reportIframe` / `IFRAME: reportIframe src changed` |

### 值變化輸出格式

輸出包含 field ID、UI 標籤（有 `<label>` 時顯示）、元素類型：

~~~
  VALUES:  (3 fields)
    查詢 (button): 2 → 3
    batch_dat [查詢日期] (input): 2026/05/16 → 2026/05/19
    co_usr [結帳者] (input): (empty) → admin
~~~

- `[查詢日期]`：從相鄰 `<label>` 自動擷取的中文名稱
- `(input)` / `(button)`：元素類型，用於區分真正的欄位值變化和按鈕文字噪音
- `undefined_doSearch` / `undefined_doClear` 等 dfid 自動映射為 `查詢` / `清除`

### Clickable 元素 td context

Grid 行內的 clickable 元素（`<span>/<i>/<label>` 等帶 `data-field-id`）會附帶 parent `<td>` 的 `data-field-id` 作為上下文，避免同名元素碰撞。

例如：`GONE label:openPreauth (in precredit_amt)` 表示 `precredit_amt` 欄位內的 `openPreauth` label 消失。

### Baseline 訊息

存基準線時會顯示完整上下文：
~~~
Baseline saved: 65 elements, 1 dialogs
  Dialogs: 房間細節
  Panels: 房間細節
  Active tab: 彙總
  Table rows: EasyUI 2, total 15
~~~

### 已知限制

- **只追蹤有 `data-field-id` 的元素**：沒有 `data-field-id` 的按鈕（如搜尋區、選單）不在追蹤範圍
- **值截斷 30 字元**：欄位值只取前 30 字元比對，超長值可能誤判為相同
- **EasyUI row count 已去重**：frozen/regular table 分裂導致的雙倍計數已修正，scan/describe/diff 均按 unique `datagrid-row-index` 去重
- **row count 是全域計數**：多個 Grid 的行數會加總，無法區分是哪個 Grid 變化
- **自訂 table 需用 total count**：部分 Grid 不用 EasyUI/Syncfusion 標準結構（如綜合櫃台的住客 Grid 用 `roomDetail-grid`），只有 total count 能抓到
- **iframe src 截斷 80 字元**：用於比對是否變化，不顯示完整 URL
- **行選取偵測的行 ID 是動態的**：`SELECTION` 輸出中的行 ID 來自 DOM 的 `data-uid`，頁面重載後會變化。偵測的是「選取狀態變化」而非「哪一筆資料被選」，僅供探索時確認操作生效用
- **Element UI popup 部分追蹤**：`el-select-dropdown`（下拉選單）和 `el-picker-panel`（日期面板）已追蹤；`el-popper`（MessageBox 等）和 `el-message-box` 仍不追蹤
- **`--wait` 在第一個變化就返回**：如果 DISABLED 先出現，後續的 ALERT 或 iframe 變化可能漏掉。非同步操作建議用手動 `diff` → 操作 → sleep → `diff`

---

## 八、pom-out 指令

### 用途

CLI 操作驗證成功後，將 locator + page method 程式碼輸出到暫存檔 `tools/pom_output.py`。核心原則：**不自動記錄操作歷史**（錯誤操作會汙染），只在確認操作正確後明確輸出。

### 追蹤機制

`click`、`type`、`get` 三個指令成功執行後，自動將操作類型和 XPath 寫入 `tools/.last_op.json`。`pom-out` 讀取此檔進行推導。

### 使用流程

```
# 1. 初始化暫存檔（開始新案例時）
pom-out --init --case 438 --title "住客新增車號"

# 2. CLI 操作驗證成功
click -x "//span[@data-field-id='openCarNosDialog']"
# → Clicked: //span[@data-field-id='openCarNosDialog']

# 3. 輸出 locator + page method（只給 base name，前綴自動加）
pom-out open_car_nos
# → Added: btn_open_car_nos (click) → pom_output.py

# 4. 繼續下一步操作...
type -x "//div[@data-field-id='carNos']//textarea" -t "ABC-1234"
pom-out car_nos

# 5. 查看目前累積的產出
pom-out --show

# 6. 案例轉化完成後清空
pom-out --clear
```

### 推導規則

| 操作類型 | locator 前綴 | method 前綴 | method body |
|---------|-------------|------------|-------------|
| click | `btn_` | `click_` | `self.click(self.locator.{name}); return self` |
| type | `input_` | `input_` | `self.input_with_clear(self.locator.{name}, value); return self` |
| get | `text_` | `get_` | `return self.driver.find_element(*self.locator.{name}).get_attribute('value')` |

前綴是慣例建議，使用者命名時可自行決定（如 confirm 按鈕用 `btn_car_nos_confirm`）。

### 暫存檔格式

`pom_output.py` 分為 Locators 和 Page Methods 兩區，`pom-out` 自動將 locator 插入 Locators 區尾、method 插入 Page Methods 區尾。案例組裝完成後用 `--clear` 清空。

### 指令參考

| 指令 | 用途 |
|------|------|
| `pom-out <base_name>` | 自動加前綴，推導並追加 |
| `pom-out <locator_name> <method_name>` | 自訂命名（override） |
| `pom-out --init [--case N] [--title "..."]` | 初始化暫存檔（含 header） |
| `pom-out --show` | 顯示暫存檔內容 |
| `pom-out --clear` | 清空暫存檔 |

