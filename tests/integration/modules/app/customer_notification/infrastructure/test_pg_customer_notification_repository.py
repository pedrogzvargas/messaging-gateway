from uuid import UUID
import pytest
from modules.app.customer_notification.infrastructure import PgCustomerNotificationRepository
from sqlalchemy_models import CustomerModel
from sqlalchemy_models import UserModel
from sqlalchemy_models import CustomerNotificationModel
from tests.integration.fixtures import db_session


async def _seed(db_session):
    user = UserModel(
        id=UUID("611f6649-527b-4af1-8a1a-b66479b5eb2e"),
        email="demo@noemail.com",
        password="test",
        is_active=True,
    )
    customer = CustomerModel(
        id=UUID("611f6649-527b-4af1-8a1a-b66479b5eb2e"),
        user_id=UUID("611f6649-527b-4af1-8a1a-b66479b5eb2e"),
        name="Pedro",
        last_name="Gonzalez"
    )
    db_session.add_all([user, customer])

    return customer


@pytest.mark.asyncio
async def test_simple_search_filters_by_customer_id_and_status(db_session):
    customer = await _seed(db_session)
    db_session.add_all([
        CustomerNotificationModel(
            id=UUID("41ad6238-a88f-495a-9254-cca57fbb735b"),
            customer_id=customer.id,
            content="Your ticket was updated",
            status="sent",
        ),
        CustomerNotificationModel(
            id=UUID("3d9400dc-206a-4301-8e19-099fc5d28b18"),
            customer_id=customer.id,
            content="Your ticket was closed",
            status="pending",
        ),
    ])
    await db_session.flush()

    repository = PgCustomerNotificationRepository(db_session)

    all_results = await repository.simple_search(filters={"customer_id": customer.id})
    assert all_results.total == 2

    sent_results = await repository.simple_search(filters={"customer_id": customer.id, "status": "sent"})
    assert sent_results.total == 1
    assert sent_results.items[0].content == "Your ticket was updated"


@pytest.mark.asyncio
async def test_simple_search_returns_zero_for_unknown_customer(db_session):
    await _seed(db_session)
    repository = PgCustomerNotificationRepository(db_session)

    results = await repository.simple_search(filters={"customer_id": UUID("00000000-0000-0000-0000-000000000000")})

    assert results.total == 0


@pytest.mark.asyncio
async def test_simple_search_paginates_results(db_session):
    customer = await _seed(db_session)
    for index in range(3):
        db_session.add(CustomerNotificationModel(
            id=UUID(f"41ad6238-a88f-495a-9254-cca57fbb735{index}"),
            customer_id=customer.id,
            content=f"Notification {index}",
            status="sent",
        ))
    await db_session.flush()

    repository = PgCustomerNotificationRepository(db_session)

    page_one = await repository.simple_search(filters={"customer_id": customer.id}, limit=2, page=1)
    assert page_one.total == 3
    assert page_one.pages == 2
    assert len(page_one.items) == 2

    page_two = await repository.simple_search(filters={"customer_id": customer.id}, limit=2, page=2)
    assert len(page_two.items) == 1
