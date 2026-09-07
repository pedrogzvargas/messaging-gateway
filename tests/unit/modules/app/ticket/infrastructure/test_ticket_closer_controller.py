from uuid import UUID
from datetime import datetime
from datetime import timezone
import pytest
from unittest.mock import AsyncMock
from modules.app.ticket.infrastructure import TicketCloserController
from modules.app.ticket.domain import Ticket


@pytest.mark.asyncio
async def test_ticket_closer() -> None:
    ticket_id = UUID("b6a34ed1-8997-4597-b152-7ec41e9ffbd2")
    customer_id = UUID("611f6649-527b-4af1-8a1a-b66479b5eb2e")

    session = AsyncMock()
    unit_of_work = AsyncMock()
    ticket_repository = AsyncMock()
    ticket_repository.get.return_value = Ticket(
        id=ticket_id,
        customer_id=customer_id,
        details="My WhatsApp connection stopped working.",
        status="open",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    ticket_closer_controller = TicketCloserController(
        session=session,
        unit_of_work=unit_of_work,
        ticket_repository=ticket_repository,
    )

    response, code = await ticket_closer_controller.close(ticket_id=ticket_id, user_id=customer_id)

    assert response.get("success") is True
    assert code == 200
    assert response.get("data").status == "closed"

    patched_ticket = ticket_repository.patch.call_args.args[0]
    assert patched_ticket.status == "closed"


@pytest.mark.asyncio
async def test_ticket_does_not_exist_on_ticket_closer() -> None:
    ticket_id = UUID("b6a34ed1-8997-4597-b152-7ec41e9ffbd2")
    customer_id = UUID("611f6649-527b-4af1-8a1a-b66479b5eb2e")

    session = AsyncMock()
    unit_of_work = AsyncMock()
    ticket_repository = AsyncMock()
    ticket_repository.get.return_value = None

    ticket_closer_controller = TicketCloserController(
        session=session,
        unit_of_work=unit_of_work,
        ticket_repository=ticket_repository,
    )

    response, code = await ticket_closer_controller.close(ticket_id=ticket_id, user_id=customer_id)

    assert response.get("success") is False
    assert code == 404
    ticket_repository.patch.assert_not_awaited()


@pytest.mark.asyncio
async def test_ticket_owned_by_another_customer_cannot_be_closed() -> None:
    ticket_id = UUID("b6a34ed1-8997-4597-b152-7ec41e9ffbd2")
    customer_id = UUID("611f6649-527b-4af1-8a1a-b66479b5eb2e")
    other_customer_id = UUID("7e6b7f3a-0d1a-4a2a-9a7a-2f3b4c5d6e7f")

    session = AsyncMock()
    unit_of_work = AsyncMock()
    ticket_repository = AsyncMock()
    ticket_repository.get.return_value = Ticket(
        id=ticket_id,
        customer_id=other_customer_id,
        details="My WhatsApp connection stopped working.",
        status="open",
    )

    ticket_closer_controller = TicketCloserController(
        session=session,
        unit_of_work=unit_of_work,
        ticket_repository=ticket_repository,
    )

    response, code = await ticket_closer_controller.close(ticket_id=ticket_id, user_id=customer_id)

    assert response.get("success") is False
    assert code == 404
    ticket_repository.patch.assert_not_awaited()
