""" Abstract available db operations"""

from abc import ABC, abstractmethod


class DbCrud(ABC):
    """Interface for getting data from db"""

    @abstractmethod
    def get_item(self, item):
        """Get db item"""

    @abstractmethod
    def create_item(self, item, values):
        """Create db item"""

    @abstractmethod
    def execute_transaction(self):
        """Execute transaction db"""
