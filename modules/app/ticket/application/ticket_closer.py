from uuid import UUID
from modules.app.ticket.domain import Ticket
from modules.app.ticket.domain import TicketRepository
from modules.app.ticket.domain.exceptions import TicketDoesNotExist
from modules.shared.persistence.domain import UnitOfWork


class TicketCloser:
    """
    Class to close a Ticket owned by the given user
    """

    def __init__(self, unit_of_work: UnitOfWork, ticket_repository: TicketRepository):
        self.__unit_of_work = unit_of_work
        self.__ticket_repository = ticket_repository

    async def close(self, ticket_id: UUID, user_id: UUID) -> Ticket:
        ticket = await self.__ticket_repository.get(ticket_id)

        if not ticket or ticket.customer_id != user_id:
            raise TicketDoesNotExist(f"Ticket with id: {ticket_id} does not exist")

        ticket.patch(data={"status": "closed"})

        async with self.__unit_of_work:
            await self.__ticket_repository.patch(ticket)

        return ticket
