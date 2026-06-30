from uuid import UUID
import pytest
from unittest.mock import AsyncMock
from unittest.mock import Mock
from modules.app.channel_account.domain import ChannelAccount
from modules.app.contact.domain import Contact
from modules.app.conversation.domain import Conversation
from modules.app.message.application.webhook_event_created_subscriber import WebhookEventCreatedSubscriber

@pytest.mark.asyncio
async def test_no_channel_account_on_webhook_event_created_subscriber() -> None:
    session = AsyncMock()
    event_bus = AsyncMock()
    unit_of_work = AsyncMock()
    environ = Mock()
    channel_account_repository = AsyncMock()
    contact_repository = AsyncMock()
    conversation_repository = AsyncMock()
    message_repository = AsyncMock()

    channel_account_repository.get_by_provider_id.return_value = None

    webhook_event_created_subscriber = WebhookEventCreatedSubscriber(
        session=session,
        event_bus=event_bus,
        environ=environ,
        unit_of_work=unit_of_work,
        conversation_repository=conversation_repository,
        channel_account_repository=channel_account_repository,
        contact_repository=contact_repository,
        message_repository=message_repository,
    )

    payload = {
        'object': 'whatsapp_business_account',
        'entry': [
            {
                'id': '1000052619380967',
                'changes': [
                    {
                        'value': {
                            'messaging_product': 'whatsapp',
                            'metadata': {
                                'display_phone_number': '5217461104241',
                                'phone_number_id': '1197984816725972'
                            },
                            'contacts': [
                                {
                                    'profile': {
                                        'name': 'Pedro G'
                                    },
                                    'wa_id': '5217461084362',
                                    'user_id': 'MX.856122934211769'
                                }
                            ],
                            'messages': [
                                {
                                    'from': '5217461084362',
                                    'from_user_id': 'MX.856122934211769',
                                    'id': 'wamid.HBgNNTIxNzQ2MTA4NDM2MhUCABIYFDNBRjY5RTM4NTFCMjQ3MjdGQjUzAA==',
                                    'timestamp': '1781143098',
                                    'text': {
                                        'body': 'Hola'
                                    },
                                    'type': 'text'
                                }
                            ]
                        },
                        'field': 'messages'
                    }
                ]
            }
        ]
    }

    await webhook_event_created_subscriber.handle(
        event={
            "payload": payload,
            "provider": "whatsapp",
            "provider_id": "1197984816725972",
        }
    )

    message_repository.add.assert_not_called()
    contact_repository.get_by_provider_id.assert_not_called()
    contact_repository.add.assert_not_called()
    conversation_repository.add.assert_not_called()
    event_bus.publish.assert_not_called()
    session.close.assert_called_once()

