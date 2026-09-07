from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from openai import AsyncOpenAI
from modules.shared.persistence.domain import UnitOfWork
from modules.shared.bus.event.domain import EventBus
from modules.app.faq.domain import FaqRepository
from modules.app.business.domain import BusinessRepository
from modules.app.faq.domain.exceptions import FaqAlreadyExist
from modules.app.business.domain.exceptions import BusinessDoesNotExist
from modules.shared.http.domain import status
from modules.shared.http.domain import messages
from modules.shared.environ.domain import Environ
from modules.shared.environ.infrastructure import PyEnviron
from modules.shared.logger.domain import Logger
from modules.shared.logger.infrastructure import PyLogger
from modules.app.faq.application import FaqCreator
from modules.app.faq.infrastructure import PgFaqRepository
from modules.app.business.infrastructure import PgBusinessRepository
from modules.shared.persistence.infrastructure import AlchemyUnitOfWork


class FaqCreatorController:

    def __init__(
        self,
        session: AsyncSession,
        event_bus: EventBus,
        unit_of_work: UnitOfWork | None = None,
        faq_repository: FaqRepository | None = None,
        business_repository: BusinessRepository | None = None,
        open_ai: AsyncOpenAI | None = None,
        environ: Environ | None = None,
        logger: Logger | None = None,
    ):
        self.__session = session
        self.__event_bus = event_bus
        self.__unit_of_work = unit_of_work or AlchemyUnitOfWork(session=self.__session)
        self.__faq_repository = faq_repository or PgFaqRepository(session=self.__session)
        self.__business_repository = business_repository or PgBusinessRepository(session=self.__session)
        self.__environ = environ or PyEnviron()
        self.__open_ai = open_ai or AsyncOpenAI(api_key=self.__environ.get_str("OPENAI_API_KEY"))
        self.__logger = logger or PyLogger(
            level=self.__environ.get_str("LOG_LEVEL"),
            format=self.__environ.get_str("LOG_FORMAT"),
        )

    async def create(self, id: UUID, customer_id: UUID, question: str, answer: str, is_active: bool):
        try:
            faq_creator = FaqCreator(
                unit_of_work=self.__unit_of_work,
                event_bus=self.__event_bus,
                business_repository=self.__business_repository,
                faq_repository=self.__faq_repository,
                open_ai=self.__open_ai,
            )

            await faq_creator.create(
                id=id,
                customer_id=customer_id,
                question=question,
                answer=answer,
                is_active=is_active,
            )
            response = {"success": True, "message": messages.SUCCESS_MESSAGE, "data": {}}, status.HTTP_201_CREATED

        except FaqAlreadyExist as ex:
            response = {"success": False, "message": f"{ex}", "data": {}}, status.HTTP_409_CONFLICT
            return response

        except BusinessDoesNotExist as ex:
            response = {"success": False, "message": f"{ex}", "data": {}}, status.HTTP_404_NOT_FOUND
            return response

        except Exception as ex:
            self.__logger.error(f"FaqCreatorController: {ex}")
            response = {"success": False, "message": messages.INTERNAL_SERVER_ERROR, "data": {}}, status.HTTP_500_INTERNAL_SERVER_ERROR
            return response

        else:
            return response
