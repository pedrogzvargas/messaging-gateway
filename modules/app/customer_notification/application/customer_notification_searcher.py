from uuid import UUID
from modules.app.customer_notification.domain import CustomerNotificationRepository
from modules.shared.http.infrastructure import PageResult


class CustomerNotificationSearcher:
    """
    Class to search Customer Notifications
    """

    def __init__(self, customer_notification_repository: CustomerNotificationRepository):
        """
        Args:
            customer_notification_repository: repository for customer_notification database table operations
        """

        self.__customer_notification_repository = customer_notification_repository

    async def search(self, query_params: dict, user_id: UUID) -> PageResult:
        """
        Args:
            query_params (dict): query params.
            user_id (UUID): id of the user making the request, same as the customer_notification's customer_id.
        Returns:
            dict: paginated customer notifications.
        """

        if not isinstance(query_params, dict):
            raise ValueError(f"query_params: {query_params} is not instance of dict")

        limit = query_params.pop("limit", 10)
        page = query_params.pop("page", 1)

        cleaned_query_params = {key: value for key, value in query_params.items() if value not in [None, ""]}
        cleaned_query_params["customer_id"] = user_id

        customer_notification_results: PageResult = await self.__customer_notification_repository.simple_search(
            filters=cleaned_query_params,
            limit=limit,
            page=page,
        )

        return customer_notification_results
