from abc import ABC, abstractmethod


class BaseServiceItemStep(ABC):

    def __init__(self, web):
        self.web = web
        self.is_price_editable = None

    @abstractmethod
    def clear_service_item(self):
        pass

    @abstractmethod
    def input_service_item_info(self, item, money):
        pass

    @abstractmethod
    def valid_tab_service_info(self, item, money):
        pass

    @abstractmethod
    def valid_tab_expense_detail_info(self, item, money):
        pass
