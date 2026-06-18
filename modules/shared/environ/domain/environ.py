from abc import ABC
from abc import abstractmethod


class Environ(ABC):

    @abstractmethod
    def get_str(self, key, default=None):
        """function to get environ variable as str"""
        pass

    @abstractmethod
    def get_int(self, key, default=None):
        """function to get environ variable as int"""
        pass

    @abstractmethod
    def get_bool(self, key, default=None):
        """function to get environ variable as bool"""
        pass
