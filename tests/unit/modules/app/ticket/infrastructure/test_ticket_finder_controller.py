from uuid import UUID
from datetime import datetime
from datetime import timezone
import pytest
from unittest.mock import AsyncMock
from modules.app.ticket.infrastructure import TicketFinderController
from modules.app.ticket.domain import Ticket


@pytest.mark.asyncio
async def test_ticket_finder() -> None:
    ticket_id = UUID("b6a34ed1-8997-4597-b152-7ec41e9ffbd2")
    customer_id = UUID("611f6649-527b-4af1-8a1a-b66479b5eb2e")

    session = AsyncMock()
    ticket_repository = AsyncMock()
    ticket_repository.get.return_value = Ticket(
        id=ticket_id,
        customer_id=customer_id,
        details="My WhatsApp connection stopped working.",
        status="open",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    ticket_finder_controller = TicketFinderController(
        session=session,
        ticket_repository=ticket_repository,
    )

    response, code = await ticket_finder_controller.find(ticket_id=ticket_id, user_id=customer_id)

    assert response.get("success") is True
    assert code == 200
    assert response.get("data").id == ticket_id
    assert response.get("data").status == "open"


@pytest.mark.asyncio
async def test_ticket_does_not_exist_on_ticket_finder() -> None:
    ticket_id = UUID("b6a34ed1-8997-4597-b152-7ec41e9ffbd2")
    customer_id = UUID("611f6649-527b-4af1-8a1a-b66479b5eb2e")

    session = AsyncMock()
    ticket_repository = AsyncMock()
    ticket_repository.get.return_value = None

    ticket_finder_controller = TicketFinderController(
        session=session,
        ticket_repository=ticket_repository,
    )

    response, code = await ticket_finder_controller.find(ticket_id=ticket_id, user_id=customer_id)

    assert response.get("success") is False
    assert code == 404


@pytest.mark.asyncio
async def test_ticket_owned_by_another_customer_is_not_found() -> None:
    ticket_id = UUID("b6a34ed1-8997-4597-b152-7ec41e9ffbd2")
    customer_id = UUID("611f6649-527b-4af1-8a1a-b66479b5eb2e")
    other_customer_id = UUID("7e6b7f3a-0d1a-4a2a-9a7a-2f3b4c5d6e7f")

    session = AsyncMock()
    ticket_repository = AsyncMock()
    ticket_repository.get.return_value = Ticket(
        id=ticket_id,
        customer_id=other_customer_id,
        details="My WhatsApp connection stopped working.",
        status="open",
    )

    ticket_finder_controller = TicketFinderController(
        session=session,
        ticket_repository=ticket_repository,
    )

    response, code = await ticket_finder_controller.find(ticket_id=ticket_id, user_id=customer_id)

    assert response.get("success") is False
    assert code == 404
