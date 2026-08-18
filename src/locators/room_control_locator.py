from selenium.webdriver.common.by import By
from locators.base_locator import BaseLocator


class RoomControlLocator(BaseLocator):

    btn_change_floor = (By.XPATH, "//li[normalize-space()='%s']")
    btn_room_no = (
        By.XPATH,
        "//div[@class='tab-content' and not(@style='display: none;')]//div[@class='card--room']//span[normalize-space()='%s']",
    )
    clean_status = (By.XPATH, "//label[normalize-space()='清掃狀態']/following-sibling::input")
    room_block = (By.XPATH, "//div[@slot='reference' and descendant::span[normalize-space()='%s']]")
    room_icon = (
        By.XPATH,
        "(//div[@slot='reference' and descendant::span[normalize-space()='%s']]//img)[%s]",
    )

    select_room_status = (By.XPATH, "//div[@data-field-id='clean_sta']")
    select_room_status_item = (By.XPATH, "//ul[@role='listbox']//span[text()='%s']")
    room_status_list = (
        By.XPATH,
        "//tbody[@role='rowgroup']//tr[@role='row']/td[@field='room_nos']",
    )
    room_checkbox = (
        By.XPATH,
        "//tbody[@role='rowgroup']//tr[@role='row']/td[text()='%s']/preceding-sibling::td",
    )
    btn_close_clean_floor = (
        By.XPATH,
        "//div[@class='e-dlg-header' and descendant::div[text()='清掃樓層']]/preceding-sibling::button[@title='關閉']",
    )
    checkbox_all_rooms = (By.XPATH, "//tr[@class='e-columnheader']/th[@tabindex='0']")

    select_category = (By.XPATH, "//div/label[normalize-space()='類別']/following-sibling::span")
    select_category_item = (
        By.XPATH,
        "(//div[contains(@class, 'combobox-item') and text()='%s'])[last()]",
    )

    date_by_label = (By.XPATH, "//div/label[normalize-space()='%s']/following-sibling::div")
    date_title_year = (
        By.XPATH,
        "(//span[@class='el-date-picker__header-label' and contains(text(), '年')] )[last()]",
    )
    date_year = (
        By.XPATH,
        "(//table[@class='el-year-table'])[last()]//td[@class='available']/a[text()='%s']",
    )
    date_month = (By.XPATH, "(//table[@class='el-month-table'])[last()]//a[text()='%s']")
    date_day = (
        By.XPATH,
        "(//table[@class='el-date-table'])[last()]//td[@class='available']//span[normalize-space()='%s']",
    )

    input_reason = (
        By.XPATH,
        "//div/label[normalize-space()='修理/參觀原因']/following-sibling::textarea",
    )
    btn_repair_visit_save = (
        By.XPATH,
        "(//div[@class='panel-title' and text()='修理/參觀']/parent::div//following-sibling::div//button)[1]",
    )

    date_by_room = (
        By.XPATH,
        "//div[@slot='reference' and descendant::span[normalize-space()='%s']] \
                    //div[@class='card-row']/span[normalize-space()='%s']",
    )
    reason_by_room = (
        By.XPATH,
        "//div[@slot='reference' and descendant::span[normalize-space()='%s']] \
                      //div[@class='card-row' and normalize-space()='%s']",
    )

    input_reason_floor = (By.XPATH, "//input[@name='reason_rmk']")
    checkbox_room_floor = (
        By.XPATH,
        "//div[@class='table__scroll']//td[@class='text-center' and following-sibling::td[normalize-space()='%s']]",
    )
    room_errors = (
        By.XPATH,
        "//div[@class='table--fix-head']//td[@class='text-center' and child::p[contains(text(),'設定失敗')]]",
    )

    room_repair_list = (By.XPATH, "//table[@class='datagrid-btable']//td[@field='room_nos']")
    room_repair_list_item = (
        By.XPATH,
        "//table[@class='datagrid-btable']//td[@field='room_nos' \
                                    and child::div[normalize-space()='%s']]/preceding-sibling::td",
    )
    room_repair_datepicker = (
        By.XPATH,
        "//div[child::div/span[normalize-space()='%s']]/following-sibling::div//span[@aria-label='select']",
    )
    room_repair_day = (
        By.XPATH,
        "//div[contains(@class, 'e-month')]//span[@data-ripple='true' and text()='%s']",
    )
    room_repair_reason = (By.XPATH, "//div[@data-field-id='reasonRemark']//textarea")
    room_repair_save = (By.XPATH, "//div[@data-field-id='confirmButton']")
    room_repair_check_all = (By.XPATH, "//div[@class='datagrid-header-check']")

    input_defect = (By.XPATH, "//textarea[@class='input']")

    # 拆併床相關 locator
    checkbox_bed_setup_room = (
        By.XPATH,
        "//tbody[@role='rowgroup']//tr[@role='row']/td[text()='%s']/preceding-sibling::td",
    )
    select_bed_setting = (By.XPATH, "//div[@data-field-id='bedStatus' and @class='flex-none']")
    select_bed_setting_item = (By.XPATH, "//ul[@role='listbox']//span[normalize-space()='%s']")
    btn_bed_setup_save = (By.XPATH, "//div[@data-field-id='save']")
    bed_setup_status = (
        By.XPATH,
        "//tbody[@role='rowgroup']//tr[@role='row']/td[text()='%s']/following-sibling::td",
    )
    btn_close_bed = (
        By.XPATH,
        "//div[@class='e-dlg-header' and descendant::div[text()='拆併床']]/preceding-sibling::button[@title='關閉']",
    )
