from uuid import UUID
from modules.app.ticket.domain import TicketRepository
from modules.shared.http.infrastructure import PageResult


class TicketSearcher:
    """
    Class to search Tickets
    """

    def __init__(self, ticket_repository: TicketRepository):
        """
        Args:
            ticket_repository: repository for ticket database table operations
        """

        self.__ticket_repository = ticket_repository

    async def search(self, query_params: dict, user_id: UUID) -> PageResult:
        """
        Args:
            query_params (dict): query params.
            user_id (UUID): id of the user making the request, same as the ticket's customer_id.
        Returns:
            dict: paginated tickets.
        """

        if not isinstance(query_params, dict):
            raise ValueError(f"query_params: {query_params} is not instance of dict")

        limit = query_params.pop("limit", 10)
        page = query_params.pop("page", 1)

        cleaned_query_params = {key: value for key, value in query_params.items() if value not in [None, ""]}
        cleaned_query_params["customer_id"] = user_id

        ticket_results: PageResult = await self.__ticket_repository.simple_search(
            filters=cleaned_query_params,
            limit=limit,
            page=page,
        )

        return ticket_results
