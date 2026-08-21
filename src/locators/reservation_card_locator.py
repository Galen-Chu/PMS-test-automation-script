from selenium.webdriver.common.by import By
from locators.base_locator import BaseLocator


class ReservationCardLocator(BaseLocator):
    # ----- 訂房明細 視窗 -----
    btn_tool = (
        By.XPATH,
        "(//div[@class='e-dlg-content']//div[@data-field-id='%s']/button)[last()]",
    )
    tab_list = (By.XPATH, "//div[@role='tablist']//div[@id='tab-%s']")
    tab_service_table = (By.XPATH, "(//div[@id='pane-service']//td[@field='%s'])[last()]")
    empty_msg_by_tab = (By.XPATH, "//div[@id='pane-%s']//div[@class='e-gridcontent']//td")
    toolbar_by_tab = (By.XPATH, "(//div[@id='pane-%s']//button[@title='%s'])[last()]")
    tab_expense_table = (
        By.XPATH,
        "(//div[@id='pane-expenseDetail']//tr[td[contains(text(),'%s')]]/td[@field='%s'])[last()]",
    )
    tab_expense_rent = (By.XPATH, "//div[@id='pane-expenseDetail']//span[text()='房租']")
    tab_expense_list_by_date = (
        By.XPATH,
        "//div[@id='pane-expenseDetail']//tr[td[contains(text(),'%s')]]//span",
    )
    tab_expense_summary_section = (
        By.XPATH,
        "//div[contains(@class,'expense')]//div[@data-field-id='%s']//input[@type='text']",
    )
    tab_guest_function = (By.XPATH, "//div[@id='pane-guest']//*[@data-field-id='%s']")
    tab_guest_function_status = (By.XPATH, "//div[@id='pane-guest']//td[@field='todoList']//i")
    tab_guest_precredit = (By.XPATH, "//div[@id='pane-guest']//td[@field='precreditAmount']//span")
    tab_guest_table = (By.XPATH, "//div[@id='pane-guest']//tbody[not(@class)]//tr")
    btn_edit_assign_notes = (
        By.XPATH,
        "//tr[td[@field='seqNos']]//span[@class='e-btn-icon e-edit e-icons']",
    )
    btn_add_assign_notes = (By.XPATH, "//i[@data-field-id='buttonButton']")
    btn_save_assign_notes = (By.XPATH, "//table[contains(@class,'inline')]//button[@title='儲存']")
    column_assign_notes = (By.XPATH, "//td[@field='assignRemark']")

    guest_name_in_table = (
        By.XPATH,
        "//div[@id='pane-guest']//tbody[not(@class)]//td[@field='altName']",
    )
    btn_edit_guest = (By.XPATH, "//div[@data-field-id='altNameButton']")
    btn_add_by_tab = (By.XPATH, "//div[@id='pane-%s']//div[@data-field-id='grid-add']")

    guest_no_info_option = (By.XPATH, "//div[@id='noInfo_popup']//span[text()='%s']")
    # ----- 訂房明細 視窗 End -----

    # ----- 訂房卡 視窗 -----
    btn_card_toolbar = (By.XPATH, "//div[@data-field-id='%s']")
    btn_select_rate_code = (By.XPATH, "//div[@data-field-id='rateCode']//button")
    btn_deposit_setting = (By.XPATH, "//button[ancestor::div[@data-field-id='banlanceAmount']]")
    select_rate_code = (By.XPATH, "//td[span[text()='%s']]//following-sibling::td[%s]")
    input_rate_cod_name = (By.XPATH, "//div[.//label[text()='房價名稱']]//input")
    empty_msg = (By.XPATH, "//div[@class='e-gridcontent']//td")
    # ----- 訂房卡 視窗 End -----

    # ----- 訂房卡頁面 -----
    btn_edit = (By.XPATH, "(//button[@title='編輯'])[last()]")
    btn_search_toolbar = (By.XPATH, "//div[contains(@data-field-id,'%s')]")
    input_by_condition = (By.XPATH, "//div[@data-field-id='%s']//input")
    # ----- 訂房卡頁面 End -----

    # ----- 房間特色選單 視窗 -----
    select_room_features = (By.XPATH, "//td[text()='%s']")
    checkbox_state = (By.XPATH, "//input[contains(@class,'e-checkselect')]")
    checked_checkbox = (
        By.XPATH,
        "//input[@class='e-checkselect']/following::span[contains(@class,'e-check')]",
    )
    # ----- 房間特色選單 視窗 End ----

    # ----- 備品庫存查詢 視窗 -----
    spare_parts_filter = (By.XPATH, "//div[@data-field-id='items']")
    spare_parts_checkboxes = (By.XPATH, "//ul[@role='listbox']//div")
    spare_parts_text = (By.XPATH, "//ul[@role='listbox']//span[text()!='']")
    spare_parts_search_result = (By.XPATH, "//td[@fieldname='itemName']/span")
    # ----- 備品庫存查詢 視窗 End -----

    # ----- 備品資訊視窗 -----
    text_batch_spare_by_label = (By.XPATH, "//td[@field='%s']")
    # ----- 備品資訊視窗 End -----

    # ----- 團體名單 視窗 -----
    group_list_row_by_field = (By.XPATH, "//tr[.//div[text()='%s']]//td[@field='%s']")
    group_list_row_by_num = (By.XPATH, "//tr[.//div[text()='%s']]")
    group_list_guest_checkbox = (By.XPATH, "//table[@class='datagrid-btable']//td[@field='ck']")
    btn_move_guest = (By.XPATH, "//button[contains(@class,'button--%s')]")
    # ----- 團體名單 視窗 End ----

    # ----- notes 視窗 -----
    textarea = (By.XPATH, "(//textarea)[last()]")
    btn_add_note = (By.XPATH, "(//span[@class='sub-button--add'])[last()]")
    btn_remove_note = (By.XPATH, "(//span[@class='sub-button--remove'])[last()]")
    # ----- notes 視窗 End -----

    # ----- 提醒事項 視窗 -----
    input_reservation_remind = (By.XPATH, "//tr[td[normalize-space()='%s']]//input")
    # ----- 提醒事項 視窗 End -----

    # ----- 訂房卡共用 -----
    btn_add = (By.XPATH, "(//div[@class='sub-button--add'])[last()]")
    # ----- 訂房卡共用 End -----

    # ----- 房租細項 視窗 -----
    expense_detail_colume_by_row_and_index = (By.XPATH, "//div[.//text()='房租細項']//tr[%s]//td")
    # ----- 房租細項 視窗 End -----

    # ----- 公帳號相關 -----
    checkbox_use_folio = (
        By.XPATH,
        "//div[@data-field-id='masterStatus']//label[.//span[text()='使用公帳號']]//input[@type='checkbox']",
    )
    # ----- 公帳號相關 End -----

    # ----- 訂金單筆新增 視窗 -----
    btn_clear_depositNos = (By.XPATH, "//div[@data-field-id='depositNos']//span[@role='button']")

    # 訂金欄位
    input_deposit_no = (By.XPATH, "//label[normalize-space()='訂金編號']/following-sibling::input")
    deposit_no_option = (By.XPATH, "//div[@role='option']//span[contains(text(),'%s')]")
    invoice_method_option = (By.XPATH, "//div[contains(@class, 'combobox-item') and text()='%s']")

    # 付款方式與金額
    table_payment_method = (By.XPATH, "//td[@data-field-id='deposit_dt_pay_way']")
    input_payment_amount = (By.XPATH, "//td[@data-field-id='deposit_dt_use_amt']//input")
    # ----- 訂金單筆新增 視窗 End -----

    # ----- 關聯單號 -----
    btn_link_nos_dialog = (
        By.XPATH,
        "//div[@data-field-id='linkNosLabel']/following-sibling::div//button",
    )
    link_nos_add_button = (By.XPATH, "(//span[contains(@class, 'sub-button--add')])[last()]")
    link_nos_remove_button = (By.XPATH, "(//span[@class='sub-button--remove'])[last()]")
    link_nos_row_data = (
        By.XPATH,
        "//div[contains(@title, '關聯單號')]//tr[%s]//td[not(@class='text-center')]",
    )
    text_link_nos = (By.XPATH, "//div[@data-field-id='linkNos']/div")
    text_link_nos_in_dialog = (
        By.XPATH,
        "//div/label[text()='關聯單號']/following-sibling::div/input",
    )
    # ----- 關聯單號 End -----
