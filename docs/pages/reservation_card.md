# 訂房卡（PMS0110040）

> 路徑：訂房 → 訂房卡
> 程式代碼：PMS0110040
> SPA 導航：`//button[normalize-space()='訂房']` → `//span[normalize-space()='訂房卡']`

---

## 佈局

```
訂房卡(PMS0110040)
├── [搜尋區] ─ C/I日期、C/O、住客姓名、訂房卡號、速查、狀態 + 查詢模式切換
├── [操作列] ─ 瀏覽 / 線上繳款單 / 匯出 Excel
├── [列表 Grid] ─ Syncfusion Grid，36 欄（訂房卡號、狀態、住客姓名、C/I、C/O...）
│   └── 每列：[鉛筆] 編輯按鈕 → 開啟訂房卡 dialog
└── [訂房卡 Dialog] ─ Syncfusion Dialog（role="dialog"）
    ├── [工具列] ─ 排房 / 訂房確認書 / 檢視R卡 / 訂房明細 / 簡訊 / E-mail / 分帳規則 / 旅客登記卡 / Pre-CheckIn / 備品批次 / 線上繳款單
    ├── [操作按鈕] ─ 儲存(save) / 儲存並新增(saveAndCreate) / 複製(copy) / 異動紀錄(doOpenChangeLogDialog)
    ├── [表單區] ─ 上半部，三個 tab 共用
    │   ├── [主檔] ─ 狀態(orderStatus)、姓名(altName)、稱謂(saluteCodGuest)、狀態碼(statusCode)、VIP(vipStatus)
    │   ├── [公司區] ─ 訂房公司(acustCode)、業務員(salesCode)、聯絡人(attenName/attenBy)、稱謂(saluteCode)
    │   ├── [聯絡區] ─ 手機(mobileNos)、保證(guarenteeType)、Email(email)、電話(officeTel)
    │   ├── [團體區] ─ 團號(groupNos)、秘書(secretaryCode)
    │   ├── [勾選區] ─ Fix Rate(fixedOrder) / 印房租(isPrtrent) / 電話限撥(telTce) / 勿擾(dndCode)
    │   ├── [唯讀區] ─ 會員編號(showCode) / 會員類別(memberTypeName) / 身分識別(identifyCode/identifyNos) / 人數(peopleQuantity)
    │   ├── [確認區] ─ 確認(confirmStatus) / 使用公帳號(masterStatus) / Pre-C/I(preCi)
    │   └── [備註] ─ 訂房備註(orderRemark) textarea
    ├── [... 按鈕群] ─ 開啟子 dialog
    │   ├── altNameBtn → 住客歷史 (EasyUI Panel) ✅ 已驗
    │   ├── acustCodeBtn → 商務公司維護 (EasyUI Panel) ✅ 已驗
    │   ├── orderRemark → 訂房備註 (Syncfusion Dialog) ✅
    │   ├── linkNosDialog → 關聯單號 (EasyUI Panel) ✅
    │   ├── roomStatusDialog → 訂單資訊 (Syncfusion Dialog) ✅ ⚠️名稱不一致
    │   ├── guideDialog → 領隊資料 (Syncfusion Dialog) ✅
    │   ├── ptvDialog → PTV (Syncfusion Dialog) ✅
    │   ├── focDialog → FOC (Syncfusion Dialog) ✅
    │   └── banlanceAmount → 開班作業 PMS0310060 (EasyUI Panel) ✅ ⚠️子程式邊界
    ├── [金額彙總區] ─ 房租(sumRentTotal) / 服務費(sumServTotal) / 其他費用(sumOtherTotal) / ADD(sumAddExtraTotal) / 總金額(generalTotal) / 應收訂金(orderDeposit) / 已付訂金(banlanceAmount) / 總間數(sumRoomTotal)
    └── [Tab 區]
        ├── [彙總 tab] (tab-Summary) ─ Grid #1: 23 欄彙總明細
        │   └── 每列：[鉛筆] 編輯 + [垃圾桶] 刪除
        ├── [明細 tab] (tab-Detail) ─ Grid #2: 26 欄逐筆明細（多 入住/房號/住客姓名/入住時間/退房時間/住房掛帳）
        │   └── 每列：[鉛筆] 編輯 + [垃圾桶] 刪除
        └── [Profile Notes tab] (tab-Profile) ─ Grid #3: 2 欄（姓名 | Profile Notes）
```

## 框架分布

| 區塊 | 框架 | 依據 |
|------|------|------|
| 搜尋區 | Syncfusion | `data-field-id` input + button |
| 列表 Grid | Syncfusion | `e-grid` class，`td[@field]` |
| 訂房卡 Dialog | Syncfusion | `role="dialog"`，`data-field-id` 全覆蓋 |
| 表單區 | Syncfusion | `data-field-id` input/checkbox/dropdown |
| 彙總/明細 Grid | Syncfusion | `td[@field]`，grid command button |
| 商務公司維護 | **EasyUI + Element UI** | `panel-title`、`_easyui_textbox_input`、`el-` class |
| 住客歷史 | **EasyUI + Syncfusion** | `panel-title`、`_easyui_textbox_input`（combobox 多數）、`data-field-id`（按鈕） |

## 元素清單

### 搜尋區

| 元素 | 類型 | Locator | 備註 |
|------|------|---------|------|
| C/I 日期 | input | `//div[@data-field-id='checkinDate']//input` | DateTimePicker |
| C/O 日期 | input | `//div[@data-field-id='checkoutDate']//input` | DateTimePicker |
| 住客姓名 | input | `//div[@data-field-id='guestName']//input` | |
| 訂房卡號 | input | `//div[@data-field-id='ikey']//input` | |
| 速查 | input | `//div[@data-field-id='quickSearch']//input` | 公司/聯絡人/卡號/團號/網訂編號 |
| 狀態 | input | `//div[@data-field-id='orderStatus']//input` | DropDownList |
| 查詢模式 | span | `//div[@data-field-id='querySets']//span` | 一般模式/進階模式 |
| 搜尋 | button | `//div[@data-field-id='searchButton']//button` | |
| 清除 | button | `//div[@data-field-id='clearButton']//button` | |
| 展開/收合 | button | `//div[@data-field-id='dropdownButton']//button` | |
| 設定 | button | `//div[@data-field-id='querySetsSettingButtohn']//button` | typo 注意：Buttohn |

### 操作列

| 元素 | 類型 | Locator | 備註 |
|------|------|---------|------|
| 瀏覽 | button | `//div[@data-field-id='browse']//button` | |
| 線上繳款單 | button | `//div[@data-field-id='payFolio']//button` | |
| 匯出 Excel | button | `//div[@data-field-id='excelExport']//button` | ⚠️ 未驗互動 |

