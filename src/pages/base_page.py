from time import sleep
import allure
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    ElementNotInteractableException,
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from locators.base_locator import BaseLocator


class BasePage:

    def __init__(self, driver, locator=None):
        # 預設 BaseLocator：測試的 pages 清單會直接實例化 BasePage 取用通用方法
        self.locator = locator if locator is not None else BaseLocator()
        self.driver = driver

    def format_locator(self, locator, values):
        # 直接格式化 locator 元組（避免 str(tuple)%value 在 Windows 上損壞中文字元）
        by, selector = locator
        return (by, selector % values)

    def click(self, locator, retries=5, delay=1):
        for attempt in range(retries):
            try:
                element = self.driver.find_element(*locator)
                if element is None:
                    # chromedriver 在頁面轉跳期間可能回傳 null 而非丟例外；
                    # 視同找不到，交給重試迴圈等頁面穩定
                    raise NoSuchElementException("find_element returned null (page transitioning)")
                element.click()
                return  # 點擊成功就結束
            except (
                ElementClickInterceptedException,
                ElementNotInteractableException,
                NoSuchElementException,
                StaleElementReferenceException,
            ) as _:
                if attempt < retries - 1:
                    sleep(delay)
                else:
                    raise

    def clear(self):
        self.click(self.locator.btn_clear)
        return self

    def input_clear(self, locator):
        element = self.driver.find_element(*locator)
        element.send_keys(Keys.CONTROL, "a")
        element.send_keys(Keys.BACKSPACE)
        return self

    def input_with_clear(self, locator, value):
        element = self.driver.find_element(*locator)
        element.clear()
        element.send_keys(value)

    def input(self, locator, value):
        self.driver.find_element(*locator).send_keys(value)

    def pointer_to_element(self, locator):
        target_element = self.driver.find_element(*locator)
        actions = ActionChains(self.driver)
        actions.move_to_element(target_element).perform()

    def has_element(self, locator, timeout=2):
        """顯式 presence 檢查。檢查期間將 implicit wait 歸零，
        避免與 WebDriverWait 混用造成逾時時間不可預期（Selenium 反模式）。"""
        self.driver.implicitly_wait(0)
        try:
            WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False
        finally:
            self.driver.implicitly_wait(10)

    def wait_clickable(self, locator, timeout=10):
        WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))
        return self

    def wait_visible(self, locator, timeout=10):
        WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
        return self

    def wait_gone(self, locator, timeout=10):
        WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located(locator))
        return self

    def wait_present(self, locator, timeout=10):
        WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))
        return self

    def wait_until(self, condition, timeout=10):
        """等待自訂條件（condition 為接受 driver 的 callable，回傳 Truthy 即完成）"""
        WebDriverWait(self.driver, timeout).until(condition)
        return self

    def screenshot(self, file_name):
        if hasattr(self.driver, "get_screenshot_as_png"):
            allure.attach(
                self.driver.get_screenshot_as_png(), file_name, allure.attachment_type.PNG
            )
        return self

    def sleep(self, seconds):
        sleep(seconds)
        return self

    def assert_data(self, title, real, expect):
        allure.attach(
            f"Real: {real} , Expect: {expect}", f"實際結果-{title}", allure.attachment_type.TEXT
        )
        assert real == expect

    def assert_data_in_list(self, title, reals, expect):
        allure.attach(
            f"Real: {reals} , Expect: {expect}", f"實際結果-{title}", allure.attachment_type.TEXT
        )
        assert expect in reals

    def assert_data_not_in_list(self, title, reals, expect):
        allure.attach(
            f"Real: {reals} , Expected not to find: {expect}",
            f"實際結果-{title}",
            allure.attachment_type.TEXT,
        )
        assert expect not in reals

    def assert_data_has_count(self, title, real):
        allure.attach(f"Real: {real}", f"實際結果-{title}", allure.attachment_type.TEXT)
        assert int(real) > 0
