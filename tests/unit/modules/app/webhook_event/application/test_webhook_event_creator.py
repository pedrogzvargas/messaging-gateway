from uuid import UUID
import pytest
from unittest.mock import AsyncMock
from modules.app.webhook_event.application import WebhookEventCreator
from modules.app.webhook_event.domain.exceptions import WebhookEventAlreadyExist
from modules.app.webhook_event.domain import WebhookEvent

@pytest.mark.asyncio
async def test_webhook_event_creator() -> None:
    webhook_event_id = "b6a34ed1-8997-4597-b152-7ec41e9ffbd2"
    webhook_event_repository = AsyncMock()
    event_bus = AsyncMock()
    webhook_event_repository.get.return_value = None
    webhook_event_creator = WebhookEventCreator(
        unit_of_work=AsyncMock(),
        webhook_event_repository=webhook_event_repository,
        event_bus=event_bus,
    )

    await webhook_event_creator.create(
        id=UUID(webhook_event_id),
        provider="Whatsapp",
        provider_id="00000000000",
        payload={},
    )

    webhook_event_repository.add.assert_called_once()
    event_bus.publish.assert_called_once()

@pytest.mark.asyncio
async def test_id_already_exist_on_webhook_event_creator() -> None:
    webhook_event_id = "b6a34ed1-8997-4597-b152-7ec41e9ffbd2"
    webhook_event_repository = AsyncMock()
    event_bus = AsyncMock()
    result = WebhookEvent(
        id=UUID(webhook_event_id),
        provider="WhatsApp",
        provider_id="00000000000",
        payload={},
    )
    webhook_event_repository.get.return_value = result
    webhook_event_creator = WebhookEventCreator(
        unit_of_work=AsyncMock(),
        webhook_event_repository=webhook_event_repository,
        event_bus=event_bus,
    )

    with pytest.raises(WebhookEventAlreadyExist):
        await webhook_event_creator.create(
            id=UUID(webhook_event_id),
            provider="Whatsapp",
            provider_id="00000000000",
            payload={},
        )