### 列表 Grid（36 欄）

| 顯示名稱 | @field | 備註 |
|----------|--------|------|
| 訂房卡號 | ikey | |
| 網訂編號 | rvreserveNos | |
| 訂房 | orderQuantity | |
| 狀態 | orderStatus | |
| 住客姓名 | guestName | |
| C/I | checkinDate | |
| C/O | checkoutDate | |
| 計價房型 | useCode | |
| 使用房型 | roomCode | |
| 房價代號 | rateCode | |
| 天數 | days | |
| 訂房公司 | acustName | |
| 聯絡人 | attenName | |
| 房號 | roomNos | |
| 單價 | rentAmount | |
| 關聯單號 | linkNos | |
| 團號 | groupNos | |
| 種類 | guestWay | |
| 訂房來源 | sourceType | |
| 業務員 | salesCode | |
| 公帳號 | masterNos | |
| 訂房類別 | guarenteeType | |
| 是否確認 | confirmStatus | |
| 市場類別 | guestType | |
| 訂房備註 | orderRemark | |
| 聯絡人電話 | attenHomeTel | |
| 聯絡人手機 | attenMobileNos | |
| 聯絡人公司電話 | attenOfficeTel | |
| 聯絡人傳真 | attenFaxNos | |
| 新增日期 | insertDate | |
| 新增者 | insertUser | |
| 修改日期 | updateDate | |
| 修改者 | updateUser | |
| 取消日期 | cancelDate | |
| 取消者 | cancelUser | |
| 取消原因 | cancelRemark | |

### 訂房卡 Dialog — 工具列

| 元素 | 類型 | Locator | 備註 |
|------|------|---------|------|
| 排房 | button | `//div[@data-field-id='doOpenRoomAssignDialog']//button` | ⚠️ 未驗互動 |
| 訂房確認書 | button | `//div[@data-field-id='doOpenReportDialog']//button` | ✅ 開啟列印 dialog |
| 檢視 R 卡 | button | `//div[@data-field-id='doOpenImageRcardPrintDialog']//button` | ⚠️ 前置條件：需有住客資料，否則 alert |
| 訂房明細 | button | `//div[@data-field-id='doOpenDtDetailDialog']//button` | ⚠️ 未驗互動 |
| 簡訊 | button | `//div[@data-field-id='doOpenSMSDialog']//button` | ⚠️ 需先選一筆彙總明細，否則 alert「請選擇一筆資料」 |
| E-mail | button | `//div[@data-field-id='doOpenEmailDialog']//button` | ✅ 開啟 E-mail panel |
| 分帳規則 | button | `//div[@data-field-id='doOpenSubAccountDialog']//button` | ✅ 開啟分帳規則 panel |
| 旅客登記卡 | button | `//div[@data-field-id='doOpenReportRcard']//button` | ✅ 開啟旅客登記卡 panel（+ 報表測試環境選擇 panel） |
| Pre-CheckIn | button | `//div[@data-field-id='doOpenPreCheckIn']//button` | ✅ 開啟 Pre-C/I dialog |
| 備品批次 | button | `//div[@data-field-id='doOpenBatchSpareInsert']//button` | ✅ 開啟備品批次新增 dialog |
| 線上繳款單 | button | `//div[@data-field-id='doOpenPayFolioDialog']//button` | ⚠️ 前置條件：需設定應收訂金，否則 alert |

### 訂房卡 Dialog — 操作按鈕

| 元素 | 類型 | Locator | 備註 |
|------|------|---------|------|
| 儲存 | button | `//div[@data-field-id='save']//button` | ⚠️ 未驗互動（不可逆） |
| 儲存並新增 | button | `//div[@data-field-id='saveAndCreate']//button` | ⚠️ 未驗互動（不可逆） |
| 複製 | button | `//div[@data-field-id='copy']//button` | ⚠️ 未驗互動（不可逆） |
| 異動紀錄 | button | `//div[@data-field-id='doOpenChangeLogDialog']//button` | ⚠️ 未驗互動 |
| 關閉 | button | `//button[@title='關閉']` | |

### 訂房卡 Dialog — 表單區（三 tab 共用）

| 元素 | 類型 | Locator | 已驗 | 備註 |
|------|------|---------|------|------|
| 狀態 | dropdown | `(//div[@data-field-id='orderStatus']//span[contains(@class,'e-ddl')])[last()]` | ✅ | ⚠️ 搜尋區有同名 multiselect，必須加 `e-ddl` + `[last()]` |
| 姓名 [...] | button | `//div[@data-field-id='altNameBtn']//button` | ✅ 開啟住客歷史 | |
| 姓名 | select | `//div[@data-field-id='altName']//input` | | DropDownList |
| 稱謂 | input | `//div[@data-field-id='saluteCodGuest']//input` | | 唯讀 |
| 狀態碼 | input | `//div[@data-field-id='statusCode']//input` | | 唯讀 |
| VIP | input | `//div[@data-field-id='vipStatus']//input` | | 唯讀 |
| Fix Rate | checkbox | `//div[@data-field-id='fixedOrder']//input` | | |
| 印房租 | checkbox | `//div[@data-field-id='isPrtrent']//input` | | |
| 電話限撥 | checkbox | `//div[@data-field-id='telTce']//input` | | |
| 勿擾 | checkbox | `//div[@data-field-id='dndCode']//input` | | |
| 團號 | input | `//div[@data-field-id='groupNos']//input` | ✅ type+get | Syncfusion textbox |
| 訂房公司 [...] | button | `//div[@data-field-id='acustCodeBtn']//button` | ✅ 開啟商務公司 | |
| 訂房公司 | dropdown | `//div[@data-field-id='acustCode']//span` | | |
| 業務員 | select | `//div[@data-field-id='salesCode']//input` | | DropDownList |
| 聯絡人 | input | `//div[@data-field-id='attenName']//input` | | |
| 聯絡人 [...] | button | `//div[@data-field-id='attenName']//button` | | DISABLED |
| 窗口來源 | dropdown | `//div[@data-field-id='attenBy']//span` | | |
| 稱謂(聯絡人) | select | `//div[@data-field-id='saluteCode']//input` | | DropDownList |
| 手機 | input | `//div[@data-field-id='mobileNos']//input` | | |
| 保證 | select | `//div[@data-field-id='guarenteeType']//input` | | DropDownList |
| Email | input | `//div[@data-field-id='email']//input` | | |
| 電話 [...] | button | `//div[@data-field-id='officeTel']//button` | | |
| 電話 | input | `//div[@data-field-id='officeTel']//input` | | |
| 會員編號 | input | `//div[@data-field-id='showCode']//input` | | DISABLED |
| 會員類別 | input | `//div[@data-field-id='memberTypeName']//input` | | DISABLED |
| 身分識別類別 | input | `//div[@data-field-id='identifyCode']//input` | | DISABLED |
| 身分識別編號 | input | `//div[@data-field-id='identifyNos']//input` | | DISABLED |
| 秘書 | select | `//div[@data-field-id='secretaryCode']//input` | | DropDownList |
| 確認 | checkbox | `//div[@data-field-id='confirmStatus']//input` | | |
| 使用公帳號 | checkbox | `//div[@data-field-id='masterStatus']//input` | | |
| Pre-C/I | checkbox | `//div[@data-field-id='preCi']//input` | | DISABLED |
| 人數 | input | `//div[@data-field-id='peopleQuantity']//input` | | DISABLED |
| 訂房備註 [...] | button | `//div[@data-field-id='orderRemark']//button` | | |
| 訂房備註 | textarea | `//div[@data-field-id='orderRemark']//textarea` | | |
| 關聯單號 [...] | button | `//div[@data-field-id='linkNosDialog']//button` | | |
| 鎖控 [...] | button | `//div[@data-field-id='roomStatusDialog']//button` | | |
| 領隊 [...] | button | `//div[@data-field-id='guideDialog']//button` | | |
| PTV [...] | button | `//div[@data-field-id='ptvDialog']//button` | | |
| FOC [...] | button | `//div[@data-field-id='focDialog']//button` | | |
| 已付訂金 [...] | button | `//div[@data-field-id='banlanceAmount']//button` | | |

