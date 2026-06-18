from uuid import UUID
from modules.whatsapp_webhook.domain import WhatsappWebhook
from modules.whatsapp_webhook.domain.exceptions import WhatsappWebhookAlreadyExist
from modules.shared.persistence.domain import UnitOfWork
from modules.shared.bus.event.domain import EventBus
from modules.whatsapp_webhook.domain import WhatsappWebhookRepository


class WhatsappWebhookCreator:

    def __init__(
        self,
        unit_of_work: UnitOfWork,
        event_bus: EventBus,
        whatsapp_webhook_repository: WhatsappWebhookRepository,
    ):
        self.__unit_of_work = unit_of_work
        self.__event_bus = event_bus
        self.__whatsapp_webhook_repository = whatsapp_webhook_repository

    async def create(self, id: UUID, payload: dict):

        if await self.__whatsapp_webhook_repository.get(id=id):
            raise WhatsappWebhookAlreadyExist(f"WhatsApp webhook with id:{id} already exists")

        webhook = WhatsappWebhook.create(
            id=id,
            payload=payload,
        )

        async with self.__unit_of_work:
            await self.__whatsapp_webhook_repository.add(webhook)

        await self.__event_bus.publish(webhook.pull_domain_events())
