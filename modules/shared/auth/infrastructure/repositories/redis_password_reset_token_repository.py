from uuid import UUID
from redis.asyncio import Redis
from modules.shared.auth.domain.repositories import PasswordResetTokenRepository


class RedisPasswordResetTokenRepository(PasswordResetTokenRepository):

    def __init__(self, redis: Redis):
        self.__redis = redis

    async def save(self, token: str, user_id: UUID, expires_in: int) -> None:
        await self.__redis.set(
            name=f"password_reset:{token}",
            value=str(user_id),
            ex=expires_in,
        )

    async def get_user_id(self, token: str) -> UUID | None:
        user_id = await self.__redis.get(f"password_reset:{token}")

        if user_id:
            return UUID(user_id)

        return None

    async def delete(self, token: str) -> None:
        await self.__redis.delete(f"password_reset:{token}")
