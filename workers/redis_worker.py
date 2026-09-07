import json
import asyncio
from redis.asyncio import Redis
from modules.shared.bus.event.application import Dispatcher
from modules.shared.bus.event.application import load_subscribers
from modules.shared.environ.infrastructure import PyEnviron
from modules.shared.logger.infrastructure import PyLogger

load_subscribers()

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

async def worker():
    consumer_name = "worker-1"
    group_name = environ.get_str("MESSAGE_GROUP_NAME")
    stream_name = environ.get_str("MESSAGE_QUEUE_NAME")

    while True:
        try:
            messages = await redis.xreadgroup(
                groupname=group_name,
                consumername=consumer_name,
                streams={stream_name: ">"},
                count=1,
                block=5000
            )
        except Exception as ex:
            logger.error(f"redis_worker: failed to read from stream: {ex}")
            continue

        if not messages:
            continue

        for stream_name, entries in messages:
            for message_id, data in entries:
                try:
                    event = json.loads(data["event"])

                    logger.info(event["event_name"])

                    # procesar
                    await Dispatcher.dispatch(event=event)
                    await redis.xack(
                        stream_name,
                        group_name,
                        message_id
                    )

                except Exception as ex:
                    logger.error(f"redis_worker: failed to process message {message_id}: {ex}")

def main():
    asyncio.run(worker())

if __name__ == "__main__":
    main()
