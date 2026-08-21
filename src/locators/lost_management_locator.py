from selenium.webdriver.common.by import By
from locators.base_locator import BaseLocator
from locators.lost_item_locator import LostItemLocator


class LostManagementLocator(BaseLocator, LostItemLocator):
    # ----- 失物管理頁面 -----
    status_close = (
        By.XPATH,
        "//label[@title='狀態']/following-sibling::div//i[contains(@class,'el-icon-close')]",
    )
    rent_day = (By.XPATH, "//label[@title='查詢日期']/following-sibling::div/input")
    # ----- 失物管理頁面 End ----

    # ----- 驗證失物資料 -----
    text_data_in_page = (
        By.XPATH,
        "//div[@class='panel datagrid panel-htop']//tr[@datagrid-row-index='%s']//td[@field='%s']/div",
    )
    # ----- 驗證失物資料 End -----
