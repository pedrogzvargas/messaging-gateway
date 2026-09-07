from uuid import UUID
import pytest
from unittest.mock import AsyncMock
from modules.app.ticket.infrastructure import TicketCreatorController
from modules.app.ticket.domain import Ticket


@pytest.mark.asyncio
async def test_ticket_creator() -> None:
    ticket_id = "b6a34ed1-8997-4597-b152-7ec41e9ffbd2"
    customer_id = "611f6649-527b-4af1-8a1a-b66479b5eb2e"

    session = AsyncMock()
    unit_of_work = AsyncMock()
    ticket_repository = AsyncMock()
    ticket_repository.get.return_value = None

    ticket_creator_controller = TicketCreatorController(
        session=session,
        unit_of_work=unit_of_work,
        ticket_repository=ticket_repository,
    )

    response, code = await ticket_creator_controller.create(
        id=UUID(ticket_id),
        customer_id=UUID(customer_id),
        details="My WhatsApp connection stopped working.",
    )

    assert response.get("success") is True
    assert code == 201

    added_ticket = ticket_repository.add.call_args.args[0]
    assert added_ticket.customer_id == UUID(customer_id)
    assert added_ticket.details == "My WhatsApp connection stopped working."
    assert added_ticket.status == "open"


@pytest.mark.asyncio
async def test_id_already_exist_on_ticket_creator() -> None:
    ticket_id = "b6a34ed1-8997-4597-b152-7ec41e9ffbd2"
    customer_id = "611f6649-527b-4af1-8a1a-b66479b5eb2e"

    session = AsyncMock()
    unit_of_work = AsyncMock()
    ticket_repository = AsyncMock()
    ticket_repository.get.return_value = Ticket(
        id=UUID(ticket_id),
        customer_id=UUID(customer_id),
        details="My WhatsApp connection stopped working.",
        status="open",
    )

    ticket_creator_controller = TicketCreatorController(
        session=session,
        unit_of_work=unit_of_work,
        ticket_repository=ticket_repository,
    )

    response, code = await ticket_creator_controller.create(
        id=UUID(ticket_id),
        customer_id=UUID(customer_id),
        details="My WhatsApp connection stopped working.",
    )

    assert response.get("success") is False
    assert code == 409
