from uuid import UUID
from datetime import datetime
from datetime import timezone
from datetime import timedelta
import pytest
from modules.app.notification_subscription.infrastructure import PgNotificationSubscriptionRepository
from modules.app.notification_subscription.domain import NotificationSubscription
from sqlalchemy_models import UserModel
from sqlalchemy_models import SessionModel
from tests.integration.fixtures import db_session


async def _seed(db_session):
    user = UserModel(
        id=UUID("611f6649-527b-4af1-8a1a-b66479b5eb2e"),
        email="demo@noemail.com",
        password="test",
        is_active=True,
    )
    session = SessionModel(
        id=UUID("611f6649-527b-4af1-8a1a-b66479b5eb2e"),
        user_id=user.id,
        revoked=False,
        expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
    )
    db_session.add_all([user, session])

    return session


@pytest.mark.asyncio
async def test_add_and_get_notification_subscription(db_session):
    session = await _seed(db_session)
    repository = PgNotificationSubscriptionRepository(db_session)

    notification_subscription = NotificationSubscription.create(
        id=UUID("41ad6238-a88f-495a-9254-cca57fbb735b"),
        session_id=session.id,
        payload={"topic": "orders"},
    )
    await repository.add(notification_subscription)

    result = await repository.get(notification_subscription.id)

    assert result.id == notification_subscription.id
    assert result.session_id == session.id
    assert result.payload == {"topic": "orders"}
    assert result.enabled is True


@pytest.mark.asyncio
async def test_get_returns_none_for_unknown_id(db_session):
    repository = PgNotificationSubscriptionRepository(db_session)

    result = await repository.get(UUID("00000000-0000-0000-0000-000000000000"))

    assert result is None


@pytest.mark.asyncio
async def test_get_by_session_id(db_session):
    session = await _seed(db_session)
    repository = PgNotificationSubscriptionRepository(db_session)

    notification_subscription = NotificationSubscription.create(
        id=UUID("41ad6238-a88f-495a-9254-cca57fbb735b"),
        session_id=session.id,
        payload={"topic": "orders"},
    )
    await repository.add(notification_subscription)

    result = await repository.get_by_session_id(session.id)

    assert result.id == notification_subscription.id
    assert result.session_id == session.id
    assert result.payload == {"topic": "orders"}


@pytest.mark.asyncio
async def test_get_by_session_id_returns_none_for_unknown_session(db_session):
    repository = PgNotificationSubscriptionRepository(db_session)

    result = await repository.get_by_session_id(UUID("00000000-0000-0000-0000-000000000000"))

    assert result is None


@pytest.mark.asyncio
async def test_patch_notification_subscription(db_session):
    session = await _seed(db_session)
    repository = PgNotificationSubscriptionRepository(db_session)

    notification_subscription = NotificationSubscription.create(
        id=UUID("41ad6238-a88f-495a-9254-cca57fbb735b"),
        session_id=session.id,
        payload={"topic": "orders"},
    )
    await repository.add(notification_subscription)

    notification_subscription.patch(data={"enabled": False})
    await repository.patch(notification_subscription)

    result = await repository.get(notification_subscription.id)

    assert result.enabled is False
