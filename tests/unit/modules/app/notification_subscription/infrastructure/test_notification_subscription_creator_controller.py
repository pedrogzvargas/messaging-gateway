from uuid import UUID
import pytest
from unittest.mock import AsyncMock
from modules.app.notification_subscription.infrastructure import NotificationSubscriptionCreatorController
from modules.app.notification_subscription.domain import NotificationSubscription


@pytest.mark.asyncio
async def test_notification_subscription_creator() -> None:
    notification_subscription_id = "b6a34ed1-8997-4597-b152-7ec41e9ffbd2"
    session_id = "611f6649-527b-4af1-8a1a-b66479b5eb2e"

    session = AsyncMock()
    unit_of_work = AsyncMock()
    notification_subscription_repository = AsyncMock()
    notification_subscription_repository.get.return_value = None

    notification_subscription_creator_controller = NotificationSubscriptionCreatorController(
        session=session,
        unit_of_work=unit_of_work,
        notification_subscription_repository=notification_subscription_repository,
    )

    response, code = await notification_subscription_creator_controller.create(
        id=UUID(notification_subscription_id),
        session_id=UUID(session_id),
        payload={"topic": "orders"},
    )

    assert response.get("success") is True
    assert code == 201

    added_notification_subscription = notification_subscription_repository.add.call_args.args[0]
    assert added_notification_subscription.session_id == UUID(session_id)
    assert added_notification_subscription.payload == {"topic": "orders"}
    assert added_notification_subscription.enabled is True


@pytest.mark.asyncio
async def test_id_already_exist_on_notification_subscription_creator() -> None:
    notification_subscription_id = "b6a34ed1-8997-4597-b152-7ec41e9ffbd2"
    session_id = "611f6649-527b-4af1-8a1a-b66479b5eb2e"

    session = AsyncMock()
    unit_of_work = AsyncMock()
    notification_subscription_repository = AsyncMock()
    notification_subscription_repository.get.return_value = NotificationSubscription(
        id=UUID(notification_subscription_id),
        session_id=UUID(session_id),
        payload={"topic": "orders"},
        enabled=True,
    )

    notification_subscription_creator_controller = NotificationSubscriptionCreatorController(
        session=session,
        unit_of_work=unit_of_work,
        notification_subscription_repository=notification_subscription_repository,
    )

    response, code = await notification_subscription_creator_controller.create(
        id=UUID(notification_subscription_id),
        session_id=UUID(session_id),
        payload={"topic": "orders"},
    )

    assert response.get("success") is False
    assert code == 409
