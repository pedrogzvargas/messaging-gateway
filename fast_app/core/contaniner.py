from redis.asyncio import Redis
from .config import get_settings
from modules.shared.bus.event.infrastructure import RedisEventBus

class Container:

    def __init__(self):
        settings = get_settings()

        self.redis_client = Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            decode_responses=True
        )

        self.event_bus = RedisEventBus(
            redis_client=self.redis_client,
        )