### 訂房卡 Dialog — 金額彙總

| 元素 | 類型 | Locator | 備註 |
|------|------|---------|------|
| 房租 | input | `//div[@data-field-id='sumRentTotal']//input` | |
| 服務費 | input | `//div[@data-field-id='sumServTotal']//input` | |
| 其他費用 | input | `//div[@data-field-id='sumOtherTotal']//input` | |
| ADD | input | `//div[@data-field-id='sumAddExtraTotal']//input` | |
| 總金額 | input | `//div[@data-field-id='generalTotal']//input` | |
| 應收訂金 | input | `//div[@data-field-id='orderDeposit']//input` | |
| 已付訂金 | input | `//div[@data-field-id='banlanceAmount']//input` | DISABLED |
| 總間數 | input | `//div[@data-field-id='sumRoomTotal']//input` | |

### 訂房卡 Dialog — Tab

| Tab | ID | Grid 欄位數 | 備註 |
|-----|-----|-----------|------|
| 彙總 | tab-Summary | 23 | 預設 tab |
| 明細 | tab-Detail | 26 | 多 入住狀態/房號/住客姓名/入住退房時間/住房掛帳 |
| Profile Notes | tab-Profile | 2 | 姓名 + Profile Notes |

### 彙總 Grid 欄位（Grid #1）

| 顯示名稱 | @field | 備註 |
|----------|--------|------|
| 訂房來源 | sourceType | |
| 單日房租 | rentAmount | |
| 服務費 | servAmount | |
| 小計 | subTotal | |
| 狀態 | orderStatus | |
| 入住日期 | ciDate | 含星期 |
| 天數 | days | |
| 退房日期 | coDate | 含星期 |
| 房價代號 | rateCode | |
| 計價 | useCode | |
| 使用 | roomCode | |
| 間數 | groupOrderQuantity | |
| 大人 | groupAdultQuantity | |
| 小孩 | groupChildQuantity | |
| 房租 | groupRentTotal | |
| 服務費 | groupServTotal | |
| 其他 | groupOtherTotal | |
| ADD | addExtraFee | 是/否 |
| ADD | groupAddExtraTotal | 金額 |
| 小計 | groupSubtotal | |
| 鎖控代號 | blockCode | |
| 佣金% | commisRate | |
| 市場 | guestType | |

### 明細 Grid 額外欄位（Grid #2，相較彙總多出）

| 顯示名稱 | @field | 備註 |
|----------|--------|------|
| 狀態 | orderStatus | |
| 入住 | checkIn | |
| # | ikeySeqNos | 序號 |
| 房號 | roomNos | |
| 住客姓名 | guestName | |
| 入住時間 | eciTime | |
| 退房時間 | ecoTime | |
| 住房掛帳 | chargeInFolio | |

## 子 Dialog 清單

| 入口 | 子 Dialog 名稱 | 框架 | 關閉方式 | 探索狀態 |
|------|---------------|------|---------|---------|
| altNameBtn | 住客歷史 | EasyUI Panel + Syncfusion 按鈕 | `//a[contains(@class,'panel-tool-close')]` | ✅ 已掃+已開 |
| acustCodeBtn | 商務公司維護 | EasyUI Panel + Element UI | `//a[contains(@class,'panel-tool-close')]` | ✅ 已掃+已開 |
| orderRemark | 訂房備註（展開編輯） | Syncfusion Dialog | `//button[@title='關閉']`⚠️需`[last()]` | ✅ 已掃 |
| linkNosDialog | 關聯單號 | EasyUI Panel | `(//a[contains(@class,'panel-tool-close')])[last()]` | ✅ 已掃 |
| roomStatusDialog | 訂單資訊（非鎖控） | Syncfusion Dialog | `(//button[@title='關閉'])[last()]` | ✅ 已掃 |
| guideDialog | 領隊資料 | Syncfusion Dialog | `(//button[@title='關閉'])[last()]` | ✅ 已掃 |
| ptvDialog | PTV | Syncfusion Dialog | `(//button[@title='關閉'])[last()]` | ✅ 已掃 |
| focDialog | FOC | Syncfusion Dialog | `(//button[@title='關閉'])[last()]` | ✅ 已掃 |
| banlanceAmount | 開班作業（PMS0310060） | EasyUI Panel + Element UI + Syncfusion | `(//a[contains(@class,'panel-tool-close')])[last()]` | ✅ 已掃（子程式邊界） |
| doOpenRoomAssignDialog | 排房 | EasyUI Panel + Syncfusion + EasyUI Grid | `(//a[contains(@class,'panel-tool-close')])[last()]` | ✅ 已掃 |
| doOpenDtDetailDialog | 訂房明細 | Syncfusion Dialog + EasyUI Grid | `(//button[@title='關閉'])[last()]` | ✅ 已掃 |
| doOpenChangeLogDialog | 異動紀錄 | Syncfusion Dialog + Syncfusion Grid | `(//button[@title='關閉'])[last()]` | ✅ 已掃 |
| rateCode（行內編輯） | 選擇房價 | EasyUI Panel + Syncfusion(882) | `(//a[contains(@class,'panel-tool-close')])[last()]` | ✅ 已掃 |

### 住客歷史 Panel 內部

