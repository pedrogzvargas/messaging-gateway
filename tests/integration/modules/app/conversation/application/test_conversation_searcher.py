from uuid import UUID
import pytest
from modules.app.conversation.infrastructure import PgConversationRepository
from modules.app.conversation.application import ConversationSearcher
from sqlalchemy_models import ConversationModel
from sqlalchemy_models import ChannelAccountModel
from sqlalchemy_models import ChannelModel
from sqlalchemy_models import BusinessModel
from sqlalchemy_models import CustomerModel
from sqlalchemy_models import UserModel
from sqlalchemy_models import ContactModel
from tests.integration.fixtures import db_session

@pytest.mark.asyncio
async def test_no_conversations_on_conversation_searcher(db_session):
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
    db_session.add_all(
        [user, customer, contact, business, channel, channel_account]
    )
    conversation_repository = PgConversationRepository(db_session)
    conversation_searcher = ConversationSearcher(
        conversation_repository=conversation_repository
    )

    conversations_result = await conversation_searcher.search(
        query_params={},
        user_id=UUID("611f6649-527b-4af1-8a1a-b66479b5eb2e"),
    )

    assert conversations_result.limit == 10
    assert conversations_result.page == 1
    assert conversations_result.pages == 0
    assert conversations_result.total == 0
    assert len(conversations_result.items) == 0

@pytest.mark.asyncio
async def test_no_filters_on_conversation_searcher(db_session):
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
    conversation_1 = ConversationModel(
        id=UUID("41ad6238-a88f-495a-9254-cca57fbb735b"),
        channel_account_id=UUID("8815a2a7-8e23-4ff1-8174-74cc80b8d399"),
        contact_id=UUID("5f70bc98-a09e-4beb-b612-66e384094fc3"),
    )
    conversation_2 = ConversationModel(
        id=UUID("3d9400dc-206a-4301-8e19-099fc5d28b18"),
        channel_account_id=UUID("8815a2a7-8e23-4ff1-8174-74cc80b8d399"),
        contact_id=UUID("5f70bc98-a09e-4beb-b612-66e384094fc3"),
    )
    db_session.add_all(
        [user, customer, contact, business, channel, channel_account, conversation_1, conversation_2]
    )
    conversation_repository = PgConversationRepository(db_session)
    conversation_searcher = ConversationSearcher(
        conversation_repository=conversation_repository
    )

    conversations_result = await conversation_searcher.search(
        query_params={},
        user_id=UUID("611f6649-527b-4af1-8a1a-b66479b5eb2e"),
    )

    assert conversations_result.limit == 10
    assert conversations_result.page == 1
    assert conversations_result.pages == 1
    assert conversations_result.total == 2
    assert len(conversations_result.items) == 2

@pytest.mark.asyncio
async def test_filter_by_display_name_on_conversation_searcher(db_session):
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
    contact_1 = ContactModel(
        id=UUID("50823fa2-b6c5-422f-bd57-6cbe777a71a5"),
        channel_account_id=UUID("8815a2a7-8e23-4ff1-8174-74cc80b8d399"),
        provider_id="5521612310",
        display_name="Manuel Garza"
    )
    conversation_1 = ConversationModel(
        id=UUID("41ad6238-a88f-495a-9254-cca57fbb735b"),
        channel_account_id=UUID("8815a2a7-8e23-4ff1-8174-74cc80b8d399"),
        contact_id=UUID("5f70bc98-a09e-4beb-b612-66e384094fc3"),
    )
    conversation_2 = ConversationModel(
        id=UUID("3d9400dc-206a-4301-8e19-099fc5d28b18"),
        channel_account_id=UUID("8815a2a7-8e23-4ff1-8174-74cc80b8d399"),
        contact_id=UUID("50823fa2-b6c5-422f-bd57-6cbe777a71a5"),
    )
    db_session.add_all(
        [user, customer, contact, contact_1, business, channel, channel_account, conversation_1, conversation_2]
    )
    conversation_repository = PgConversationRepository(db_session)
    conversation_searcher = ConversationSearcher(
        conversation_repository=conversation_repository
    )

    conversations_result = await conversation_searcher.search(
        query_params={
            "name": "Pedro G",
        },
        user_id=UUID("611f6649-527b-4af1-8a1a-b66479b5eb2e"),
    )

    assert conversations_result.limit == 10
    assert conversations_result.page == 1
    assert conversations_result.pages == 1
    assert conversations_result.total == 1
    assert len(conversations_result.items) == 1
    assert conversations_result.items[0].display_name == "Pedro G"

