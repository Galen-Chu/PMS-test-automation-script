from selenium.webdriver.common.by import By
from locators.base_locator import BaseLocator


class ReservationLocator(BaseLocator):

    table_empty_pointer = (
        By.XPATH,
        "//tbody[@class='table--data']/tr[not(td[@class='name-color pointer'])]/td[@class='pointer']",
    )
    text_selected_room = (By.XPATH, "//td[contains(@class, 'is_selected')]/parent::tr/th[2]")
    btn_reservation = (By.XPATH, "//button[@data-field-id='r_1050']")
    rent_day = (By.XPATH, "//div[@class='month-picker']//input[@type='text']")

    # ----- 住客歷史 -----
    btn_edit_name = (By.XPATH, "//div[@data-field-id='altNameBtn']")
    input_first_name = (By.XPATH, "//div[@data-field-id='first_nam']//input")
    input_last_name = (By.XPATH, "//div[@data-field-id='last_nam']//input")
    input_salute = (By.XPATH, "//div[@data-field-id='salute_cod']/span/input")
    option_salute = (
        By.XPATH,
        "//tr[contains(@class, 'datagrid-row') and child::td[child::div[text()='%s']]]",
    )
    input_mobile = (By.XPATH, "//div[@data-field-id='cust_idx.mobile_nos']//input")
    input_email = (By.XPATH, "//div[@data-field-id='cust_idx.e_mail']//textarea")
    btn_save_guest = (By.XPATH, "//button[@data-field-id='doSaveData']")
    btn_save = (By.XPATH, "//div[@data-field-id='save']")
    guest_data_confirm = (By.XPATH, "//div[text()='住客歷史資料確認']")
    # ----- 住客歷史 End -----

    # ----- 訂房卡主檔 -----
    company_selection = (By.XPATH, "//div[contains(@class, 'dropdownbase')]//div[text()='%s']")
    text_salute_code = (
        By.XPATH,
        "//div[@data-field-id='saluteCode']//span[@class='e-input-value']/span/span[last()]",
    )
    text_dialog_ikey = (By.XPATH, "//div[@data-filed-id='dialogIkey']")
    text_deposit_amo = (By.XPATH, "//div[@data-field-id='banlanceAmount']//input[@type='text']")
    # ----- 訂房卡主檔 End -----

    # ----- 明細頁籤 -----
    tab_detail = (By.XPATH, "//div[@id='tab-Detail']")
    td_guest_info = (
        By.XPATH,
        "//div[@aria-labelledby='tab-Detail']//tr[@class='e-row']/td[@field='%s']",
    )
    input_co_date = (By.XPATH, "//input[@id='coDate']")
    # ----- 明細頁籤 End -----

    # ----- 依房型訂房 -----
    select_room_type = (By.XPATH, "//tr[contains(@data-tt-id, '%s') and not(@data-tt-parent-id)]\
                        /td[contains(@class, 'pointer') and not(contains(@class, 'is_selected'))]")
    btn_edit_item = (
        By.XPATH,
        "//div[@id='pane-Summary']//button[@title='編輯' and not(contains(@class, 'e-hide'))]",
    )

    input_rent_total = (By.XPATH, "//input[@id='groupRentTotal']")
    btn_reservation_by_room_type = (By.XPATH, "//button[@data-field-id='reservation']")
    btn_rent_total_detail = (By.XPATH, "//div[@data-field-id='groupRentTotalButton']")
    # ----- 依房型訂房 End -----

    # ----- 浮動房價 -----
    text_rent_amounts = (
        By.XPATH,
        "//th[normalize-space()='房租']/ancestor::div[contains(@class, 'e-gridheader')]\
                         /following-sibling::div[contains(@class, 'e-gridcontent')]//td[@field='rentItemAmount']",
    )
    btn_panel_close = (
        By.XPATH,
        "//div[text()='%s']/ancestor::div[@class='e-dlg-header']/preceding-sibling::button",
    )
    # ----- 浮動房價 END -----