| 元素 | 類型 | Locator | 備註 |
|------|------|---------|------|
| 名 | input | `//div[@data-field-id='first_nam']//input` | Syncfusion |
| 姓 | input | `//div[@data-field-id='last_nam']//input` | Syncfusion |
| 姓名 | input | `//div[@data-field-id='alt_nam']//input` | Syncfusion |
| 稱謂 | input | `//div[@data-field-id='salute_cod']//input` | EasyUI combobox |
| 性別 | input | `//div[@data-field-id='cust_idx.sex_typ']//input` | EasyUI combobox |
| 狀態 | input | `//div[@data-field-id='status_cod']//input` | EasyUI combobox |
| VIP | input | `//div[@data-field-id='vip_sta']//input` | EasyUI combobox |
| 別名 | input | `//div[@data-field-id='other_nam']//input` | Syncfusion |
| 證件號碼 | input | `//div[@data-field-id='cust_idx.id_cod']//input` | Syncfusion |
| 生日 | input | `//div[@data-field-id='cust_idx.birth_dat']//input` | 含日曆 icon |
| 國籍 | input | `//div[@data-field-id='contry_cod']//input` | EasyUI combobox |
| 居住地 | input | `//div[@data-field-id='live_cod']//input` | EasyUI combobox |
| 語系 | input | `//div[@data-field-id='lang_cod']//input` | EasyUI combobox |
| 身分 | input | `//div[@data-field-id='role_cod']//input` | EasyUI combobox |
| 公司名稱 | input | `//div[@data-field-id='ccust_nam']//input` | Syncfusion |
| 公司電話 | input | `//div[@data-field-id='cust_idx.office_tel']//input` | Syncfusion |
| 行動電話 | input | `//div[@data-field-id='cust_idx.mobile_nos']//input` | Syncfusion |
| 住家電話 | input | `//div[@data-field-id='cust_idx.home_tel']//input` | Syncfusion |
| 傳真號碼 | input | `//div[@data-field-id='cust_idx.fax_nos']//input` | Syncfusion |
| 發票抬頭 | input | `//div[@data-field-id='cust_idx.uni_title']//input` | Syncfusion |
| 統一編號 | input | `//div[@data-field-id='cust_idx.uni_cod']//input` | Syncfusion |
| 車號 | input | `//div[@data-field-id='car_nos']//input` | Syncfusion |
| DM | input | `//div[@data-field-id='dm_flag']//input` | EasyUI combobox |
| 郵遞區號 | input | `//div[@data-field-id='cust_idx.zip_cod']//input` | 含查詢 icon |
| 申報公司 | input | `//div[@data-field-id='acu_cust_cod']//input` | EasyUI combobox，DISABLED |
| 載具類別 | input | `//div[@data-field-id='carriertype']//input` | EasyUI combobox |
| 載具顯碼 | input | `//div[@data-field-id='carrierid1']//input` | DISABLED |
| 航空公司 | input | `//div[@data-field-id='airline_cod']//input` | EasyUI combobox |
| 酬賓計畫卡號 | input | `//div[@data-field-id='airmb_nos']//input` | Syncfusion |
| 身分識別類別 | input | `//div[@data-field-id='identify_cod']//input` | EasyUI combobox |
| 身分識別編號 | input | `//div[@data-field-id='identify_nos']//input` | DISABLED |
| 退房清單方式 | input | `//div[@data-field-id='co_del_sta']//input` | EasyUI combobox |
| Email | textarea | `//div[@data-field-id='cust_idx.e_mail']//textarea` | |
| 地址 | textarea | `//div[@data-field-id='cust_idx.add_rmk']//textarea` | |
| 住客歷史編號 | input | `//div[@data-field-id='show_cod']//input` | DISABLED |
| 儲存 | button | `//button[@data-field-id='doSaveData']` | ⚠️ 未驗互動（不可逆） |
| 新增 | button | `//button[@data-field-id='doAddData']` | ⚠️ 未驗互動（不可逆） |
| 異動紀錄 | button | `//button[@data-field-id='loadChangeLog']` | |
| 車號 [...] | button | `//button[@data-field-id='openCarNos']` | |
| 商務公司 [...] | button | `//button[@data-field-id='openAcuCustCode']` | |
| 身分識別 [...] | button | `//button[@data-field-id='openIdentifyNos']` | |
| 來店資料 | button | `//button[@data-field-id='openVisitsPanel']` | DISABLED（需選住客） |
| 備註 | button | `//button[@data-field-id='openNotes']` | DISABLED（需選住客） |
| 證件掃描 | button | `//button[@data-field-id='openScan']` | DISABLED（需選住客） |
| 留言紀錄 | button | `//button[@data-field-id='openMessage']` | |
| 失物紀錄 | button | `//button[@data-field-id='openLost']` | |
| 訂單資訊 | button | `//button[@data-field-id='openOrder']` | |

### 訂房備註 Dialog（orderRemark 展開）

| 元素 | 類型 | Locator | 備註 |
|------|------|---------|------|
| 備註內容 | textarea | `//div[@data-field-id='orderRemark']//textarea` | 可讀寫，placeholder="請輸入" |
| 確定 | button | `//div[@data-field-id='confirmButton']//button` | ⚠️ 未驗互動（會寫入） |
| 關閉 | button | `//button[@title='關閉'][last()]` | ⚠️ 必須加 `[last()]`，否則關到主 dialog |

- 框架：Syncfusion（dialog + textarea + button）
- 結構極簡：一個 textarea 全螢幕編輯 + 確定/關閉
- 觸發：主 dialog 表單區 `//div[@data-field-id='orderRemark']//button`

### 關聯單號 Panel（linkNosDialog）

| 元素 | 類型 | Locator | 備註 |
|------|------|---------|------|
| 關聯單號 | input | label 定位（無 data-field-id） | DISABLED，顯示用 |
| 相關房號 | button | `//button[normalize-space()='相關房號']` | |
| 儲存 | button | `//button[child::img[@alt='save']]` | type="submit" ⚠️ 未驗互動（不可逆） |
| 新增 | span | `//span[contains(@class,'sub-button--add')]` | |
| 關閉 | a | `(//a[contains(@class,'panel-tool-close')])[last()]` | EasyUI panel 關閉 |

**關聯單號 Table**（6 欄）：

| 顯示名稱 | 備註 |
|----------|------|
| 訂房卡號 | |
| 房號 | |
| 住客姓名 | |
| 入住日期 | |
| 退房日期 | |
| 訂房名稱/團號 | |

- 框架：EasyUI Panel（無 data-field-id，label 定位、img alt 按鈕）
- 含一個 6 欄 table 顯示已關聯的訂房卡
- 觸發：`//div[@data-field-id='linkNosDialog']//button`

