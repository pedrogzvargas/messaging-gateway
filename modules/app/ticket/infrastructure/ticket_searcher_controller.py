from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from modules.app.ticket.domain import TicketRepository
from modules.app.ticket.application import TicketSearcher
from modules.app.ticket.infrastructure import PgTicketRepository
from modules.shared.http.domain import status
from modules.shared.http.domain import messages
from modules.shared.http.infrastructure import PageResponse
from .ticket_response import TicketResponse


class TicketSearcherController:
    """
    Class controller to search Tickets
    """

    def __init__(
        self,
        session: AsyncSession,
        ticket_repository: TicketRepository | None = None,
    ):
        """
        Args:
            session: database session
            ticket_repository: repository for ticket database table operations
        """

        self.__session = session
        self.__ticket_repository = ticket_repository or PgTicketRepository(session=self.__session)

    async def search(self, query_params: dict, user_id: UUID):
        try:
            ticket_searcher = TicketSearcher(ticket_repository=self.__ticket_repository)
            tickets_response = await ticket_searcher.search(query_params=query_params, user_id=user_id)
            tickets = PageResponse[TicketResponse](
                page=tickets_response.page,
                limit=tickets_response.limit,
                total=tickets_response.total,
                pages=tickets_response.pages,
                results=[
                    TicketResponse.model_validate(item)
                    for item in tickets_response.items
                ]
            )
            response = tickets, status.HTTP_200_OK

        except Exception as ex:
            response = {
                "success": False,
                "message": messages.INTERNAL_SERVER_ERROR,
                "data": {}
            }, status.HTTP_500_INTERNAL_SERVER_ERROR
            return response

        else:
            return response
