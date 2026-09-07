from uuid import UUID
from datetime import datetime
from datetime import timezone
import pytest
from unittest.mock import AsyncMock
from modules.app.notification_subscription.infrastructure import NotificationSubscriptionFinderController
from modules.app.notification_subscription.domain import NotificationSubscription


@pytest.mark.asyncio
async def test_notification_subscription_finder() -> None:
    notification_subscription_id = "b6a34ed1-8997-4597-b152-7ec41e9ffbd2"
    session_id = "611f6649-527b-4af1-8a1a-b66479b5eb2e"

    notification_subscription_repository = AsyncMock()
    notification_subscription_repository.get_by_session_id.return_value = NotificationSubscription(
        id=UUID(notification_subscription_id),
        session_id=UUID(session_id),
        payload={"topic": "orders"},
        enabled=True,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    notification_subscription_finder_controller = NotificationSubscriptionFinderController(
        session=AsyncMock(),
        notification_subscription_repository=notification_subscription_repository,
    )

    response, code = await notification_subscription_finder_controller.find(session_id=UUID(session_id))

    assert response.get("success") is True
    assert code == 200
    assert response.get("data").id == UUID(notification_subscription_id)
    assert response.get("data").payload == {"topic": "orders"}


@pytest.mark.asyncio
async def test_notification_subscription_not_found_on_finder() -> None:
    session_id = "611f6649-527b-4af1-8a1a-b66479b5eb2e"

    notification_subscription_repository = AsyncMock()
    notification_subscription_repository.get_by_session_id.return_value = None

    notification_subscription_finder_controller = NotificationSubscriptionFinderController(
        session=AsyncMock(),
        notification_subscription_repository=notification_subscription_repository,
    )

    response, code = await notification_subscription_finder_controller.find(session_id=UUID(session_id))

    assert response.get("success") is False
    assert code == 404
