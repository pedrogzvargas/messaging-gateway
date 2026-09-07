from uuid import UUID
from modules.app.ticket.domain import Ticket
from modules.app.ticket.domain import TicketRepository
from modules.app.ticket.domain.exceptions import TicketAlreadyExist
from modules.shared.persistence.domain import UnitOfWork


class TicketCreator:

    def __init__(self, unit_of_work: UnitOfWork, ticket_repository: TicketRepository):
        self.__unit_of_work = unit_of_work
        self.__ticket_repository = ticket_repository

    async def create(self, id: UUID, customer_id: UUID, details: str, status: str = "open"):

        if await self.__ticket_repository.get(id=id):
            raise TicketAlreadyExist(f"Ticket with id:{id} already exists")

        ticket = Ticket.create(
            id=id,
            customer_id=customer_id,
            details=details,
            status=status,
        )

        async with self.__unit_of_work:
            await self.__ticket_repository.add(ticket)
