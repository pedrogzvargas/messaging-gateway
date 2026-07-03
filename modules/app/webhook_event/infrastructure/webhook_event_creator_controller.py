from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from modules.shared.persistence.domain import UnitOfWork
from modules.shared.bus.event.domain import EventBus
from modules.app.webhook_event.domain import WebhookEventRepository
from modules.app.webhook_event.domain.exceptions import WebhookEventAlreadyExist
from modules.shared.http.domain import status
from modules.shared.http.domain import messages
from modules.app.webhook_event.application import WebhookEventCreator
from modules.app.webhook_event.infrastructure import PgWebhookEventRepository
from modules.shared.persistence.infrastructure import AlchemyUnitOfWork


class WebhookEventCreatorController:

    def __init__(
        self,
        session: AsyncSession,
        event_bus: EventBus,
        unit_of_work: UnitOfWork | None = None,
        webhook_event_repository: WebhookEventRepository | None = None,
    ):
        self.__session = session
        self.__event_bus = event_bus
        self.__unit_of_work = unit_of_work or AlchemyUnitOfWork(session=self.__session)
        self.__webhook_event_repository = webhook_event_repository or PgWebhookEventRepository(session=self.__session)

    async def create(self, id: UUID, provider: str, provider_id: str, payload: dict):
        try:
            webhook_event_creator = WebhookEventCreator(
                unit_of_work=self.__unit_of_work,
                event_bus=self.__event_bus,
                webhook_event_repository=self.__webhook_event_repository,
            )

            await webhook_event_creator.create(id=id, provider=provider, provider_id=provider_id, payload=payload)
            response = {"success": True, "message": messages.SUCCESS_MESSAGE, "data": {}}, status.HTTP_201_CREATED

        except WebhookEventAlreadyExist as ex:
            response = {"success": False, "message": f"{ex}", "data": {}}, status.HTTP_409_CONFLICT
            return response

        except Exception as ex:
            response = {"success": False, "message": messages.INTERNAL_SERVER_ERROR, "data": {}}, status.HTTP_500_INTERNAL_SERVER_ERROR
            return response

        else:
            return response
