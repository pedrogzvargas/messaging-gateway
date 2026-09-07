from uuid import UUID
from datetime import datetime
from datetime import timedelta
from datetime import timezone
import pytest
from modules.app.conversation.infrastructure import PgConversationRepository
from sqlalchemy_models import ConversationModel
from sqlalchemy_models import ChannelAccountModel
from sqlalchemy_models import ChannelModel
from sqlalchemy_models import BusinessModel
from sqlalchemy_models import CustomerModel
from sqlalchemy_models import UserModel
from sqlalchemy_models import ContactModel
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
    business = BusinessModel(
        id=UUID("c75e8241-2de8-462d-b673-cfd55c0edc0f"),
        customer_id=UUID("611f6649-527b-4af1-8a1a-b66479b5eb2e"),
        name="Vualdex",
    )
    channel = ChannelModel(
        id=UUID("1a984cab-102b-4676-9e00-971855048d4c"),
        name="WhatsApp",
        is_active=True,
    )
    channel_account = ChannelAccountModel(
        id=UUID("8815a2a7-8e23-4ff1-8174-74cc80b8d399"),
        channel_id=channel.id,
        business_id=business.id,
        provider_id="1197984816725972",
        display_name="7461084362",
    )
    contact = ContactModel(
        id=UUID("5f70bc98-a09e-4beb-b612-66e384094fc3"),
        channel_account_id=channel_account.id,
        provider_id="7461084362",
        display_name="Pedro G"
    )
    today_conversation = ConversationModel(
        id=UUID("41ad6238-a88f-495a-9254-cca57fbb735b"),
        channel_account_id=channel_account.id,
        contact_id=contact.id,
        created_at=datetime.now(timezone.utc),
    )
    old_conversation = ConversationModel(
        id=UUID("3d9400dc-206a-4301-8e19-099fc5d28b18"),
        channel_account_id=channel_account.id,
        contact_id=contact.id,
        created_at=datetime.now(timezone.utc) - timedelta(days=3),
    )
    db_session.add_all([
        user, customer, business, channel, channel_account, contact,
        today_conversation, old_conversation,
    ])

    return business


@pytest.mark.asyncio
async def test_count_by_business_id_returns_total(db_session):
    business = await _seed(db_session)
    repository = PgConversationRepository(db_session)

    total = await repository.count_by_business_id(business_id=business.id)

    assert total == 2


@pytest.mark.asyncio
async def test_count_by_business_id_filters_by_since(db_session):
    business = await _seed(db_session)
    repository = PgConversationRepository(db_session)

    today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    today_total = await repository.count_by_business_id(business_id=business.id, since=today_start)

    assert today_total == 1


@pytest.mark.asyncio
async def test_count_by_business_id_returns_zero_for_unknown_business(db_session):
    await _seed(db_session)
    repository = PgConversationRepository(db_session)

    total = await repository.count_by_business_id(business_id=UUID("00000000-0000-0000-0000-000000000000"))

    assert total == 0
