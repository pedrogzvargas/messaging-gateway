from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from modules.app.customer_notification.domain import CustomerNotificationRepository
from modules.app.customer_notification.application import CustomerNotificationSearcher
from modules.app.customer_notification.infrastructure import PgCustomerNotificationRepository
from modules.shared.http.domain import status
from modules.shared.http.domain import messages
from modules.shared.http.infrastructure import PageResponse
from .customer_notification_response import CustomerNotificationResponse


class CustomerNotificationSearcherController:
    """
    Class controller to search Customer Notifications
    """

    def __init__(
        self,
        session: AsyncSession,
        customer_notification_repository: CustomerNotificationRepository | None = None,
    ):
        """
        Args:
            session: database session
            customer_notification_repository: repository for customer_notification database table operations
        """

        self.__session = session
        self.__customer_notification_repository = customer_notification_repository or PgCustomerNotificationRepository(session=self.__session)

    async def search(self, query_params: dict, user_id: UUID):
        try:
            customer_notification_searcher = CustomerNotificationSearcher(
                customer_notification_repository=self.__customer_notification_repository,
            )
            customer_notifications_response = await customer_notification_searcher.search(
                query_params=query_params,
                user_id=user_id,
            )
            customer_notifications = PageResponse[CustomerNotificationResponse](
                page=customer_notifications_response.page,
                limit=customer_notifications_response.limit,
                total=customer_notifications_response.total,
                pages=customer_notifications_response.pages,
                results=[
                    CustomerNotificationResponse.model_validate(item)
                    for item in customer_notifications_response.items
                ]
            )
            response = customer_notifications, status.HTTP_200_OK

        except Exception as ex:
            response = {
                "success": False,
                "message": messages.INTERNAL_SERVER_ERROR,
                "data": {}
            }, status.HTTP_500_INTERNAL_SERVER_ERROR
            return response

        else:
            return response