@pytest.mark.asyncio
async def test_first_message_on_webhook_event_created_subscriber() -> None:
    session = AsyncMock()
    event_bus = AsyncMock()
    unit_of_work = AsyncMock()
    environ = Mock()
    channel_account_repository = AsyncMock()
    contact_repository = AsyncMock()
    conversation_repository = AsyncMock()
    message_repository = AsyncMock()

    channel_account_repository.get_by_provider_id.return_value = ChannelAccount(
        id=UUID("4805ed0a-7dc6-4129-a6f7-d47de8db6b35"),
        channel_id=UUID("7f8a555f-b5be-42da-9c67-2f3157524bc7"),
        business_id=UUID("433b6dad-77dd-462b-9c00-f6c8ddd53c59"),
        provider_id="1197984816725972",
    )

    contact_repository.get_by_provider_id.return_value = None
    conversation_repository.get_by_fields.return_value = None

    webhook_event_created_subscriber = WebhookEventCreatedSubscriber(
        session=session,
        event_bus=event_bus,
        environ=environ,
        unit_of_work=unit_of_work,
        conversation_repository=conversation_repository,
        channel_account_repository=channel_account_repository,
        contact_repository=contact_repository,
        message_repository=message_repository,
    )

    payload = {
        'object': 'whatsapp_business_account',
        'entry': [
            {
                'id': '1000052619380967',
                'changes': [
                    {
                        'value': {
                            'messaging_product': 'whatsapp',
                            'metadata': {
                                'display_phone_number': '5217461104241',
                                'phone_number_id': '1197984816725972'
                            },
                            'contacts': [
                                {
                                    'profile': {
                                        'name': 'Pedro G'
                                    },
                                    'wa_id': '5217461084362',
                                    'user_id': 'MX.856122934211769'
                                }
                            ],
                            'messages': [
                                {
                                    'from': '5217461084362',
                                    'from_user_id': 'MX.856122934211769',
                                    'id': 'wamid.HBgNNTIxNzQ2MTA4NDM2MhUCABIYFDNBRjY5RTM4NTFCMjQ3MjdGQjUzAA==',
                                    'timestamp': '1781143098',
                                    'text': {
                                        'body': 'Hola'
                                    },
                                    'type': 'text'
                                }
                            ]
                        },
                        'field': 'messages'
                    }
                ]
            }
        ]
    }

    await webhook_event_created_subscriber.handle(
        event={
            "payload": payload,
            "provider": "whatsapp",
            "provider_id": "1197984816725972",
        }
    )

    contact_repository.add.assert_called_once()
    message_repository.add.assert_called_once()
    conversation_repository.add.assert_called_once()
    event_bus.publish.assert_called_once()
    session.close.assert_called_once()

@pytest.mark.asyncio
async def test_contact_already_exist_on_webhook_event_created_subscriber() -> None:
    session = AsyncMock()
    event_bus = AsyncMock()
    unit_of_work = AsyncMock()
    environ = Mock()
    channel_account_repository = AsyncMock()
    contact_repository = AsyncMock()
    conversation_repository = AsyncMock()
    message_repository = AsyncMock()

    channel_account_repository.get_by_provider_id.return_value = ChannelAccount(
        id=UUID("4805ed0a-7dc6-4129-a6f7-d47de8db6b35"),
        channel_id=UUID("7f8a555f-b5be-42da-9c67-2f3157524bc7"),
        business_id=UUID("433b6dad-77dd-462b-9c00-f6c8ddd53c59"),
        provider_id="1197984816725972",
    )

    contact_repository.get_by_provider_id.return_value = Contact(
        id=UUID("8849469f-a1fe-4bd2-b9eb-368998f5bb1f"),
        channel_id=UUID("7f8a555f-b5be-42da-9c67-2f3157524bc7"),
        provider_id="1197984816725972",
        display_name="Pedro G",
    )
    conversation_repository.get_by_fields.return_value = None

    webhook_event_created_subscriber = WebhookEventCreatedSubscriber(
        session=session,
        event_bus=event_bus,
        environ=environ,
        unit_of_work=unit_of_work,
        conversation_repository=conversation_repository,
        channel_account_repository=channel_account_repository,
        contact_repository=contact_repository,
        message_repository=message_repository,
    )

    payload = {
        'object': 'whatsapp_business_account',
        'entry': [
            {
                'id': '1000052619380967',
                'changes': [
                    {
                        'value': {
                            'messaging_product': 'whatsapp',
                            'metadata': {
                                'display_phone_number': '5217461104241',
                                'phone_number_id': '1197984816725972'
                            },
                            'contacts': [
                                {
                                    'profile': {
                                        'name': 'Pedro G'
                                    },
                                    'wa_id': '5217461084362',
                                    'user_id': 'MX.856122934211769'
                                }
                            ],
                            'messages': [
                                {
                                    'from': '5217461084362',
                                    'from_user_id': 'MX.856122934211769',
                                    'id': 'wamid.HBgNNTIxNzQ2MTA4NDM2MhUCABIYFDNBRjY5RTM4NTFCMjQ3MjdGQjUzAA==',
                                    'timestamp': '1781143098',
                                    'text': {
                                        'body': 'Hola'
                                    },
                                    'type': 'text'
                                }
                            ]
                        },
                        'field': 'messages'
                    }
                ]
            }
        ]
    }

    await webhook_event_created_subscriber.handle(
        event={
            "payload": payload,
            "provider": "whatsapp",
            "provider_id": "1197984816725972",
        }
    )

    contact_repository.add.assert_not_called()
    message_repository.add.assert_called_once()
    conversation_repository.add.assert_called_once()
    event_bus.publish.assert_called_once()
    session.close.assert_called_once()

