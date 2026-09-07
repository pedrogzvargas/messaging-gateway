from uuid import UUID
from datetime import datetime
import pytest
from modules.app.conversation.infrastructure import PgConversationRepository
from modules.app.conversation.domain.exceptions import ConversationDoesNotExist
from modules.app.message.infrastructure import PgMessageRepository
from modules.app.message.application import ConversationMessageFinder
from sqlalchemy_models import MessageModel
from sqlalchemy_models import ConversationModel
from sqlalchemy_models import ChannelAccountModel
from sqlalchemy_models import ChannelModel
from sqlalchemy_models import BusinessModel
from sqlalchemy_models import CustomerModel
from sqlalchemy_models import UserModel
from sqlalchemy_models import ContactModel
from tests.integration.fixtures import db_session


async def _seed_conversation(db_session):
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
        channel_id=UUID("1a984cab-102b-4676-9e00-971855048d4c"),
        business_id=UUID("c75e8241-2de8-462d-b673-cfd55c0edc0f"),
        provider_id="1197984816725972",
        display_name="7461084362",
    )
    contact = ContactModel(
        id=UUID("5f70bc98-a09e-4beb-b612-66e384094fc3"),
        channel_account_id=UUID("8815a2a7-8e23-4ff1-8174-74cc80b8d399"),
        provider_id="7461084362",
        display_name="Pedro G"
    )
    conversation = ConversationModel(
        id=UUID("41ad6238-a88f-495a-9254-cca57fbb735b"),
        channel_account_id=UUID("8815a2a7-8e23-4ff1-8174-74cc80b8d399"),
        contact_id=UUID("5f70bc98-a09e-4beb-b612-66e384094fc3"),
    )
    db_session.add_all(
        [user, customer, contact, business, channel, channel_account, conversation]
    )

    return conversation


def _build_finder(db_session):
    return ConversationMessageFinder(
        conversation_repository=PgConversationRepository(db_session),
        message_repository=PgMessageRepository(db_session),
    )


@pytest.mark.asyncio
async def test_find_conversation_with_messages(db_session):
    conversation = await _seed_conversation(db_session)
    message = MessageModel(
        id=UUID("2f2c9b8e-5c8c-4f2a-9a1e-9a6f4a7f1b2d"),
        conversation_id=conversation.id,
        role="user",
        message_id="wamid.123",
        message_type="text",
        message="Hola",
        direction="inbound",
        timestamp=datetime(2026, 7, 13, 12, 0, 0),
        payload={"foo": "bar"},
    )
    db_session.add(message)

    conversation_message_finder = _build_finder(db_session)
    result = await conversation_message_finder.find(conversation_id=conversation.id)

    assert result.conversation.id == conversation.id
    assert result.conversation.display_name == "Pedro G"
    assert len(result.messages) == 1
    assert result.messages[0].message == "Hola"


@pytest.mark.asyncio
async def test_find_raises_when_conversation_does_not_exist(db_session):
    conversation_message_finder = _build_finder(db_session)

    with pytest.raises(ConversationDoesNotExist):
        await conversation_message_finder.find(conversation_id=UUID("41ad6238-a88f-495a-9254-cca57fbb735b"))
