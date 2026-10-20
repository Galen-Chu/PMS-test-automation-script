import allure
from pages.login_page import LoginPage
from pages.base_page import BasePage
from tools.driver_helper import DriverHelper


@allure.feature("登入頁")
class TestLogin:

    @allure.story("登入成功")
    def test_login(self, logged_in_driver):
        """驗證登入成功（登入動作由 logged_in_driver fixture 完成）"""
        pages = [LoginPage, BasePage]
        web = DriverHelper.get_logged_in_browser(pages)
        web.login_page.screenshot("登入成功").sleep(2)
