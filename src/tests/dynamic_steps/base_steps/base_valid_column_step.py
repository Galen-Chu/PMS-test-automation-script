from abc import ABC, abstractmethod


class BaseValidColumnStep(ABC):

    def __init__(self, web):
        self.web = web

    @abstractmethod
    def input_data(self):
        pass

    @abstractmethod
    def assert_result(self):
        pass
