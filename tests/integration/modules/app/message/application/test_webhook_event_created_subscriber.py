from uuid import UUID
import pytest
from unittest.mock import AsyncMock
from unittest.mock import Mock
from modules.app.message.application.webhook_event_created_subscriber import WebhookEventCreatedSubscriber
from modules.shared.persistence.infrastructure import AlchemyUnitOfWork
from modules.app.channel_account.infrastructure import PgChannelAccountRepository
from modules.app.contact.infrastructure import PgContactRepository
from modules.app.conversation.infrastructure import PgConversationRepository
from modules.app.message.infrastructure import PgMessageRepository
from sqlalchemy_models import ChannelAccountModel, ContactModel, ConversationModel
from tests.integration.fixtures import db_session

@pytest.mark.asyncio
async def test_no_channel_account_on_webhook_event_created_subscriber(db_session) -> None:
    unit_of_work = AlchemyUnitOfWork(session=db_session)
    event_bus = AsyncMock()
    environ = Mock()
    channel_account_repository = PgChannelAccountRepository(session=db_session)
    contact_repository = PgContactRepository(session=db_session)
    conversation_repository = PgConversationRepository(session=db_session)
    message_repository = PgMessageRepository(session=db_session)

    webhook_event_created_subscriber = WebhookEventCreatedSubscriber(
        session=db_session,
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

    assert len(await message_repository.all()) == 0

@pytest.mark.asyncio
async def test_first_message_on_webhook_event_created_subscriber(db_session) -> None:
    unit_of_work = AlchemyUnitOfWork(session=db_session)
    event_bus = AsyncMock()
    environ = Mock()
    channel_account_repository = PgChannelAccountRepository(session=db_session)
    contact_repository = PgContactRepository(session=db_session)
    conversation_repository = PgConversationRepository(session=db_session)
    message_repository = PgMessageRepository(session=db_session)

    channel_account = ChannelAccountModel(
        id=UUID("4805ed0a-7dc6-4129-a6f7-d47de8db6b35"),
        channel_id=UUID("7f8a555f-b5be-42da-9c67-2f3157524bc7"),
        business_id=UUID("433b6dad-77dd-462b-9c00-f6c8ddd53c59"),
        provider_id="1197984816725972",
    )
    db_session.add(channel_account)
    await db_session.commit()

    webhook_event_created_subscriber = WebhookEventCreatedSubscriber(
        session=db_session,
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

    contact = await contact_repository.get_by_provider_id(provider_id="5217461084362")
    conversation = await conversation_repository.get_by_fields(
        channel_account_id=channel_account.id,
        contact_id=contact.id,
    )
    assert contact.display_name == "Pedro G"
    assert conversation is not None
    assert len(await message_repository.all()) == 1

@pytest.mark.asyncio
async def test_contact_already_exist_on_webhook_event_created_subscriber(db_session) -> None:
    unit_of_work = AlchemyUnitOfWork(session=db_session)
    event_bus = AsyncMock()
    environ = Mock()
    channel_account_repository = PgChannelAccountRepository(session=db_session)
    contact_repository = PgContactRepository(session=db_session)
    conversation_repository = PgConversationRepository(session=db_session)
    message_repository = PgMessageRepository(session=db_session)

    channel_account = ChannelAccountModel(
        id=UUID("4805ed0a-7dc6-4129-a6f7-d47de8db6b35"),
        channel_id=UUID("7f8a555f-b5be-42da-9c67-2f3157524bc7"),
        business_id=UUID("433b6dad-77dd-462b-9c00-f6c8ddd53c59"),
        provider_id="1197984816725972",
    )

    contact = ContactModel(
        id=UUID("8849469f-a1fe-4bd2-b9eb-368998f5bb1f"),
        channel_id=UUID("7f8a555f-b5be-42da-9c67-2f3157524bc7"),
        provider_id="5217461084362",
        display_name="Pedro G",
    )

    db_session.add_all(
        [
            channel_account,
            contact
        ]
    )
    await db_session.commit()

    webhook_event_created_subscriber = WebhookEventCreatedSubscriber(
        session=db_session,
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

    conversation = await conversation_repository.get_by_fields(
        channel_account_id=channel_account.id,
        contact_id=contact.id,
    )

    assert conversation is not None
    assert len(await message_repository.all()) == 1

@pytest.mark.asyncio
async def test_conversation_already_exist_on_webhook_event_created_subscriber(db_session) -> None:
    unit_of_work = AlchemyUnitOfWork(session=db_session)
    event_bus = AsyncMock()
    environ = Mock()
    channel_account_repository = PgChannelAccountRepository(session=db_session)
    contact_repository = PgContactRepository(session=db_session)
    conversation_repository = PgConversationRepository(session=db_session)
    message_repository = PgMessageRepository(session=db_session)

    channel_account = ChannelAccountModel(
        id=UUID("4805ed0a-7dc6-4129-a6f7-d47de8db6b35"),
        channel_id=UUID("7f8a555f-b5be-42da-9c67-2f3157524bc7"),
        business_id=UUID("433b6dad-77dd-462b-9c00-f6c8ddd53c59"),
        provider_id="1197984816725972",
    )

    contact  = ContactModel(
        id=UUID("8849469f-a1fe-4bd2-b9eb-368998f5bb1f"),
        channel_id=UUID("7f8a555f-b5be-42da-9c67-2f3157524bc7"),
        provider_id="5217461084362",
        display_name="Pedro G",
    )
    conversation = ConversationModel(
        id=UUID("8e665a93-250a-451c-b158-c9e471945ae9"),
        channel_account_id=UUID("4805ed0a-7dc6-4129-a6f7-d47de8db6b35"),
        contact_id=UUID("8849469f-a1fe-4bd2-b9eb-368998f5bb1f")
    )

    db_session.add_all(
        [
            channel_account,
            contact,
            conversation,
        ]
    )
    await db_session.commit()

    webhook_event_created_subscriber = WebhookEventCreatedSubscriber(
        session=db_session,
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

    assert len(await message_repository.all()) == 1
