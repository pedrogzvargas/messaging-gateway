from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from modules.app.notification_subscription.domain import NotificationSubscriptionRepository
from modules.app.notification_subscription.domain.exceptions import NotificationSubscriptionAlreadyExist
from modules.app.notification_subscription.application import NotificationSubscriptionCreator
from modules.app.notification_subscription.infrastructure import PgNotificationSubscriptionRepository
from modules.shared.persistence.domain import UnitOfWork
from modules.shared.persistence.infrastructure import AlchemyUnitOfWork
from modules.shared.http.domain import status
from modules.shared.http.domain import messages
from modules.shared.environ.domain import Environ
from modules.shared.environ.infrastructure import PyEnviron
from modules.shared.logger.domain import Logger
from modules.shared.logger.infrastructure import PyLogger


class NotificationSubscriptionCreatorController:
    """
    Class controller to create NotificationSubscription
    """

    def __init__(
        self,
        session: AsyncSession,
        unit_of_work: UnitOfWork | None = None,
        notification_subscription_repository: NotificationSubscriptionRepository | None = None,
        environ: Environ | None = None,
        logger: Logger | None = None,
    ):
        """
        Args:
            session: database session
            unit_of_work: unit of work
            notification_subscription_repository: repository for notification_subscription database table operations
            environ: environ variable reader
            logger: logger
        """

        self.__session = session
        self.__unit_of_work = unit_of_work or AlchemyUnitOfWork(session=self.__session)
        self.__notification_subscription_repository = notification_subscription_repository or PgNotificationSubscriptionRepository(session=self.__session)
        self.__environ = environ or PyEnviron()
        self.__logger = logger or PyLogger(
            level=self.__environ.get_str("LOG_LEVEL"),
            format=self.__environ.get_str("LOG_FORMAT"),
        )

    async def create(self, id: UUID, session_id: UUID, payload: dict):
        try:
            notification_subscription_creator = NotificationSubscriptionCreator(
                unit_of_work=self.__unit_of_work,
                notification_subscription_repository=self.__notification_subscription_repository,
            )

            await notification_subscription_creator.create(id=id, session_id=session_id, payload=payload)
            response = {"success": True, "message": messages.SUCCESS_MESSAGE, "data": {}}, status.HTTP_201_CREATED

        except NotificationSubscriptionAlreadyExist as ex:
            response = {"success": False, "message": f"{ex}", "data": {}}, status.HTTP_409_CONFLICT
            return response

        except Exception as ex:
            self.__logger.error(f"NotificationSubscriptionCreatorController: {ex}")
            response = {
                "success": False,
                "message": messages.INTERNAL_SERVER_ERROR,
                "data": {},
            }, status.HTTP_500_INTERNAL_SERVER_ERROR
            return response

        else:
            return response