### 訂單資訊 Dialog（roomStatusDialog — 名稱不一致）

> ⚠️ data-field-id 為 `roomStatusDialog`（鎖控），但實際開啟的 dialog 標題是「訂單資訊」

| 元素 | 類型 | Locator | 備註 |
|------|------|---------|------|
| 確認號碼 | input | `//div[@data-field-id='confirmNos']//input` | DISABLED |
| 確認日期 | input | `//div[@data-field-id='confirmDate']//input` | DISABLED，DatePicker |
| 確認者 | input | `//div[@data-field-id='confirmUser']//input` | DISABLED |
| 取消號碼 | input | `//div[@data-field-id='cancelNos']//input` | DISABLED |
| 取消日期 | input | `//div[@data-field-id='cancelDate']//input` | DISABLED，DatePicker |
| 取消者 | input | `//div[@data-field-id='cancelUser']//input` | DISABLED |
| 保留日期 | input | `//div[@data-field-id='keepDate']//input` | DatePicker，placeholder="請選擇" |
| 保留時間 | input | `//div[@data-field-id='keepTime']//input` | TimePicker，placeholder="請選擇" |
| 自助機入住 | checkbox | `//div[@data-field-id='kiosCi']//input` | |
| 確定 | button | `//div[@data-field-id='confirmButton']//button` | ⚠️ 未驗互動 |
| 關閉 | button | `(//button[@title='關閉'])[last()]` | |

- 框架：Syncfusion（全部 data-field-id 定位）
- 6 個唯讀欄位（確認/取消資訊）+ 3 個可操作欄位（保留日期時間 + 自助機入住）
- 觸發：`//div[@data-field-id='roomStatusDialog']//button`

### 領隊資料 Dialog（guideDialog）

| 元素 | 類型 | Locator | 備註 |
|------|------|---------|------|
| 領隊姓名 | input | `//div[@data-field-id='guideName']//input` | placeholder="請輸入" |
| 領隊房號 | input | `//div[@data-field-id='guideRoom']//input` | placeholder="請輸入" |
| 領隊電話 | input | `//div[@data-field-id='guideTel']//input` | placeholder="請輸入" |
| 確定 | button | `//div[@data-field-id='confirmButton']//button` | ⚠️ 未驗互動 |
| 關閉 | button | `(//button[@title='關閉'])[last()]` | |

- 框架：Syncfusion（全部 data-field-id 定位）
- 3 個文字輸入欄位，全部可填寫
- 觸發：`//div[@data-field-id='guideDialog']//button`

### PTV Dialog（ptvDialog）

| 元素 | 類型 | Locator | 備註 |
|------|------|---------|------|
| 備註 | input | `//div[@data-field-id='infoRemark']//input` | placeholder="請輸入" |
| 是否團體 | dropdown | `//div[@data-field-id='infoIsGroup']//span` | 預設值「否」 |
| 確定 | button | `//div[@data-field-id='confirmButton']//button` | ⚠️ 未驗互動 |
| 關閉 | button | `(//button[@title='關閉'])[last()]` | |

- 框架：Syncfusion
- 觸發：`//div[@data-field-id='ptvDialog']//button`

### FOC Dialog（focDialog）

| 元素 | 類型 | Locator | 備註 |
|------|------|---------|------|
| 免費類型 | dropdown | `//div[@data-field-id='freeType']//input` | DropDownList，placeholder="請選擇" |
| 房號 | input | `//div[@data-field-id='roomNos']//input` | DISABLED |
| 免費房號 | input | `//div[@data-field-id='freeRoomNos']//input` | DISABLED |
| 免費金額 | input | `//div[@data-field-id='freeAmount']//input` | DISABLED，placeholder=" - " |
| 儲存 | button | `//div[@data-field-id='saveButton']//button` | ⚠️ 未驗互動（不可逆） |
| 關閉 | button | `(//button[@title='關閉'])[last()]` | |

- 框架：Syncfusion
- 1 個可操作下拉 + 3 個唯讀欄位
- 注意：儲存按鈕 data-field-id 是 `saveButton`（非 confirmButton）
- 觸發：`//div[@data-field-id='focDialog']//button`

### 開班作業 Panel（banlanceAmount — 子程式 PMS0310060）

> ⚠️ data-field-id 為 `banlanceAmount`（餘額），但實際開啟「開班」panel
> ⚠️ 子程式邊界：data-field-id 含 `PMS0310060` 前綴

| 元素 | 類型 | Locator | 備註 |
|------|------|---------|------|
| 日期 | input | `//div[@data-field-id='shop_dat']//input` | DISABLED |
| 廳別 | input | `//div[@data-field-id='rspt_cod']//input` | 含 `<i>` 查詢按鈕 |
| 使用者 | input | `//div[@data-field-id='open_man']//input` | DISABLED |
| 班別 | input | `//div[@data-field-id='shift_cod']//input` | |
| 密碼 | input | `//div[@data-field-id='s99_user.usr_pwd']//input` | type="password" |
| 確認 | button | `//button[@data-field-id='PMS0310060_r_1011']` | ⚠️ 未驗互動（不可逆） |
| 關閉 | a | `(//a[contains(@class,'panel-tool-close')])[last()]` | |

- 框架：Element UI (1) + Syncfusion (6)，EasyUI Panel 容器
- 子程式邊界確認：確認按鈕 data-field-id 為 `PMS0310060_r_1011`
- 觸發：`//div[@data-field-id='banlanceAmount']//button`
- 可能是前置作業——未開班就不能操作餘額/訂金功能

### 排房 Panel（doOpenRoomAssignDialog）

**操作列**：

| 元素 | 類型 | Locator | 備註 |
|------|------|---------|------|
| 彙總/明細切換 | button | `//button[@data-field-id='setTab']` | 預設「彙總」 |
| 排房狀態 | button | `//button[@data-field-id='assignStatus']` | 預設「全部」 |
| 排房調整 | button | `//button[@data-field-id='doAssignAdjustment']` | DISABLED |
| 批次取消 | button | `//button[@data-field-id='doUnassignAll']` | ⚠️ 未驗互動（不可逆） |
| 樓層 | button | `//button[@data-field-id='dropdownFloorStatus']` | 篩選下拉 |
| 清掃狀況 | button | `//button[@data-field-id='dropdownCleanStatus']` | 篩選下拉 |
| 棟別 | button | `//button[@data-field-id='dropdownBuildNosStatus']` | 篩選下拉 |
| 房間特色 | button | `//button[@data-field-id='dropdownCharacterRemark']` | 篩選下拉 |
| 拆併床 | button | `//button[@data-field-id='dropdownBedStatus']` | 篩選下拉 |
| 大圖示 | button | `//button[@data-field-id='dropdownRoomDisplayStatus']` | 顯示模式切換 |
| 篩選條件 | button | `//button[@data-field-id='openFilterCondictionDialog']` | 開啟篩選 dialog |
| 可排房 | checkbox | `//label[@data-field-id='chkAssign']` | label 上有 checkbox |
| 關閉 | a | `(//a[contains(@class,'panel-tool-close')])[last()]` | |

