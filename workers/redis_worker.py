import json
import asyncio
from redis.asyncio import Redis
from modules.shared.bus.event.application import Dispatcher
from modules.shared.bus.event.application import load_subscribers
from modules.shared.environ.infrastructure import PyEnviron

load_subscribers()

environ = PyEnviron()
redis = Redis(
    host=environ.get_str("REDIS_HOST", "localhost"),
    port=environ.get_int("REDIS_PORT", 6379),
    decode_responses=True
)

async def worker():
    last_id = "$"

    while True:
        messages = await redis.xread(
            {"events": last_id},
            block=5000,
            count=10
        )

        if not messages:
            continue

        for stream_name, entries in messages:
            for message_id, data in entries:
                event = json.loads(data["event"])

                print(event["event_name"])

                # procesar
                await Dispatcher.dispatch(event=event)

                last_id = message_id

def main():
    asyncio.run(worker())

if __name__ == "__main__":
    main()
