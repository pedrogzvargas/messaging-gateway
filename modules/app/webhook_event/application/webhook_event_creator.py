from uuid import UUID
from modules.app.webhook_event.domain import WebhookEvent
from modules.app.webhook_event.domain.exceptions import WebhookEventAlreadyExist
from modules.shared.persistence.domain import UnitOfWork
from modules.shared.bus.event.domain import EventBus
from modules.app.webhook_event.domain import WebhookEventRepository


class WebhookEventCreator:

    def __init__(
        self,
        unit_of_work: UnitOfWork,
        event_bus: EventBus,
        webhook_event_repository: WebhookEventRepository,
    ):
        self.__unit_of_work = unit_of_work
        self.__event_bus = event_bus
        self.__webhook_event_repository = webhook_event_repository

    async def create(self, id: UUID, provider: str, provider_id: str, payload: dict):

        if await self.__webhook_event_repository.get(id=id):
            raise WebhookEventAlreadyExist(f"Webhook event with id:{id} already exists")

        webhook = WebhookEvent.create(
            id=id,
            provider=provider,
            provider_id=provider_id,
            payload=payload,
        )

        async with self.__unit_of_work:
            await self.__webhook_event_repository.add(webhook)

        await self.__event_bus.publish(webhook.pull_domain_events())
