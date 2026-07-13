from uuid import UUID
import pytest
from unittest.mock import AsyncMock
from unittest.mock import Mock
from modules.app.agent.application.message_created_subscriber import MessageCreatedSubscriber
from modules.app.conversation.domain import Conversation
from modules.app.conversation.domain.exceptions import ConversationDoesNotExist
from modules.app.contact.domain.exceptions import ContactDoesNotExist
from modules.app.contact.domain import Contact


@pytest.mark.asyncio
async def test_message_created_subscriber() -> None:
    session = AsyncMock()
    unit_of_work = AsyncMock()
    llm = AsyncMock()
    conversation_repository = AsyncMock()
    contact_repository = AsyncMock()
    message_repository = AsyncMock()
    faq_repository = AsyncMock()
    message_channel = AsyncMock()
    environ = Mock()

    conversation_repository.get.return_value = Conversation(
        id=UUID("634692e0-7b15-40ed-a671-bbe6a445e7b8"),
        channel_account_id=UUID("538d5a67-3f32-4ad9-a867-68dd6dcd4cc1"),
        contact_id=UUID("901e00a4-d44f-4028-8f9c-1dba964a0460"),
    )

    contact_repository.get.return_value = Contact(
        id=UUID("901e00a4-d44f-4028-8f9c-1dba964a0460"),
        channel_account_id=UUID("b36f19f8-4da4-40d4-a1d1-b8a5c5a92fc0"),
        provider_id="5217461084362",
        display_name="Pedro G"
    )

    message_channel.send_message.return_value = {
      "messaging_product": "whatsapp",
      "contacts": [
        {
          "input": "+16505551234",
          "wa_id": "16505551234"
        }
      ],
      "messages": [
        {
          "id": "wamid.HBgLMTY0NjcwNDM1OTUVAgARGBI1RjQyNUE3NEYxMzAzMzQ5MkEA"
        }
      ]
    }

    message_created_subscriber = MessageCreatedSubscriber(
        session=session,
        unit_of_work=unit_of_work,
        environ=environ,
        llm=llm,
        conversation_repository=conversation_repository,
        contact_repository=contact_repository,
        message_repository=message_repository,
        faq_repository=faq_repository,
        message_channel=message_channel,
    )

    llm.invoke.return_value = "greeting"

    event = {
        "conversation_id": "7dc53878-ee36-4c63-aad9-6ef321639cea",
        "role": "user",
        "message_id": "wamid.HBgNNTIxNzQ2MTA4NDM2MhUCABIYFDNBRjY5RTM4NTFCMjQ3MjdGQjUzAA==",
        "message_type": "text",
        "message": "Hola",
        "direction": "inbound",
        "timestamp": "1781143098",
        "payload": {}
    }

    await message_created_subscriber.handle(
        event=event
    )

    message_repository.add.assert_called_once()
    session.close.assert_called_once()

@pytest.mark.asyncio
async def test_conversation_does_not_exist_on_message_created_subscriber() -> None:
    session = AsyncMock()
    unit_of_work = AsyncMock()
    llm = AsyncMock()
    conversation_repository = AsyncMock()
    contact_repository = AsyncMock()
    message_repository = AsyncMock()
    faq_repository = AsyncMock()
    message_channel = AsyncMock()
    environ = Mock()

    conversation_repository.get.return_value = None

    contact_repository.get.return_value = Contact(
        id=UUID("901e00a4-d44f-4028-8f9c-1dba964a0460"),
        channel_account_id=UUID("b36f19f8-4da4-40d4-a1d1-b8a5c5a92fc0"),
        provider_id="5217461084362",
        display_name="Pedro G"
    )

    message_created_subscriber = MessageCreatedSubscriber(
        session=session,
        unit_of_work=unit_of_work,
        environ=environ,
        llm=llm,
        conversation_repository=conversation_repository,
        contact_repository=contact_repository,
        message_repository=message_repository,
        faq_repository=faq_repository,
        message_channel=message_channel,
    )

    llm.invoke.return_value = "greeting"

    event = {
        "conversation_id": "7dc53878-ee36-4c63-aad9-6ef321639cea",
        "role": "user",
        "message_id": "wamid.HBgNNTIxNzQ2MTA4NDM2MhUCABIYFDNBRjY5RTM4NTFCMjQ3MjdGQjUzAA==",
        "message_type": "text",
        "message": "Hola",
        "direction": "inbound",
        "timestamp": "1781143098",
        "payload": {}
    }

    with pytest.raises(ConversationDoesNotExist):
        await message_created_subscriber.handle(
            event=event
        )

@pytest.mark.asyncio
async def test_contact_does_not_exist_on_message_created_subscriber() -> None:
    session = AsyncMock()
    unit_of_work = AsyncMock()
    llm = AsyncMock()
    conversation_repository = AsyncMock()
    contact_repository = AsyncMock()
    message_repository = AsyncMock()
    faq_repository = AsyncMock()
    message_channel = AsyncMock()
    environ = Mock()

    conversation_repository.get.return_value = Conversation(
        id=UUID("634692e0-7b15-40ed-a671-bbe6a445e7b8"),
        channel_account_id=UUID("538d5a67-3f32-4ad9-a867-68dd6dcd4cc1"),
        contact_id=UUID("901e00a4-d44f-4028-8f9c-1dba964a0460"),
    )

    contact_repository.get.return_value = None

    message_created_subscriber = MessageCreatedSubscriber(
        session=session,
        unit_of_work=unit_of_work,
        environ=environ,
        llm=llm,
        conversation_repository=conversation_repository,
        contact_repository=contact_repository,
        message_repository=message_repository,
        faq_repository=faq_repository,
        message_channel=message_channel,
    )

    llm.invoke.return_value = "greeting"

    event = {
        "conversation_id": "7dc53878-ee36-4c63-aad9-6ef321639cea",
        "role": "user",
        "message_id": "wamid.HBgNNTIxNzQ2MTA4NDM2MhUCABIYFDNBRjY5RTM4NTFCMjQ3MjdGQjUzAA==",
        "message_type": "text",
        "message": "Hola",
        "direction": "inbound",
        "timestamp": "1781143098",
        "payload": {}
    }

    with pytest.raises(ContactDoesNotExist):
        await message_created_subscriber.handle(
            event=event
        )
