from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from modules.shared.persistence.domain import UnitOfWork
from modules.shared.bus.event.domain import EventBus
from modules.whatsapp_webhook.domain import WhatsappWebhookRepository
from modules.whatsapp_webhook.domain.exceptions import WhatsappWebhookAlreadyExist
from modules.shared.http.domain import status
from modules.shared.http.domain import messages
from modules.whatsapp_webhook.application import WhatsappWebhookCreator
from modules.whatsapp_webhook.infrastructure import PgWhatsappWebhookRepository
from modules.shared.persistence.infrastructure import AlchemyUnitOfWork


class WhatsappWebhookCreatorController:

    def __init__(
        self,
        session: AsyncSession,
        event_bus: EventBus,
        unit_of_work: UnitOfWork | None = None,
        whatsapp_webhook_repository: WhatsappWebhookRepository | None = None,
    ):
        self.__session = session
        self.__event_bus = event_bus
        self.__unit_of_work = unit_of_work or AlchemyUnitOfWork(session=self.__session)
        self.__whatsapp_webhook_repository = whatsapp_webhook_repository or PgWhatsappWebhookRepository(session=self.__session)

    async def create(self, payload: dict):
        try:
            whatsapp_webhook_creator = WhatsappWebhookCreator(
                unit_of_work=self.__unit_of_work,
                event_bus=self.__event_bus,
                whatsapp_webhook_repository=self.__whatsapp_webhook_repository,
            )

            await whatsapp_webhook_creator.create(id=uuid4(), payload=payload)
            response = {"success": True, "message": messages.SUCCESS_MESSAGE, "data": {}}, status.HTTP_201_CREATED

        except WhatsappWebhookAlreadyExist as ex:
            response = {"success": False, "message": f"{ex}", "data": {}}, status.HTTP_409_CONFLICT
            return response

        except Exception as ex:
            response = {"success": False, "message": messages.INTERNAL_SERVER_ERROR, "data": {}}, status.HTTP_500_INTERNAL_SERVER_ERROR
            return response

        else:
            return response
