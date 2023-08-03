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
    def __enter__(self):
        """Query context manager enter"""

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Query context manager exit"""
