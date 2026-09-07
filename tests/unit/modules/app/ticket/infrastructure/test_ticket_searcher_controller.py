from uuid import UUID
from datetime import datetime
from datetime import timezone
import pytest
from unittest.mock import AsyncMock
from modules.app.ticket.infrastructure import TicketSearcherController
from modules.app.ticket.application import TicketItem
from modules.shared.http.infrastructure import PageResult


@pytest.mark.asyncio
async def test_ticket_searcher() -> None:
    customer_id = UUID("611f6649-527b-4af1-8a1a-b66479b5eb2e")
    ticket_item = TicketItem(
        id=UUID("b6a34ed1-8997-4597-b152-7ec41e9ffbd2"),
        customer_id=customer_id,
        details="My WhatsApp connection stopped working.",
        status="open",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    session = AsyncMock()
    ticket_repository = AsyncMock()
    ticket_repository.simple_search.return_value = PageResult(
        page=1, limit=10, total=1, pages=1, items=[ticket_item],
    )

    ticket_searcher_controller = TicketSearcherController(
        session=session,
        ticket_repository=ticket_repository,
    )

    response, code = await ticket_searcher_controller.search(
        query_params={}, user_id=customer_id,
    )

    assert code == 200
    assert response.total == 1
    assert response.results[0].details == "My WhatsApp connection stopped working."

    filters = ticket_repository.simple_search.call_args.kwargs["filters"]
    assert filters["customer_id"] == customer_id
