from selenium.webdriver.common.by import By
from locators.base_locator import BaseLocator


class SharePanelLocator(BaseLocator):

    panel_footer_btn = (
        By.XPATH,
        "//div[@class='panel-title' and text()='%s']/parent::div/following-sibling::div//button[normalize-space()='%s']",
    )
    panel_save = (
        By.XPATH,
        "//div[@class='panel-title' and text()='%s']/parent::div/following-sibling::div//img[@alt='save']",
    )
    panel_select = (
        By.XPATH,
        "//div[@class='panel-title' and text()='%s']/parent::div/following-sibling::div//input[@placeholder='請選擇']",
    )
    panel_select_by_name = (
        By.XPATH,
        "//div[@class='panel-title' and text()='%s']/parent::div/following-sibling::div//input[@placeholder='請選擇']",
    )
    btn_pnael_close = (
        By.XPATH,
        "(//div[@class='panel-title' and text()='%s']/following-sibling::div/a)[last()]",
    )

    # ---- 開班 panel ----
    label_select = (By.XPATH, "//label[normalize-space()='%s']/following-sibling::div//input")
    label_input = (By.XPATH, "(//label[normalize-space()='%s']/following-sibling::input)[last()]")
    label_input_2 = (
        By.XPATH,
        "//label[normalize-space()='%s']/following-sibling::div//input[not(@validatehidden)]",
    )
    label_input_3 = (
        By.XPATH,
        "(//div[child::div[child::span[normalize-space()='%s']]]\
                     /following-sibling::div//input[not(@aria-label='hidden')])[last()]",
    )
    # ---- 開班 panel END ----

    # ---- 房價 panel ----
    label_span_select_3 = (
        By.XPATH,
        "//div[child::div[child::span[normalize-space()='%s']]]\
                           /following-sibling::div",
    )
    label_span_select_value_3 = (
        By.XPATH,
        "//div[child::div[child::span[normalize-space()='%s']]]\
                                 /following-sibling::div//span[@class='e-input-value']",
    )
    label_span_select_item_3 = (
        By.XPATH,
        "//li[contains(@class, 'e-list-item') and normalize-space()='%s']",
    )

    label_span_select = (By.XPATH, "//label[normalize-space()='%s']/following-sibling::span")
    label_span_select_value = (
        By.XPATH,
        "//label[normalize-space()='%s']/following-sibling::span/input[@type='text' and following-sibling::input]",
    )
    label_span_select_item = (By.XPATH, "//div[@class='combobox-item' and text()='%s']")
    label_checkbox = (
        By.XPATH,
        "(//label[normalize-space()='%s']//input[@type='checkbox'])[last()]",
    )
    label_name = (By.XPATH, "//a[normalize-space()='%s']")

    label_duration = (By.XPATH, "//label[normalize-space()='%s']/following-sibling::div/input")
    # ---- 房價 end ----

    # ---- 房價多語系panel ----
    label_input_by_lang = (By.XPATH, "//td[normalize-space()='%s']/following-sibling::td/input")
    btn_confirm = (By.XPATH, "//button[@class='button--confirm']")
    # ---- 房價多語系panel end ----

    # ---- 使用期間 panel ----
    panel_add = (
        By.XPATH,
        "//div[child::div[contains(text(), '%s')]]/following-sibling::div//span[@class='sub-button--add']",
    )
    input_column_by_header = (
        By.XPATH,
        "//th[normalize-space()='%s']/ancestor::table\
                              /tbody/tr/td[count(//tr//th[normalize-space()='%s']/preceding-sibling::th)+1]",
    )
    drop_down_item = (By.XPATH, "//div[@class='combobox-item' and normalize-space()='%s']")
    # ---- 使用期間 panel end ----

    detail_tab_name = (By.XPATH, "//div[@id='tab-%s']")
    text_cratecod_mn = (By.XPATH, "//td[@field='alt_nam']/div[text()='%s']")
