from selenium.webdriver.common.by import By
from locators.base_locator import BaseLocator


class GroupManagementLocator(BaseLocator):

    # ----- 列表 Grid -----
    row_group = (By.XPATH, "//td[@field='master_nos' and normalize-space()='%s']")
    text_list_co_dat = (By.XPATH, "(//td[@field='co_dat'])[2]")

    # ----- 改退房日 Panel -----
    cell_co_date = (
        By.XPATH,
        "//div[contains(@class,'el-picker-panel')]//td[contains(@class,'available') and normalize-space()='%s']",
    )
    text_eco_dat = (By.XPATH, "(//td[@field='eco_dat'])[2]")
    btn_close_panel_by_title = (
        By.XPATH,
        "(//div[contains(@class,'panel-title') and normalize-space()='%s']"
        "/..//a[contains(@class,'panel-tool-close')])[last()]",
    )

    # ----- 清子房間（#501）-----
    # 已入住 tab 子房勾選（%s=房號，tr scope；房退房後離開 grid，find_elements 空 → has_ci_room 偵測移除）
    checkbox_ci_sub_room = (
        By.XPATH,
        "//tr[td[@field='room_nos' and normalize-space()='%s']]//input[@name='ck']",
    )
    # 清子房間按鈕（團體明細 Panel 操作列）
    btn_clean_sub_room = (By.XPATH, "//button[normalize-space()='清子房間']")
    # 錯誤提示 dialog（未入預估款 → Early C/O 詢問）內子房勾選
    # dialog 只列錯誤子房不用指定房號；panel-title scope 避背景已入住 tab grid 同名 ck
    checkbox_err_dialog_ck = (
        By.XPATH,
        "//div[contains(@class,'panel-title') and normalize-space()='錯誤提示']"
        "/ancestor::div[contains(@class,'panel')]//input[@name='ck']",
    )
    # 錯誤提示 dialog 確定（雙重 confirm 共用：第一次→Early C/O 詢問，第二次→退房完成）
    btn_err_dialog_confirm = (
        By.XPATH,
        "//div[contains(@class,'panel-title') and normalize-space()='錯誤提示']"
        "/ancestor::div[contains(@class,'panel')]//button[normalize-space()='確定']",
    )
