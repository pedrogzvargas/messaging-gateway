import json
from redis.asyncio import Redis
from modules.shared.bus.event.domain import EventBus
from modules.shared.bus.event.infrastructure.custom_json_encoder import CustomJSONEncoder


class RedisEventBus(EventBus):
    """
    Redis event bus creator
    """

    def __init__(self, redis_client: Redis, stream_name: str):
        self.__redis_client = redis_client
        self.__stream_name = stream_name

    async def publish(self, domain_events):
        """function to publish on Redis"""

        for domain_event in domain_events:
            json_domain_event = json.dumps(domain_event.to_primitives(), cls=CustomJSONEncoder).encode("utf-8")
            await self.__redis_client.xadd(
                name=self.__stream_name,
                fields={
                    "event": json_domain_event
                },
            )
