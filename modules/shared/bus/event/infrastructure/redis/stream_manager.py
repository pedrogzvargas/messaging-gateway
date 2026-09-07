from redis.asyncio import Redis
from modules.shared.logger.domain import Logger


class StramManager:

    def __init__(self, redis_client: Redis, logger: Logger):
        self.__redis_client = redis_client
        self.__logger = logger

    async def create_group(self, stram_name: str, group_name: str, id: str = "$"):
        try:
            await self.__redis_client.xgroup_create(
                name=stram_name,
                groupname=group_name,
                id=id,
                mkstream=True,
            )

            self.__logger.info(f"Stram {stram_name} has been created")

        except Exception as ex:
            self.__logger.error(f"redis_worker: failed to read from stream: {ex}")
