from abc import ABC
from abc import abstractmethod


class Logger(ABC):

    @abstractmethod
    def debug(self, message):
        """function to log debug message"""
        pass

    @abstractmethod
    def info(self, message):
        """function to log info message"""
        pass

    @abstractmethod
    def warning(self, message):
        """function to log warning message"""
        pass

    @abstractmethod
    def error(self, message):
        """function to log error message"""
        pass

