from abc import ABC, abstractmethod


class BaseRateCodStep(ABC):

    def __init__(self, web):
        self.web = web

    @abstractmethod
    def input_rate_cod_info(self, rate_cod):
        pass

    def set_use_duration(self):
        pass

    def set_rate_cod_price(self):
        pass

    def set_service_items(self):
        pass

    @abstractmethod
    def valid_rate_cod_info(self, rate_cod):
        pass
