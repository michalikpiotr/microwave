from abc import ABC, abstractmethod


class DbCrud(ABC):
    """Interface for getting data from db"""

    @abstractmethod
    def get_item(self, item):
        pass

    @abstractmethod
    def create_item(self, item, values):
        pass
