from redis.asyncio import Redis
from modules.shared.environ.domain import Environ
from modules.shared.auth.domain import AuthAttemptHandler


class RedisAuthAttemptHandler(AuthAttemptHandler):
    def __init__(self, redis: Redis, environ: Environ):
        self.__redis = redis
        self.__environ = environ

    async def is_blocked(self, email: str) -> bool:
        return await self.__redis.exists(self._blocked_key(email)) == 1

    async def register_failed_attempt(self, email: str) -> int:
        attempts_key = self._attempts_key(email)
        attempts = await self.__redis.incr(attempts_key)
        auth_max_attempts = self.__environ.get_int('AUTH_MAX_ATTEMPTS')
        auth_block_time_seconds = self.__environ.get_int('AUTH_BLOCK_TIME_SECONDS')
        auth_attempt_window_seconds = self.__environ.get_int('AUTH_ATTEMPT_WINDOW_SECONDS')

        if attempts == 1:
            await self.__redis.expire(name=attempts_key, time=auth_attempt_window_seconds)

        if attempts == auth_max_attempts:
            await self.__redis.set(name=self._blocked_key(email), value="1", ex=auth_block_time_seconds)
            await self.__redis.delete(attempts_key)

        return attempts

    async def clear_attempts(self, email: str):
        return await self.__redis.delete(self._attempts_key(email))
