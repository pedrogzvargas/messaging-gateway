from uuid import UUID
import pytest
from modules.app.contact.infrastructure import PgContactRepository
from modules.app.contact.application import ContactSearcher
from sqlalchemy_models import ContactModel
from sqlalchemy_models import ChannelAccountModel
from sqlalchemy_models import ChannelModel
from sqlalchemy_models import BusinessModel
from sqlalchemy_models import CustomerModel
from sqlalchemy_models import UserModel
from tests.integration.fixtures import db_session


async def _seed_business(db_session, user_id, business_id, business_name):
    user = UserModel(
        id=user_id,
        email=f"{user_id}@noemail.com",
        password="test",
        is_active=True,
    )
    customer = CustomerModel(
        id=user_id,
        user_id=user_id,
        name="Pedro",
        last_name="Gonzalez"
    )
    business = BusinessModel(
        id=business_id,
        customer_id=user_id,
        name=business_name,
    )
    db_session.add_all([user, customer, business])

    return business


def _build_searcher(db_session):
    return ContactSearcher(contact_repository=PgContactRepository(db_session))


@pytest.mark.asyncio
async def test_search_scopes_results_to_the_user_business(db_session):
    business_1 = await _seed_business(
        db_session,
        user_id=UUID("611f6649-527b-4af1-8a1a-b66479b5eb2e"),
        business_id=UUID("c75e8241-2de8-462d-b673-cfd55c0edc0f"),
        business_name="Vualdex",
    )
    business_2 = await _seed_business(
        db_session,
        user_id=UUID("7e6b7f3a-0d1a-4a2a-9a7a-2f3b4c5d6e7f"),
        business_id=UUID("9b2f4c5d-6e7f-4a8b-9c1d-2e3f4a5b6c7d"),
        business_name="Other Business",
    )
    channel = ChannelModel(
        id=UUID("1a984cab-102b-4676-9e00-971855048d4c"),
        name="WhatsApp",
        is_active=True,
    )
    channel_account_1 = ChannelAccountModel(
        id=UUID("8815a2a7-8e23-4ff1-8174-74cc80b8d399"),
        channel_id=channel.id,
        business_id=business_1.id,
        provider_id="1197984816725972",
        display_name="7461084362",
    )
    channel_account_2 = ChannelAccountModel(
        id=UUID("2c3d4e5f-6a7b-4c8d-9e0f-1a2b3c4d5e6f"),
        channel_id=channel.id,
        business_id=business_2.id,
        provider_id="5215512345678",
        display_name="5215512345678",
    )
    contact_1 = ContactModel(
        id=UUID("5f70bc98-a09e-4beb-b612-66e384094fc3"),
        channel_account_id=channel_account_1.id,
        provider_id="7461084362",
        display_name="Pedro G"
    )
    contact_2 = ContactModel(
        id=UUID("50823fa2-b6c5-422f-bd57-6cbe777a71a5"),
        channel_account_id=channel_account_2.id,
        provider_id="5521612310",
        display_name="Manuel Garza"
    )
    db_session.add_all([channel, channel_account_1, channel_account_2, contact_1, contact_2])

    contact_searcher = _build_searcher(db_session)
    result = await contact_searcher.search(
        query_params={},
        user_id=UUID("611f6649-527b-4af1-8a1a-b66479b5eb2e"),
    )

    assert result.total == 1
    assert len(result.items) == 1
    assert result.items[0].display_name == "Pedro G"


@pytest.mark.asyncio
async def test_search_returns_empty_when_user_has_no_business(db_session):
    contact_searcher = _build_searcher(db_session)
    result = await contact_searcher.search(
        query_params={},
        user_id=UUID("611f6649-527b-4af1-8a1a-b66479b5eb2e"),
    )

    assert result.total == 0
    assert result.pages == 0
    assert len(result.items) == 0
