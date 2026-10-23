from pages.athena_base_page import AthenaBasePage
from locators.pre_credit_locator import PreCreditLocator


class PreCreditComponent(AthenaBasePage):

    def __init__(self, driver):
        super().__init__(driver, PreCreditLocator())

    def click_add_precredit(self):
        self.click(self.locator.btn_add_precredit)
        return self

    def create_precredit(self, card_type, card_number, expiredate, authcod, amount):
        card_type_dropdown_locator = self.formator_locator(
            self.locator.card_type_dropdown, "payWay"
        )
        self.click(card_type_dropdown_locator)
        card_type_locator = self.formator_locator(self.locator.card_type_select, card_type)
        self.click(card_type_locator)
        card_number_locator = self.formator_locator(self.locator.input_precredit_label, "creditNos")
        self.input(card_number_locator, card_number)
        expiredate_locator = self.formator_locator(self.locator.input_precredit_label, "expiraDat")
        self.input(expiredate_locator, expiredate)
        authcod_locator = self.formator_locator(self.locator.input_precredit_label, "preauthCod")
        self.input(authcod_locator, authcod)
        amount_locator = self.formator_locator(self.locator.input_precredit_label, "precreditAmt")
        self.input(amount_locator, amount)
        return self

    def get_precredit_info(self, field):
        precredit_info_locator = self.formator_locator(self.locator.text_precredit_label, field)
        precredit_info = self.driver.find_element(*precredit_info_locator).text
        return precredit_info

    def btn_del_precredit_is_enabled(self):
        return self.driver.find_element(*self.locator.btn_delete).get_attribute("disabled")