@pytest.mark.asyncio
async def test_conversation_already_exist_on_webhook_event_created_subscriber() -> None:
    session = AsyncMock()
    event_bus = AsyncMock()
    unit_of_work = AsyncMock()
    environ = Mock()
    channel_account_repository = AsyncMock()
    contact_repository = AsyncMock()
    conversation_repository = AsyncMock()
    message_repository = AsyncMock()

    channel_account_repository.get_by_provider_id.return_value = ChannelAccount(
        id=UUID("4805ed0a-7dc6-4129-a6f7-d47de8db6b35"),
        channel_id=UUID("7f8a555f-b5be-42da-9c67-2f3157524bc7"),
        business_id=UUID("433b6dad-77dd-462b-9c00-f6c8ddd53c59"),
        provider_id="1197984816725972",
    )

    contact_repository.get_by_provider_id.return_value = Contact(
        id=UUID("8849469f-a1fe-4bd2-b9eb-368998f5bb1f"),
        channel_id=UUID("7f8a555f-b5be-42da-9c67-2f3157524bc7"),
        provider_id="1197984816725972",
        display_name="Pedro G",
    )
    conversation_repository.get_by_phone.return_value = Conversation(
        id=UUID("8e665a93-250a-451c-b158-c9e471945ae9"),
        channel_account_id=UUID("4805ed0a-7dc6-4129-a6f7-d47de8db6b35"),
        contact_id=UUID("8849469f-a1fe-4bd2-b9eb-368998f5bb1f")
    )

    webhook_event_created_subscriber = WebhookEventCreatedSubscriber(
        session=session,
        event_bus=event_bus,
        environ=environ,
        unit_of_work=unit_of_work,
        conversation_repository=conversation_repository,
        channel_account_repository=channel_account_repository,
        contact_repository=contact_repository,
        message_repository=message_repository,
    )

    payload = {
        'object': 'whatsapp_business_account',
        'entry': [
            {
                'id': '1000052619380967',
                'changes': [
                    {
                        'value': {
                            'messaging_product': 'whatsapp',
                            'metadata': {
                                'display_phone_number': '5217461104241',
                                'phone_number_id': '1197984816725972'
                            },
                            'contacts': [
                                {
                                    'profile': {
                                        'name': 'Pedro G'
                                    },
                                    'wa_id': '5217461084362',
                                    'user_id': 'MX.856122934211769'
                                }
                            ],
                            'messages': [
                                {
                                    'from': '5217461084362',
                                    'from_user_id': 'MX.856122934211769',
                                    'id': 'wamid.HBgNNTIxNzQ2MTA4NDM2MhUCABIYFDNBRjY5RTM4NTFCMjQ3MjdGQjUzAA==',
                                    'timestamp': '1781143098',
                                    'text': {
                                        'body': 'Hola'
                                    },
                                    'type': 'text'
                                }
                            ]
                        },
                        'field': 'messages'
                    }
                ]
            }
        ]
    }

    await webhook_event_created_subscriber.handle(
        event={
            "payload": payload,
            "provider": "whatsapp",
            "provider_id": "1197984816725972",
        }
    )

    contact_repository.add.assert_not_called()
    conversation_repository.add.assert_not_called()
    message_repository.add.assert_called_once()
    event_bus.publish.assert_called_once()
    session.close.assert_called_once()
