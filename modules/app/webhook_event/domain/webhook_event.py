from uuid import UUID
from datetime import datetime
from modules.shared.aggregate_root.domain import AggregateRoot
from .webhook_event_created_domain_event import WebhookEventCreatedDomainEvent


class WebhookEvent(AggregateRoot):

    def __init__(
        self,
        id: UUID,
        provider: str,
        provider_id: str,
        payload: dict,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ):
        super().__init__()
        self.id = id
        self.provider = provider
        self.provider_id = provider_id
        self.payload = payload
        self.created_at = created_at
        self.updated_at = updated_at

    @staticmethod
    def create(
        id: UUID,
        provider: str,
        provider_id: str,
        payload: dict,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ):
        webhook_event = WebhookEvent(
            id=id,
            provider=provider,
            provider_id=provider_id,
            payload=payload,
            created_at=created_at,
            updated_at=updated_at,
        )

        webhook_event.record(
            WebhookEventCreatedDomainEvent(
                aggregate_id=id,
                provider=provider,
                provider_id=provider_id,
                payload=payload,
            )
        )

        return webhook_event
