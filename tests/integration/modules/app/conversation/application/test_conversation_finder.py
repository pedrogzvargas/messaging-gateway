from uuid import UUID
import pytest
from modules.app.conversation.infrastructure import PgConversationRepository
from modules.app.conversation.application import ConversationFinder
from modules.app.conversation.domain.exceptions import ConversationDoesNotExist
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
    other_user = UserModel(
        id=UUID("7e6b7f3a-0d1a-4a2a-9a7a-2f3b4c5d6e7f"),
        email="other@noemail.com",
        password="test",
        is_active=True,
    )
    other_customer = CustomerModel(
        id=UUID("7e6b7f3a-0d1a-4a2a-9a7a-2f3b4c5d6e7f"),
        user_id=UUID("7e6b7f3a-0d1a-4a2a-9a7a-2f3b4c5d6e7f"),
        name="Other",
        last_name="Owner"
    )
    other_business = BusinessModel(
        id=UUID("9b2f4c5d-6e7f-4a8b-9c1d-2e3f4a5b6c7d"),
        customer_id=UUID("7e6b7f3a-0d1a-4a2a-9a7a-2f3b4c5d6e7f"),
        name="Other Business",
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
    conversation = ConversationModel(
        id=UUID("41ad6238-a88f-495a-9254-cca57fbb735b"),
        channel_account_id=channel_account.id,
        contact_id=contact.id,
    )
    db_session.add_all([
        user, customer, business, other_user, other_customer, other_business,
        channel, channel_account, contact, conversation,
    ])

    return conversation


def _build_finder(db_session):
    return ConversationFinder(conversation_repository=PgConversationRepository(db_session))


@pytest.mark.asyncio
async def test_find_returns_conversation_owned_by_user_business(db_session):
    conversation = await _seed(db_session)
    conversation_finder = _build_finder(db_session)

    result = await conversation_finder.find(
        conversation_id=conversation.id,
        user_id=UUID("611f6649-527b-4af1-8a1a-b66479b5eb2e"),
    )

    assert result.id == conversation.id
    assert result.display_name == "Pedro G"


@pytest.mark.asyncio
async def test_find_raises_when_conversation_belongs_to_another_business(db_session):
    conversation = await _seed(db_session)
    conversation_finder = _build_finder(db_session)

    with pytest.raises(ConversationDoesNotExist):
        await conversation_finder.find(
            conversation_id=conversation.id,
            user_id=UUID("7e6b7f3a-0d1a-4a2a-9a7a-2f3b4c5d6e7f"),
        )


@pytest.mark.asyncio
async def test_find_raises_when_user_has_no_business(db_session):
    conversation = await _seed(db_session)
    conversation_finder = _build_finder(db_session)

    with pytest.raises(ConversationDoesNotExist):
        await conversation_finder.find(
            conversation_id=conversation.id,
            user_id=UUID("00000000-0000-0000-0000-000000000000"),
        )
