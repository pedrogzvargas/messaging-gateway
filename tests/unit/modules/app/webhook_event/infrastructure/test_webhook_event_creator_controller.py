from uuid import UUID
import pytest
from unittest.mock import AsyncMock
from modules.app.webhook_event.infrastructure import WebhookEventCreatorController
from modules.app.webhook_event.domain import WebhookEvent


@pytest.mark.asyncio
async def test_webhook_event_creator() -> None:
    webhook_event_id = "b6a34ed1-8997-4597-b152-7ec41e9ffbd2"
    session = AsyncMock()
    event_bus = AsyncMock()
    unit_of_work = AsyncMock()
    webhook_event_repository = AsyncMock()
    webhook_event_repository.get.return_value = None
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
    webhook_event_creator_controller = WebhookEventCreatorController(
        session=session,
        event_bus=event_bus,
        unit_of_work=unit_of_work,
        webhook_event_repository=webhook_event_repository,
    )

    response, code = await webhook_event_creator_controller.create(
        id=UUID(webhook_event_id),
        provider="WhatsApp",
        provider_id="00000000000",
        payload=payload
    )
    assert response.get('success') is True
    assert code == 201

@pytest.mark.asyncio
async def test_id_already_exist_on_webhook_event_creator() -> None:
    webhook_event_id = "b6a34ed1-8997-4597-b152-7ec41e9ffbd2"
    session = AsyncMock()
    event_bus = AsyncMock()
    unit_of_work = AsyncMock()
    webhook_event_repository = AsyncMock()
    result = WebhookEvent(
        id=UUID(webhook_event_id),
        provider="WhatsApp",
        provider_id="00000000000",
        payload={},
    )
    webhook_event_repository.get.return_value = result
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
    webhook_event_creator_controller = WebhookEventCreatorController(
        session=session,
        event_bus=event_bus,
        unit_of_work=unit_of_work,
        webhook_event_repository=webhook_event_repository,
    )

    response, code = await webhook_event_creator_controller.create(
        id=UUID(webhook_event_id),
        provider="WhatsApp",
        provider_id="00000000000",
        payload=payload,
    )
    assert response.get('success') is False
    assert code == 409
