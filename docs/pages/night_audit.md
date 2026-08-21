# 夜間稽核（PMS0510010）

> 路徑：夜核 → 夜間稽核
> 程式代碼：PMS0510010
> SPA 導航：`//button[normalize-space()='夜核']` → `//span[@data-field-id='PMS0510010']`

---

## 佈局

```
夜間稽核(PMS0510010)
├── [資訊區] ─ 系統營業日期(rent_cal_dat)、主機日期(system_dat)、可夜核時間(can_nightrun_tim)、本次處理日期(batch_dat)、需跨日夜核(nightrun_must_tomorrow)
├── [檢查清單 Grid] ─ 6 欄（執行/群組代碼/執行結果/編號/說明/描述），含勾選欄位
├── [執行按鈕] ─ 執行夜核
└── [Tab: 已入住] ─ Grid（8 欄：房號/序/住客姓名/狀態/餘額/預付款餘額/C/O提醒/退房日期）
```

## 框架分布

| 區塊 | 框架 | 判斷依據 |
|------|------|---------|
| 資訊區 | Syncfusion | DatePicker、`data-field-id` |
| 檢查清單 Grid | EasyUI DataGrid | `datagrid-row-*`、editable checkbox |
| 已入住 Grid | EasyUI DataGrid | `datagrid-row-*` |

## 資訊區

| 元素 | data-field-id | 類型 | 狀態 | 備註 |
|------|---------------|------|------|------|
| 系統營業日期 | rent_cal_dat | Syncfusion DatePicker | DISABLED | |
| 主機日期 | system_dat | Syncfusion DatePicker | DISABLED | |
| 可夜核時間 | can_nightrun_tim | time input | DISABLED | |
| 本次處理日期 | batch_dat | Syncfusion DatePicker | enabled | 可修改 |
| 需跨日夜核 | nightrun_must_tomorrow | input | DISABLED | |

## 檢查清單 Grid（6 欄）

| 欄位 | 中文標題 |
|------|---------|
| — | 執行（勾選框） |
| group_cod | 群組代碼 |
| result | 執行結果 |
| item_no | 編號 |
| description | 說明 |
| remark | 描述 |

25 個檢查項目，全部 DISABLED（由系統自動檢查）。

## 執行按鈕

| 元素 | Locator | 備註 |
|------|---------|------|
| 執行 | `//button[normalize-space()='執行']` | ⚠️ 不可逆操作：中斷所有 PMS 系統，執行夜核，登出所有使用者 |

## 已入住 Tab Grid（8 欄）

| 欄位 | field | 中文標題 |
|------|-------|---------|
| — | ck | 勾選（editable） |
| room_nos | room_nos | 房號 |
| room_ser | room_ser | 序 |
| alt_nam | alt_nam | 住客姓名 |
| guest_sta | guest_sta | 狀態 |
| item_tot | item_tot | 餘額 |
| prepay_amt | prepay_amt | 預付款餘額 |
| co_rmk | co_rmk | C/O提醒 |
| aco_dat | aco_dat | 退房日期 |

## 操作備註

- **夜核流程**：檢查清單項目全部通過 → 點擊「執行」→ 確認提示 → 夜核完成 → 系統登出
- **執行前確認**：點擊執行後會跳出「將會中斷所有正在執行的PMS系統,確定要夜核嗎?」提示
- **異常處理**：如有 E(錯誤) 項目必須處理才能執行；W(警告) 可忽略繼續
- **檢查清單**：編號格式 A00##，25 個項目全部 DISABLED

### ⚠️ 未驗互動

- 執行按鈕（不可逆，會中斷所有 PMS 系統並登出使用者）
