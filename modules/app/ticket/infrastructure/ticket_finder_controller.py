from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from modules.app.ticket.domain import TicketRepository
from modules.app.ticket.domain.exceptions import TicketDoesNotExist
from modules.app.ticket.application import TicketFinder
from modules.app.ticket.infrastructure import PgTicketRepository
from modules.shared.http.domain import status
from modules.shared.http.domain import messages
from .ticket_response import TicketResponse


class TicketFinderController:
    """
    Class controller to get a single Ticket owned by the current user
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

    async def find(self, ticket_id: UUID, user_id: UUID):
        try:
            ticket_finder = TicketFinder(ticket_repository=self.__ticket_repository)
            ticket = await ticket_finder.find(ticket_id=ticket_id, user_id=user_id)
            response = {
                "success": True,
                "message": messages.SUCCESS_MESSAGE,
                "data": TicketResponse.model_validate(ticket),
            }, status.HTTP_200_OK

        except TicketDoesNotExist as ex:
            response = {"success": False, "message": f"{ex}", "data": {}}, status.HTTP_404_NOT_FOUND
            return response

        except Exception as ex:
            response = {
                "success": False,
                "message": messages.INTERNAL_SERVER_ERROR,
                "data": {}
            }, status.HTTP_500_INTERNAL_SERVER_ERROR
            return response

        else:
            return response
