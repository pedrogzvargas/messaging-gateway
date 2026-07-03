from uuid import UUID
from abc import ABC
from abc import abstractmethod


class PasswordResetTokenRepository(ABC):

    @abstractmethod
    async def save(self, token: str, user_id: UUID, expires_in: int) -> None:
        pass

    @abstractmethod
    async def get_user_id(self, token: str) -> UUID | None:
        pass

    @abstractmethod
    async def delete(self, token: str) -> None:
        pass
