from selenium.webdriver.common.by import By
from locators.base_locator import BaseLocator


class BookingQuantityForecastReportLocator(BaseLocator):

    # ----- 查詢條件區 -----
    # qry_dat 為 Element UI daterange picker（雙 input：[1]起日 [2]訖日）；case 用預設不操作
    input_qry_dat_start = (By.XPATH, "(//div[@data-field-id='qry_dat']//input)[1]")
    input_qry_dat_end = (By.XPATH, "(//div[@data-field-id='qry_dat']//input)[2]")

    # ----- 報表區 -----
    iframe_report = (By.ID, "reportIframe")
    # btn_search 沿用 BaseLocator（contains '_doSearch' match 'undefined_doSearch'）
