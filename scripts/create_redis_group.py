from redis.asyncio import Redis
from modules.shared.environ.infrastructure import PyEnviron
from modules.shared.bus.event.infrastructure.redis import StramManager
from modules.shared.logger.infrastructure import PyLogger

environ = PyEnviron()
redis = Redis(
    host=environ.get_str("REDIS_HOST", "localhost"),
    port=environ.get_int("REDIS_PORT", 6379),
    decode_responses=True
)
logger = PyLogger(
    level=environ.get_str("LOG_LEVEL"),
    format=environ.get_str("LOG_FORMAT"),
)

async def create_redis_group():
    stream_manager = StramManager(redis, logger)
    await stream_manager.create_group(
        stram_name=environ.get_str("MESSAGE_QUEUE_NAME"),
        group_name=environ.get_str("MESSAGE_GROUP_NAME"),
        id="0"
    )

if __name__ == "__main__":
    import asyncio
    asyncio.run(create_redis_group())
