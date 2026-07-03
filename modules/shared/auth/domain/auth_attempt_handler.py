from abc import ABC
from abc import abstractmethod


class AuthAttemptHandler(ABC):

    @staticmethod
    def _attempts_key(email: str) -> str:
        return f"login_attempts:{email}"

    @staticmethod
    def _blocked_key(email: str) -> str:
        return f"login_blocked:{email}"

    @abstractmethod
    async def is_blocked(self, email: str) -> bool:
        """function to check if email is blocked"""
        pass

    @abstractmethod
    async def register_failed_attempt(self, email: str) -> int:
        """function to register failed attempt"""
        pass

    @abstractmethod
    async def clear_attempts(self, email: str):
        """function to clear failed attempts"""
        pass