**房型選擇**（`chooseRoomType` 內 `<a>` 連結）：
ALL, TWN, DBL, QUAD, TEST, TRP, mlss, VL, STD, SPT, ODB, NDB, SDB, TRT, TUY, DBR, TRR, SAS, MAR, FST, TAS, SD... 等 24 種
- 定位：`//div[@data-field-id='chooseRoomType']//a[normalize-space()='%s']`

**排房 Grid**（EasyUI DataGrid，18 欄）：

| 顯示名稱 | @field | 備註 |
|----------|--------|------|
| 訂房卡號 | ikey_display | |
| 關聯單號 | link_nos | |
| 訂房 | order_qnt | |
| 排房 | assign_qnt | |
| C/I | ci_qnt | |
| 住客姓名 | guest_list | |
| 入住日期 | ci_dat | |
| 退房日期 | co_dat | |
| 計價房型 | use_cod | |
| 使用房型 | room_cod | |
| 團號 | group_nos | |
| 訂房公司 | acust_nam | |
| 狀態 | order_sta | |
| 房價代號 | ratecod_nam | |
| 單價 | rent_amt | |
| 服務費 | serv_amt | |
| 大人 | adult_qnt | |
| 小孩 | child_qnt | |

- 框架：EasyUI Panel 容器 + EasyUI DataGrid（`td[@field]`）+ Syncfusion 按鈕(82)
- 複雜度高：篩選器（樓層/清掃/棟別/房間特色/拆併床）+ 房型選擇 + grid
- 觸發：`//div[@data-field-id='doOpenRoomAssignDialog']//button`

### 訂房明細 Dialog（doOpenDtDetailDialog）

**工具列**：

| 元素 | 類型 | Locator | 備註 |
|------|------|---------|------|
| 團體名單 | button | `//div[@data-field-id='groupList']//button` | 📌 子 dialog 未探索 |
| 櫃檯備品 | button | `//div[@data-field-id='spareParts']//button` | 📌 子 dialog 未探索 |
| 備品資訊 | button | `//div[@data-field-id='showAllSpare']//button` | |
| 全部顯示 | button | `//div[@data-field-id='showAllList']//button` | |
| 儲存 | button | `//div[@data-field-id='save']//button` | ⚠️ 未驗互動（不可逆） |
| 關閉 | button | `(//button[@title='關閉'])[last()]` | |

**Tab 區**：

| Tab | ID | 備註 |
|-----|-----|------|
| 住客 | tab-guest | 含住客明細 Grid（見下方）|
| 服務項目 | tab-service | 含 textarea |
| 費用明細 | tab-expenseDetail | rentValue/serviceChargeValue/additionalFeeValue/otherFeeValue/totalValue |

**明細 Grid（上方，EasyUI DataGrid）**：

| 顯示名稱 | @field | 備註 |
|----------|--------|------|
| (房型按鈕) | button | 可編輯，如 "TWN0:TWN" |
| 狀態 | orderStatus | |
| 入住日期 | ciDate | |
| 退房日期 | coDate | |
| 房價代號 | rateCode | |
| 計價 | useCode | |
| 使用 | roomCode | |
| 間數 | orderQuantity | |
| 天數 | days | |
| 大人 | adultQuantity | |
| 小孩 | childQuantity | |
| 加人(大) | addMan | |
| 加人(小) | addChild | |
| ADD | addExtraFee | |
| 訊息 | message | |

**住客明細 Grid（tab-guest）**：

Syncfusion Grid inline edit 模式。每行有 Edit/Delete/Save/Cancel 按鈕（動態 ID）。

| 顯示名稱 | @field | 備註 |
|----------|--------|------|
| 住客姓名 | altName | 可編輯（inline edit） |
| 備註 | notes | |
| 預授權金額 | precreditAmount | |
| 交辦事項 | todoList | |
| 提醒 | reminder | |
| 失物 | lostProperty | |
| 轉帳 | transfer | |
| 留言 | message | |
| 無資訊 | noInfo | |
| # | ikeySeqNos / iKeySeqNos | 序號 |
| 狀態 | guestStatus | |
| 排房狀態 | assignStatus | |
| 序號 | seqNos | |
| 房號 | roomNos | |
| 排房備註 | assignRemark | |
| 住客代碼 | gcustCode | |
| C/I序號 | ciSer | |

**新增住客**：點 Edit 按鈕進入 inline edit 模式 → 輸入住客姓名（textarea）→ Save

**費用明細 Grid（tab-expenseDetail）**：

| 顯示名稱 | @field | 備註 |
|----------|--------|------|
| 項目編號 | itemNos | |
| 父序號 | parentSeqNos | |
| 使用日期 | useDate | 含星期 |
| 分帳 | SubAccountStatus | |
| 項目名稱 | itemSna | 如「房租1」 |
| 單價 | unitAmount | |
| 數量 | itemQnt | |
| 金額 | itemAmount | |
| 服務日期 | servDate | |
| 新增者 | insertUser | |
| 新增日期 | insertDate | |

- 框架：Syncfusion Dialog(71) + EasyUI DataGrid（`td[@field]`）
- 複雜度最高：3 個 tab + 多層 grid + 多住客 textarea
- 觸發：`//div[@data-field-id='doOpenDtDetailDialog']//button`

### 異動紀錄 Dialog（doOpenChangeLogDialog）

| 元素 | 類型 | Locator | 備註 |
|------|------|---------|------|
| 關閉 | button | `(//button[@title='關閉'])[last()]` | |
| 每頁筆數 | dropdown | Syncfusion DropDownList（動態 ID） | "Items per page" |
| 分頁 | div | `//div[@title='第一頁']` / `//div[@title='上一頁']` / `//div[@title='下一頁']` / `//div[@title='最終頁']` | |

**異動紀錄 Grid**（Syncfusion Grid，8 欄，唯讀）：

| 顯示名稱 | @field | 備註 |
|----------|--------|------|
| 異動時間 | changeStamp | 如 "2026/05/15 18:17:57" |
| 異動者 | changers | 帳號 |
| 功能 | functions | 如「依房型訂房」 |
| 動作 | action | 如「編輯」 |
| 對象 | target | 如「訂房卡號=00013289」 |
| 欄位名稱 | fieldName | 中文欄位名 |
| 變更前 | beforeChange | |
| 變更後 | afterChange | |

