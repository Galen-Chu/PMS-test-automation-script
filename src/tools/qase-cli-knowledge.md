# Qase CLI 工具知識庫

> `qase_cli.py` — Qase API CLI，管理測試案例、測試計畫與測試執行。

---

## 呼叫方式

```bash
# AI（Claude Code bash）
.venv/Scripts/python.exe tools/qase_cli.py <command> [options]

# 專案代碼預設 PMS，可用 -p 覆蓋
.venv/Scripts/python.exe tools/qase_cli.py -p CRM list-suites
```

**Token 來源**：自動從 `pytest.ini` 的 `QASE_API_TOKEN` 讀取，或環境變數 `$QASE_API_TOKEN`。

---

## 指令總覽

### 案例管理

| 指令 | 用途 | 範例 |
|------|------|------|
| `get-case <id>` | 查看單一案例（含 steps、preconditions） | `get-case 438` |
| `list-cases <suite_id>` | 列出 suite 下的案例（含 automation、params） | `list-cases 9` |
| `update-case <id>` | 更新案例（automation / field / params / steps） | `update-case 438 -a automated` |

**update-case 參數**：

```bash
# 設定自動化狀態
update-case 438 -a to-be-automated    # not-automated / to-be-automated / automated

# 設定任意欄位（可重複）
update-case 438 -f priority=2 -f layer=1

# 設定參數化資料
update-case 438 --params '{"房號":["101","102"]}'

# 設定 Gherkin steps
update-case 438 -s "Given 開啟訂房卡\nWhen 輸入房號\nThen 顯示房間資訊"
update-case 438 -sf steps.txt        # 從檔案讀取

# 跳過確認
update-case 438 -a automated -y
```

**list-cases 輸出**：標記 params 數量（`params:N`），方便篩選參數化案例。

### Suite 管理

| 指令 | 用途 | 範例 |
|------|------|------|
| `list-suites` | 列出所有 suite（含 cases_count、parent） | `list-suites` |

### Plan 管理

| 指令 | 用途 | 範例 |
|------|------|------|
| `list-plans` | 列出所有 plan（含 cases_count） | `list-plans` |
| `get-plan <id>` | 取得 plan 詳情與完整 case ID 清單 | `get-plan 4` |

**用途**：Plan 包含完整的 case ID 清單。Run 通常從 Plan 建立，透過 `get-plan` 可取得 run 的所有案例（含 untested）。

### Run 管理

| 指令 | 用途 | 範例 |
|------|------|------|
| `list-runs` | 列出 test runs（含統計：Total/Pass/Fail/Untested） | `list-runs --limit 10` |
| `get-run <id>` | 取得 run 詳情（狀態、統計、環境、里程碑） | `get-run 83` |
| `list-results <run_id>` | 列出 run 內已測試案例（去重取最新） | `list-results 83` |
| `run-untested <run_id>` | 列出 run 中未測試的案例（按 suite 分組） | `run-untested 83 --plan 4` |

**`run-untested` 詳細說明**：

```bash
# 自動偵測 plan（run 需有 plan_id）
run-untested 79

# 手動指定 plan（run 沒有 plan_id 時）
run-untested 83 --plan 4
```

輸出按 suite 分組，顯示案例標題、自動化狀態與參數組合測試進度。

邏輯：
1. 從 plan 取得完整案例清單
2. 從 run results 取得已測試的參數組合數（不去重，每筆 result = 一組參數）
3. 逐一取得案例 params，計算參數組合總數（笛卡爾積）
4. 若已測組合 < 總組合 → 列為 untested，顯示 `tested/total`

**Qase 參數化機制**：一個案例若有 `天數: [1天, 7天, 30天] × 間數: [1間]` = 3 組參數，在 run 中會產生 3 筆 result entries。Qase 的 run 統計（total/passed/untested）按參數組合計算，不是按唯一案例。

**已知限制**：
- Result API 不回傳具體使用了哪組參數，只能比對數量
- 若 run 無 plan_id，需手動 `--plan` 指定來源 plan
- Plan 與 run 的案例數可能略有差異（run 建立時可能剔除部分案例）
- 85 個案例需要逐筆 API 呼叫，耗時約 10-15 秒

### 共用參數

所有指令支援：
- `--json`：原始 JSON 輸出（適合程式處理）
- `-p <code>`：指定專案代碼（預設 PMS）

---

## Qase API Enum 對照

> 由實際 API 觀察推導，非官方文件。值可能因 Qase 版本更新而變動。

| 欄位 | 0 | 1 | 2 | 3 |
|------|---|---|---|---|
| automation | is-not-automated | to-be-automated | automated | — |
| priority | 未設定 | high | medium | low |
| case status | actual | draft | deprecated | — |
| run status | in_progress | passed | failed | interrupted |

**注意**：`severity` 和 `type` 無法透過 PATCH API 更新（API 回傳成功但值不變）。

---

## 與 Qase MCP 工具對照

| 功能 | 我們的 CLI | MCP 工具 | 備註 |
|------|-----------|---------|------|
| 查看/列出案例 | `get-case` / `list-cases` | `get_case` / `list_cases` | CLI 加了 params 顯示 |
| 更新案例 | `update-case` | `update_case` | MCP update_case 有 parsing bug |
| Suite | `list-suites` | `list_suites` / `get_suite` | — |
| Plan | `list-plans` / `get-plan` | `list_plans` / `get_plan` | — |
| Run | `list-runs` / `get-run` | `list_runs` / `get_run` | — |
| Run 結果 | `list-results` | `list_results` | — |
| 批次更新 | — | `bulk_create_cases` | 未整合，視需求加入 |
| 建立/刪除 | — | `create_*` / `delete_*` | CLI 偏向查詢+更新 |
| Defect | — | `list_defects` / `get_defect` | 未整合 |
| Milestone | — | `list_milestones` / `get_milestone` | 未整合 |
| QQL 搜尋 | — | `qql_search` | 未整合 |
| 提交結果 | — | `create_result` / `create_results_bulk` | 未整合，自動化回報用 |
| 環境 | — | `list_environments` | 未整合 |

**整合原則**：CLI 專注查詢 + 案例更新（autotest 日常工作），MCP 補充臨時查詢。建立/刪除等破壞性操作保留在 MCP（需額外確認）。

---

## 未整合功能（依優先度）

1. **`create_results_bulk`** — 自動化測試完後回報結果到 Qase run（高價值）
2. **`list-defects`** — 查詢相關缺陷（中價值）
3. **`qql-search`** — 複雜查詢（Qase server 穩定性待觀察）
4. **`list-environments`** — 查詢環境清單（低價值，偶爾用 MCP 即可）
5. **`list-milestones`** — 查詢里程碑（低價值）
