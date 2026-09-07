from uuid import UUID
from datetime import datetime
from datetime import timezone
import pytest
from unittest.mock import AsyncMock
from modules.app.customer_notification.infrastructure import CustomerNotificationSearcherController
from modules.app.customer_notification.application import CustomerNotificationItem
from modules.shared.http.infrastructure import PageResult


@pytest.mark.asyncio
async def test_customer_notification_searcher() -> None:
    customer_id = UUID("611f6649-527b-4af1-8a1a-b66479b5eb2e")
    customer_notification_item = CustomerNotificationItem(
        id=UUID("b6a34ed1-8997-4597-b152-7ec41e9ffbd2"),
        customer_id=customer_id,
        content="Your ticket was updated",
        status="sent",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    session = AsyncMock()
    customer_notification_repository = AsyncMock()
    customer_notification_repository.simple_search.return_value = PageResult(
        page=1, limit=10, total=1, pages=1, items=[customer_notification_item],
    )

    customer_notification_searcher_controller = CustomerNotificationSearcherController(
        session=session,
        customer_notification_repository=customer_notification_repository,
    )

    response, code = await customer_notification_searcher_controller.search(
        query_params={}, user_id=customer_id,
    )

    assert code == 200
    assert response.total == 1
    assert response.results[0].content == "Your ticket was updated"

    filters = customer_notification_repository.simple_search.call_args.kwargs["filters"]
    assert filters["customer_id"] == customer_id
