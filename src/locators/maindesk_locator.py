from selenium.webdriver.common.by import By
from locators.base_locator import BaseLocator


class MaindeskLocator(BaseLocator):

    # ----- 多筆頁面 -----
    room_by_number = (
        By.XPATH,
        "//div[contains(@class,'room')]//h4[normalize-space()='%s']/ancestor::div[contains(@class,'room')]",
    )
    room_status_tag = (By.XPATH, "//div[@class='toolbar']//label[contains(text(), '%s')]")
    floor = (By.XPATH, "//div[@class='tab']//a[normalize-space()='%s']")
    first_room = (
        By.XPATH,
        "//div[@class='tab-content' and not(@style)]//div[@class='card-wrap']//div[@class='card--room'][1]",
    )

    room_number = (
        By.XPATH,
        "//div[@class='tab-content' and not(@style)]//div[@class='card-wrap']//div[@class='card--room'][1]//h4",
    )
    room_style = (
        By.XPATH,
        "//div[@class='tab-content' and not(@style)]//div[@class='card-wrap']//div[@class='card--room'][1]//div[2]/span",
    )
    room_stay_days = (
        By.XPATH,
        "//div[@class='tab-content' and not(@style)]//div[@class='card-wrap']//div[@class='card--room'][1]//div[2]/span[2]",
    )
    room_guest_name = (
        By.XPATH,
        "//div[@class='tab-content' and not(@style)]//div[@class='card-wrap']//div[@class='card--room'][1]//div[3]",
    )

    # ----- 櫃台入住 視窗 -----
    days_dropdown = (By.XPATH, "//label[normalize-space()='天數']/following-sibling::span")
    days_options = (By.XPATH, "//div[text()='%s : %s']")

    # ----- 房間細節 視窗 -----
    btn_edit_field = (By.XPATH, "//div[@data-field-id='%s']/button")
    btn_guest_function_maindesk = (By.XPATH, "//td[@data-field-id='%s']")
    btn_guest_function_span = (By.XPATH, "//span[@data-field-id='%s']")
    btn_add_guest = (By.XPATH, "//span[@data-field-id='appendSingleRow']")
    notice_content_text = (By.XPATH, "//div[@data-field-id='notice_rmk']/textarea")
    guest_row_field = (By.XPATH, "(//td[@data-field-id='alt_nam']/span//input[1])[last()]")
    text_precredit_amount = (By.XPATH, "//td[@data-field-id='precredit_amt']/label")
    check_precredit = (By.XPATH, "//td[@data-field-id='notes']/i")
    guest_remark_column = (By.XPATH, "//td[@data-field-id='fo_remark']//input")

    # ----- 改退房日 視窗 -----
    # -- 日期選單 --
    date_by_field = (By.XPATH, "//label[normalize-space()='%s']/following-sibling::div/input")
    btn_date = (By.XPATH, "//span[contains(text(), '年') and @role='button']")
    date_year = (By.XPATH, "//table[@class='el-year-table']//a[text()='%s']")
    date_mon = (By.XPATH, "//table[@class='el-month-table']//a[text()='%s']")
    date_day = (By.XPATH, "//table[@class='el-date-table']//td[normalize-space()='%s']")
    # -- 日期選單 End --
    room_checkbox_in_table = (By.XPATH, "//td[@field='ck']//input[@type='checkbox']")

    # ----- 改房價 視窗 -----
    btn_save = (By.XPATH, "(//button[child::img])[last()]")
    input_row_data = (By.XPATH, "//td[@field='%s']//span/input[1]")

    # ----- 換房 視窗 -----
    dirty_room_ck = (By.XPATH, "//div[@data-field-id='set_dirty_room']//span")

    # ----- 指定訂金 + 指定公帳號 視窗 -----
    input_dropdown_field = (
        By.XPATH,
        "//label[normalize-space()='%s']/following-sibling::span/span/following-sibling::input",
    )
    room_dt_row = (By.XPATH, "//tr[.//div[text()='%s']]")
    first_master_room = (
        By.XPATH,
        "//div[@class='datagrid-header' and .//span[text()='公帳號']]/following-sibling::div//tr",
    )

    # ----- 注意事項 視窗 -----
    notice_content_textarea = (By.XPATH, "//textarea[@data-field-id='noticeContent']")

    # ----- 預授權 視窗 -----
    btn_edit_precredit = (By.XPATH, "(//button[child::img[@alt='edit']])[last()]")

    # ----- 車號 視窗 -----
    carNos_textarea = (By.XPATH, "//div[@data-field-id='carNos']//textarea")
