from .registry import CLASS_SUBSCRIBERS

class Dispatcher:

    @staticmethod
    async def dispatch(event: dict):
        event_name = event.get("event_name")
        handlers = CLASS_SUBSCRIBERS.get(event_name)

        if handlers:
            for handler in handlers:
                handler = handler()
                await handler.handle(event)