@pytest.mark.asyncio
async def test_filter_by_provider_id_on_conversation_searcher(db_session):
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
    contact_1 = ContactModel(
        id=UUID("50823fa2-b6c5-422f-bd57-6cbe777a71a5"),
        channel_account_id=UUID("8815a2a7-8e23-4ff1-8174-74cc80b8d399"),
        provider_id="5521612310",
        display_name="Manuel Garza"
    )
    conversation_1 = ConversationModel(
        id=UUID("41ad6238-a88f-495a-9254-cca57fbb735b"),
        channel_account_id=UUID("8815a2a7-8e23-4ff1-8174-74cc80b8d399"),
        contact_id=UUID("5f70bc98-a09e-4beb-b612-66e384094fc3"),
    )
    conversation_2 = ConversationModel(
        id=UUID("3d9400dc-206a-4301-8e19-099fc5d28b18"),
        channel_account_id=UUID("8815a2a7-8e23-4ff1-8174-74cc80b8d399"),
        contact_id=UUID("50823fa2-b6c5-422f-bd57-6cbe777a71a5"),
    )
    db_session.add_all(
        [user, customer, contact, contact_1, business, channel, channel_account, conversation_1, conversation_2]
    )
    conversation_repository = PgConversationRepository(db_session)
    conversation_searcher = ConversationSearcher(
        conversation_repository=conversation_repository
    )

    conversations_result = await conversation_searcher.search(
        query_params={
            "provider_id": "5521612310",
        },
        user_id=UUID("611f6649-527b-4af1-8a1a-b66479b5eb2e"),
    )

    assert conversations_result.limit == 10
    assert conversations_result.page == 1
    assert conversations_result.pages == 1
    assert conversations_result.total == 1
    assert len(conversations_result.items) == 1
    assert conversations_result.items[0].display_name == "Manuel Garza"

@pytest.mark.asyncio
async def test_search_scopes_results_to_the_user_business(db_session):
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
        channel_id=UUID("1a984cab-102b-4676-9e00-971855048d4c"),
        business_id=UUID("c75e8241-2de8-462d-b673-cfd55c0edc0f"),
        provider_id="1197984816725972",
        display_name="7461084362",
    )
    other_channel_account = ChannelAccountModel(
        id=UUID("2c3d4e5f-6a7b-4c8d-9e0f-1a2b3c4d5e6f"),
        channel_id=UUID("1a984cab-102b-4676-9e00-971855048d4c"),
        business_id=UUID("9b2f4c5d-6e7f-4a8b-9c1d-2e3f4a5b6c7d"),
        provider_id="5215512345678",
        display_name="5215512345678",
    )
    contact = ContactModel(
        id=UUID("5f70bc98-a09e-4beb-b612-66e384094fc3"),
        channel_account_id=UUID("8815a2a7-8e23-4ff1-8174-74cc80b8d399"),
        provider_id="7461084362",
        display_name="Pedro G"
    )
    other_contact = ContactModel(
        id=UUID("50823fa2-b6c5-422f-bd57-6cbe777a71a5"),
        channel_account_id=UUID("2c3d4e5f-6a7b-4c8d-9e0f-1a2b3c4d5e6f"),
        provider_id="5521612310",
        display_name="Manuel Garza"
    )
    conversation = ConversationModel(
        id=UUID("41ad6238-a88f-495a-9254-cca57fbb735b"),
        channel_account_id=UUID("8815a2a7-8e23-4ff1-8174-74cc80b8d399"),
        contact_id=UUID("5f70bc98-a09e-4beb-b612-66e384094fc3"),
    )
    other_conversation = ConversationModel(
        id=UUID("3d9400dc-206a-4301-8e19-099fc5d28b18"),
        channel_account_id=UUID("2c3d4e5f-6a7b-4c8d-9e0f-1a2b3c4d5e6f"),
        contact_id=UUID("50823fa2-b6c5-422f-bd57-6cbe777a71a5"),
    )
    db_session.add_all([
        user, customer, business, other_user, other_customer, other_business,
        channel, channel_account, other_channel_account,
        contact, other_contact, conversation, other_conversation,
    ])
    conversation_repository = PgConversationRepository(db_session)
    conversation_searcher = ConversationSearcher(
        conversation_repository=conversation_repository
    )

    conversations_result = await conversation_searcher.search(
        query_params={},
        user_id=UUID("611f6649-527b-4af1-8a1a-b66479b5eb2e"),
    )

    assert conversations_result.total == 1
    assert len(conversations_result.items) == 1
    assert conversations_result.items[0].display_name == "Pedro G"

@pytest.mark.asyncio
async def test_search_returns_empty_when_user_has_no_business(db_session):
    conversation_repository = PgConversationRepository(db_session)
    conversation_searcher = ConversationSearcher(
        conversation_repository=conversation_repository
    )

    conversations_result = await conversation_searcher.search(
        query_params={},
        user_id=UUID("611f6649-527b-4af1-8a1a-b66479b5eb2e"),
    )

    assert conversations_result.total == 0
    assert conversations_result.pages == 0
    assert len(conversations_result.items) == 0
