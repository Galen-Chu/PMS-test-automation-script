from selenium.webdriver.common.by import By
from locators.base_locator import BaseLocator


class GuestAccountLocator(BaseLocator):

    btn_guest_maintain = (By.XPATH, "//button[@data-field-id='openPMS0310011']")

    # ----- 入帳 ----
    btn_credit = (By.XPATH, "//button[@data-field-id='r_1040']")
    select_consumption = (By.XPATH, "//div[@class='el-select select required']")
    input_amount = (
        By.XPATH,
        "(//div[@class='panel-title' and text()='入帳']/parent::div\
                    /following-sibling::div//input[contains(@id, 'numerictextbox_')])[1]",
    )
    # ----- 入帳 END -----

    # ----- 住客帳維護單筆 -----
    label_deposit = (By.XPATH, "//label[text()='%s']/following-sibling::input")
    td_deposit_info = (
        By.XPATH,
        "(//div[@aria-labelledby='tab-1']//tr/td[@field='%s']/div)[last()]",
    )

    btn_item_detail = (
        By.XPATH,
        "//div[@aria-labelledby='tab-1']//tr/td[@field='item_tot' and child::div[text()='200']]\
                       /following-sibling::td[@field='detail_sta']//span",
    )
    text_input_values = (
        By.XPATH,
        "//div[@data-field-id='%s']//span[@class='e-input-value']/span/span",
    )  # rsptCode , shiftCode , roomNos
    text_input_value = (
        By.XPATH,
        "//div[@data-field-id='%s']//span[@class='e-input-value']/span",
    )  # rsptCode , shiftCode , roomNos
    row_item = (
        By.XPATH,
        "//tr[@aria-rowindex='%s']//td[@field='%s']",
    )  # 1, smallType , 1 , productNos

    btn_checkout_more = (
        By.XPATH,
        "//label[text()='已結帳總額']/following-sibling::span[@class='sub-button--more']",
    )
    # ----- 住客帳維護單筆 END -----

    # ----- 結帳 -----
    btn_add_checkout_type = (
        By.XPATH,
        "//th[@data-field-id='openPay']/div[@class='sub-button--add']",
    )
    # ----- 結帳 END -----

    # ----- 已結帳 -----
    row_in_table = (
        By.XPATH,
        "//th[normalize-space()='%s']/ancestor::thead/following-sibling::tbody//tr",
    )
    th_position = (By.XPATH, "//th[normalize-space()='%s']/preceding-sibling::th")
    # ----- 已結帳 END -----

    # ----- 發票明細 ----
    text_uni_cod = (By.XPATH, "//input[@name='uni_cod']")
    # ----- 發票明細 END ----
