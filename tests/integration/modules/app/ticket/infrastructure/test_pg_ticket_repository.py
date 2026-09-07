from uuid import UUID
import pytest
from modules.app.ticket.infrastructure import PgTicketRepository
from modules.app.ticket.domain import Ticket
from sqlalchemy_models import CustomerModel
from sqlalchemy_models import UserModel
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
async def test_add_and_get_ticket(db_session):
    customer = await _seed(db_session)
    repository = PgTicketRepository(db_session)

    ticket = Ticket.create(
        id=UUID("41ad6238-a88f-495a-9254-cca57fbb735b"),
        customer_id=customer.id,
        details="My WhatsApp connection stopped working.",
    )
    await repository.add(ticket)

    result = await repository.get(ticket.id)

    assert result.id == ticket.id
    assert result.customer_id == customer.id
    assert result.status == "open"


@pytest.mark.asyncio
async def test_simple_search_filters_by_customer_id_and_status(db_session):
    customer = await _seed(db_session)
    repository = PgTicketRepository(db_session)

    await repository.add(Ticket.create(
        id=UUID("41ad6238-a88f-495a-9254-cca57fbb735b"),
        customer_id=customer.id,
        details="Open ticket",
        status="open",
    ))
    await repository.add(Ticket.create(
        id=UUID("3d9400dc-206a-4301-8e19-099fc5d28b18"),
        customer_id=customer.id,
        details="Closed ticket",
        status="closed",
    ))

    all_results = await repository.simple_search(filters={"customer_id": customer.id})
    assert all_results.total == 2

    open_results = await repository.simple_search(filters={"customer_id": customer.id, "status": "open"})
    assert open_results.total == 1
    assert open_results.items[0].details == "Open ticket"


@pytest.mark.asyncio
async def test_simple_search_returns_zero_for_unknown_customer(db_session):
    await _seed(db_session)
    repository = PgTicketRepository(db_session)

    results = await repository.simple_search(filters={"customer_id": UUID("00000000-0000-0000-0000-000000000000")})

    assert results.total == 0


@pytest.mark.asyncio
async def test_patch_updates_ticket_status(db_session):
    customer = await _seed(db_session)
    repository = PgTicketRepository(db_session)

    ticket = Ticket.create(
        id=UUID("41ad6238-a88f-495a-9254-cca57fbb735b"),
        customer_id=customer.id,
        details="My WhatsApp connection stopped working.",
    )
    await repository.add(ticket)

    ticket.patch(data={"status": "closed"})
    await repository.patch(ticket)

    result = await repository.get(ticket.id)
    assert result.status == "closed"
    assert result.customer_id == customer.id
