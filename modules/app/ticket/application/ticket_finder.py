from uuid import UUID
from modules.app.ticket.domain import TicketRepository
from modules.app.ticket.domain.exceptions import TicketDoesNotExist


class TicketFinder:
    """
    Class to get a single Ticket owned by the given user
    """

    def __init__(self, ticket_repository: TicketRepository):
        """
        Args:
            ticket_repository: repository for ticket database table operations
        """

        self.__ticket_repository = ticket_repository

    async def find(self, ticket_id: UUID, user_id: UUID):
        ticket = await self.__ticket_repository.get(ticket_id)

        if not ticket or ticket.customer_id != user_id:
            raise TicketDoesNotExist(f"Ticket with id: {ticket_id} does not exist")

        return ticket
