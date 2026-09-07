from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from modules.app.notification_subscription.domain import NotificationSubscriptionRepository
from modules.app.notification_subscription.domain.exceptions import NotificationSubscriptionDoesNotExist
from modules.app.notification_subscription.application import NotificationSubscriptionFinder
from modules.app.notification_subscription.infrastructure import PgNotificationSubscriptionRepository
from modules.shared.http.domain import status
from modules.shared.http.domain import messages
from .notification_subscription_response import NotificationSubscriptionResponse


class NotificationSubscriptionFinderController:
    """
    Class controller to find the NotificationSubscription of the current session
    """

    def __init__(
        self,
        session: AsyncSession,
        notification_subscription_repository: NotificationSubscriptionRepository | None = None,
    ):
        self.__session = session
        self.__notification_subscription_repository = notification_subscription_repository or PgNotificationSubscriptionRepository(session=self.__session)

    async def find(self, session_id: UUID):
        try:
            notification_subscription_finder = NotificationSubscriptionFinder(
                notification_subscription_repository=self.__notification_subscription_repository,
            )
            notification_subscription = await notification_subscription_finder.find(session_id=session_id)

            response = {
                "success": True,
                "message": messages.SUCCESS_MESSAGE,
                "data": NotificationSubscriptionResponse.model_validate(notification_subscription),
            }, status.HTTP_200_OK

        except NotificationSubscriptionDoesNotExist as ex:
            response = {"success": False, "message": f"{ex}", "data": {}}, status.HTTP_404_NOT_FOUND
            return response

        except Exception as ex:
            response = {
                "success": False,
                "message": messages.INTERNAL_SERVER_ERROR,
                "data": {},
            }, status.HTTP_500_INTERNAL_SERVER_ERROR
            return response

        else:
            return response
