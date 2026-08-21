from selenium.webdriver.common.by import By

from locators.base_locator import BaseLocator


class CompanyPanelLocator(BaseLocator):

    btn_target_contract = (By.XPATH, "//tr[contains(@id, 'companyContractDgId')]")
    btn_add_contract = (By.XPATH, "//div[@class='panel-title' and contains(text(), '商務公司維護')]\
                        /parent::div/following-sibling::div//div[@id='contractPanel']//button[1]")
    btn_remove_contract = (
        By.XPATH,
        "//div[@class='panel-title' and contains(text(), '商務公司維護')]\
                           /parent::div/following-sibling::div//div[@id='contractPanel']//button[2]",
    )
    input_contract_no = (
        By.XPATH,
        "(//tr[contains(@id, 'companyContractDgId')]/td[@field='contract_cod']//input)[2]",
    )
    input_contract_start_date = (
        By.XPATH,
        "//tr[contains(@id, 'companyContractDgId')]/td[@field='begin_dat']//a",
    )
    input_contract_end_date = (
        By.XPATH,
        "//tr[contains(@id, 'companyContractDgId')]/td[@field='end_dat']//a",
    )
    select_hotel_cod = (
        By.XPATH,
        "//tr[contains(@id, 'companyContractDgId')]/td[@field='hotel_cod']//a",
    )
    select_rate_cod = (
        By.XPATH,
        "//tr[contains(@id, 'companyContractDgId')]/td[@field='rate_cod']//a",
    )

    td_input_value = (By.XPATH, "//tr[contains(@id, 'companyContractDgId')]/td[@field='%s']/div")
    item_cod = (By.XPATH, "(//div[@class='combobox-item' and text()='%s'])[last()]")

    btn_save = (By.XPATH, "(//div[child::div[@class='panel-title' and text()='商務公司維護']]\
                /following-sibling::div//div[contains(@class, 'justify-content-end')]//button)[1]")

    calendar_title = (
        By.XPATH,
        "//div[contains(@class, 'panel-htop') and not(contains(@style, 'none'))]//div[@class='calendar-title']",
    )
    calendar_year = (
        By.XPATH,
        "//div[contains(@class, 'panel-htop') and not(contains(@style, 'none'))]//input[@class='calendar-menu-year']",
    )
    calendar_mon = (
        By.XPATH,
        "//div[contains(@class, 'panel-htop') and not(contains(@style, 'none'))]\
                //table[@class='calendar-mtable']//td[text()='%s']",
    )
    calendar_day = (
        By.XPATH,
        "//div[contains(@class, 'panel-htop') and not(contains(@style, 'none'))]//div[@class='calendar-body']\
                    //td[contains(@class,'calendar-day') and not(contains(@class, 'calendar-other-month')) and text()='%s']",
    )

    btn_rm_special_contract = (By.XPATH, "//span[@class='button-remove--s']")
    btn_add_special_contract = (By.XPATH, "//span[@class='button-add--s']")
    select_special_rate_cod = (By.XPATH, "//div[@data-field-id='ratecodMnForCratecod']")
    item_special_rate_cod = (By.XPATH, "//li[@data-value='%s']")
    confirm_button = (By.XPATH, "//div[@data-field-id='confirmButton']/button")
