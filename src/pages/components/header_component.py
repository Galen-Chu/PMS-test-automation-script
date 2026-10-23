from pages.athena_base_page import AthenaBasePage
from locators.header_locator import HeaderLocator


class HeaderComponent(AthenaBasePage):

    def __init__(self, driver):
        super().__init__(driver, HeaderLocator())

    def expand_menu(self, func_name):
        tmp_locator = self.formator_locator(self.locator.btn_menu_item, func_name)
        self.click(tmp_locator)
        # 等待選單展開（任一子選項出現）
        self.wait_visible(self.locator.expanded_menu_item)
        return self

    def to_func_page(self, func_name):
        tmp_locator = self.formator_locator(self.locator.btn_dropdown_item, func_name)
        self.click(tmp_locator)
        return self