- 框架：Syncfusion Dialog + Syncfusion Grid + 分頁
- 全唯讀，用於稽核/查看歷史變更
- 觸發：`//div[@data-field-id='doOpenChangeLogDialog']//button`

### 選擇房價 Panel（彙總 Grid 行內編輯 → rateCode 按鈕）

> 操作路徑：彙總 Grid 點鉛筆編輯 → 行內出現 `rateCode` 按鈕 → 點擊開啟

| 元素 | 類型 | Locator | 備註 |
|------|------|---------|------|
| 房價名稱搜尋 | input | `//div[.//label[text()='房價名稱']]//input` | |
| 確定 | button | `//button[normalize-space()='確定']` | ⚠️ 未驗互動（會變更房價） |
| 關閉 | a | `(//a[contains(@class,'panel-tool-close')])[last()]` | |

**房價 Grid**（50 列，column = 房型代號如 TWN/DBL/STD...）：

- 房價代號 + 房價名稱（frozen 欄位）
- 各房型欄位顯示對應單價（可點擊選取）
- `td.bg-orange-2`：合約房價標記（淡橘底 `rgb(252, 237, 218)`），表示訂房公司綁定的合約房價
- `td.selected`：當前選中的 cell
- 合約房價自動排到最上方

- 框架：Syncfusion(882)，EasyUI Panel 容器
- 觸發路徑：彙總 Grid 鉛筆編輯 → `//div[@data-field-id='rateCode']//button`

### 列印 Dialog（doOpenReportDialog — 訂房確認書）

| 元素 | 類型 | Locator | 備註 |
|------|------|---------|------|
| 明細序號 | dropdown | `//div[@data-field-id='ikey_seq_nos']//input` | DropDownList，placeholder="請選擇" |
| 範本 | dropdown | `//div[@data-field-id='template']//input` | DropDownList，placeholder="請選擇" |
| 模式 | dropdown | `//div[@data-field-id='sql_mode']//span` | 預設「group」 |
| E-Mail | button | `//div[@data-field-id='email']//button` | |
| 列印/匯出 | button | `//div[@data-field-id='dropdownButton']//button` | DropdownButton（多選列印/PDF/Excel） |
| 關閉 | button | `(//button[@title='關閉'])[last()]` | |

- 框架：Syncfusion
- 觸發：`//div[@data-field-id='doOpenReportDialog']//button`

### E-mail Panel（doOpenEmailDialog）

| 元素 | 類型 | Locator | 備註 |
|------|------|---------|------|
| 收件人 | input | `//div[@data-field-id='atten_nam']//input` | DISABLED |
| E-Mail | input | `//div[@data-field-id='e_mail']//input` | |
| 格式代號 | input | `//div[@data-field-id='content_fmt']//input` | **EasyUI combobox**（`_easyui_textbox_input`） |
| 主旨 | input | `//div[@data-field-id='send_subject']//input` | |
| 發送內容 | button | `//div[@data-field-id='send_content_button']//button` | 展開內容編輯 |
| 附件上傳 | button | `//button[normalize-space()='附件上傳']` | |
| 儲存/寄送 | button | `//button[child::img[@alt='save']]` | img alt 定位 ⚠️ 未驗互動 |
| 關閉 | a | `(//a[contains(@class,'panel-tool-close')])[last()]` | |

- 框架：Syncfusion(6) + **EasyUI combobox**（content_fmt）
- ⚠️ 格式代號是 EasyUI combobox，走 DDL 操作（逐頁驗證時確認操作方式）
- 觸發：`//div[@data-field-id='doOpenEmailDialog']//button`

### 分帳規則 Panel（doOpenSubAccountDialog）

| 元素 | 類型 | Locator | 備註 |
|------|------|---------|------|
| 設定 | input | `//div[@data-field-id='master_sta']//input` | **EasyUI combobox**（`_easyui_textbox_input`） |
| 套用分帳代號 | button | `//button[normalize-space()='套用分帳代號']` | |
| 全選 | button | `//button[normalize-space()='全選']` | |
| 新增 | button | `//button[child::img[@alt='add']]` | img alt 定位 |
| 儲存 | button | `//button[child::img[@alt='save']]` | img alt 定位 ⚠️ 未驗互動 |
| 關閉 | a | `(//a[contains(@class,'panel-tool-close')])[last()]` | |

**分帳 Grid**（EasyUI DataGrid，1 欄）：

| 顯示名稱 | @field | 備註 |
|----------|--------|------|
| 帳夾 | folio_nos | |

- 框架：EasyUI(2) + Syncfusion(1)，EasyUI Panel 容器
- ⚠️ 設定欄位是 EasyUI combobox，走 DDL 操作（逐頁驗證時確認操作方式）
- 觸發：`//div[@data-field-id='doOpenSubAccountDialog']//button`

### 備品批次新增 Dialog（doOpenBatchSpareInsert）

**操作列**：

| 元素 | 類型 | Locator | 備註 |
|------|------|---------|------|
| 庫存查詢 | button | `//div[@data-field-id='checkInventory']//button` | 📌 子功能未探索 |
| 備品資訊 | button | `//div[@data-field-id='spareInfo']//button` | 📌 子功能未探索 |
| 儲存 | button | `//div[@data-field-id='save']//button` | ⚠️ 未驗互動（不可逆） |
| 關閉 | button | `(//button[@title='關閉'])[last()]` | |

**Tab 區**：

| Tab | ID | 備註 |
|-----|-----|------|
| 未入住 | tab-notCheckIn | |
| 已入住 | tab-checkIn | |

**明細 Grid**（Syncfusion，5 欄 + checkbox 選取）：

| 顯示名稱 | @field | 備註 |
|----------|--------|------|
| 序號 | ikeySeqNos | |
| 房號 | roomNos | |
| 住客姓名 | guestName | |
| 入住日期 | checkInDate | |
| 退房日期 | checkOutDate | |

- 框架：Syncfusion（dialog + grid + checkbox）
- 2 個 tab（未入住/已入住）+ 備品 textarea ×4
- 觸發：`//div[@data-field-id='doOpenBatchSpareInsert']//button`

### 旅客登記卡 Panel（doOpenReportRcard）

| 元素 | 類型 | Locator | 備註 |
|------|------|---------|------|
| 報表格式 | input | `//div[@data-field-id='template']//input` | **EasyUI combobox** |
| 匯出 | button | `//button[@data-field-id='export']` | img alt="export" |
| 關閉 | a | `(//a[contains(@class,'panel-tool-close')])[last()]` | |

- 框架：Syncfusion(4) + EasyUI combobox（template）
- 開啟時附帶「報表測試環境選擇」panel（可能只在 QA 環境出現）
- 觸發：`//div[@data-field-id='doOpenReportRcard']//button`

### Pre-C/I Dialog（doOpenPreCheckIn）

| 元素 | 類型 | Locator | 備註 |
|------|------|---------|------|
| Pre-C/I 狀態 | dropdown | `//div[@data-field-id='preciStatus']//input` | DropDownList |
| 發送對象 | dropdown | `//div[@data-field-id='sendObject']//span` | 預設「訂房卡全部住客」 |
| 搜尋 | button | `//div[@data-field-id='searchButton']//button` | type="submit" |
| 清除 | button | `//div[@data-field-id='clearButton']//button` | |
| 簡訊 | button | `//div[@data-field-id='sms']//button` | |
| 電子郵件 | button | `//div[@data-field-id='email']//button` | |
| 發送 | button | `//div[@data-field-id='send']//button` | ⚠️ 未驗互動（會發送） |
| 關閉 | button | `(//button[@title='關閉'])[last()]` | |

- 框架：Syncfusion
- 含 checkbox grid（全選）+ textarea（內容預覽）
- 觸發：`//div[@data-field-id='doOpenPreCheckIn']//button`

## 操作備註

### 導航
- SPA 選單導航：click `//button[normalize-space()='訂房']` → click `//span[normalize-space()='訂房卡']`
- ⚠️ 不要 click `<a>` 元素（不觸發 SPA 路由），必須 click `<span>`
- `<span>` 不在 scan 預設範圍，需用 `find -x` 確認

### 框架混用
- 訂房卡 Dialog 本體：Syncfusion（設值風險低）
- 商務公司維護子 dialog：**EasyUI + Element UI**（設值風險中~高）
- 住客歷史子 dialog：**EasyUI combobox 大量使用**（salute_cod、sex_typ、status_cod、vip_sta、contry_cod 等 13 個），Syncfusion 僅用於純文字 input 和按鈕

### EasyUI combobox 操作（住客歷史內）
- ⚠️ EasyUI combobox 本身就是下拉選單，走 DDL 操作（click 展開 → click 選項），逐頁驗證時確認操作方式
- 或用 `type -x input -t "keyword" --enter` → JS click 選取

### Dialog 關閉方式
- 訂房卡 Dialog：Syncfusion — `//button[@title='關閉']`
- 商務公司維護 / 住客歷史：EasyUI Panel — `//a[contains(@class,'panel-tool-close')]`（多個時加 `[last()]`）

### 已驗操作
- groupNos textbox：type + get 讀回驗證 ✅（Syncfusion textbox 正常）
- acustCodeBtn `...`：click 開啟商務公司維護 ✅，panel-tool-close 關閉 ✅
- altNameBtn `...`：click 開啟住客歷史 ✅，panel-tool-close 關閉 ✅

### C2 盲區掃描結果
- `panel-tool-close`：2 個殘留 DOM（商務公司、住客歷史關閉後 display:none 不移除）
- `icon/fa-`：2 個 `<i>` 無辨識屬性，低影響
- `span.button/sub-button`：無
- `label[@data-field-id]`：無
- 結論：Syncfusion 為主，scan 覆蓋率高，盲區小

### C4 陷阱檢查
- `td[@data-field-id]` 多匹配：**不存在**（訂房卡不用 EasyUI td 結構）
- `button[child::img]`：**不存在**（工具列用文字按鈕不用 img）
- EasyUI combobox（主 dialog）：**不存在**（只在住客歷史子 dialog 有 13 個）
- 結論：訂房卡 dialog 本體幾乎無已知陷阱，陷阱集中在子 dialog

### C5 參數化候選
- `//div[@data-field-id='%s']//button` — `...` 按鈕群（10+ 個同結構）
- `//div[@data-field-id='%s']//input` — 表單 input 群（33 個同結構）
- Grid 編輯按鈕 ID 含動態數字（`grid_391111584_2Edit_0_gridcommand85`），不穩定，不宜直接用

### C6 狀態變異
- orderStatus DDL：click `e-input-group` span **兩次嘗試均無反應**
- 可能原因：此訂房卡狀態不允許從 dialog 內直接切換，或需要特定觸發方式
- 標記：❌ DDL 觸發失敗，待查（案例 #527/#528/#529 涉及狀態變更）

### 未解決
- orderStatus DDL：✅ 已解決
  - 根因：搜尋區和 dialog 表單區各有一個 `data-field-id='orderStatus'`，但類型不同（multiselect vs DDL）
  - 正確定位：`(//div[@data-field-id='orderStatus']//span[contains(@class,'e-ddl')])[last()]`
  - 選項：正常、等待、取消、洽價、VIP
  - 注意：diff 無法偵測 DDL 展開（aria-expanded 變化不在 diff 追蹤範圍）
- 工具列按鈕狀態：排房 ✅ / 訂房確認書(列印) ✅ / 檢視R卡(需住客) / 訂房明細 ✅ / 簡訊(需選明細) / E-mail ✅ / 分帳規則 ✅ / 旅客登記卡 ✅ / Pre-C/I ✅ / 備品批次 ✅ / 線上繳款單(需訂金)
- 所有不可逆操作（儲存、新增、複製、發送）：僅 find 確認存在
- 訂房明細內「團體名單」「櫃檯備品」子 dialog 未探索

### querySetsSettingButtohn
- data-field-id 有 typo：`Buttohn`（不是 Button），定位時需注意拼寫

### 彙總 Grid 編輯按鈕 scope 陷阱
- `//button[contains(@id,'Edit') and contains(@id,'gridcommand')]` 會匹配列表頁 + dialog 內所有 Grid 的編輯按鈕
- 列表頁的按鈕在 dialog 後面，點擊會被 BLOCKED
- grid_0 = 列表頁 Grid、grid_6 = 彙總 Grid、grid_7 = 明細 Grid
- 行內編輯模式啟動後，會出現 `rateCode`、`blockCode` 等欄位的操作按鈕

### 合約房價標記（bg-orange-2）
- 選擇房價 panel 中，訂房公司有合約的房價列 `td` 會帶 class `bg-orange-2`
- 背景色：`rgb(252, 237, 218)`（淡橘色）
- 合約房價自動排到清單最上方
- 此標記只在訂房公司為合約公司（非 FIT）時出現

### 訂房備註 Dialog 關閉陷阱
- 訂房備註 dialog 的關閉按鈕 `//button[@title='關閉']` 與主 dialog 共用同一 XPath
- 不加限定會先匹配主 dialog 的關閉按鈕 → 主 dialog 關閉、子 dialog 殘留
- 正確關閉方式：`//button[@title='關閉'][last()]` 或 `//div[@data-field-id='confirmButton']//button`（確定按鈕）
