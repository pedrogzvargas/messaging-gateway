from uuid import UUID
from datetime import datetime
from modules.shared.aggregate_root.domain import AggregateRoot
from .whatsapp_webhook_created_domain_event import WhatsappWebhookCreatedDomainEvent


class WhatsappWebhook(AggregateRoot):

    def __init__(
        self,
        id: UUID,
        payload: dict,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ):
        super().__init__()
        self.id = id
        self.payload = payload
        self.created_at = created_at
        self.updated_at = updated_at

    @staticmethod
    def create(
        id: UUID,
        payload: dict,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ):
        whatsapp_webhook = WhatsappWebhook(
            id=id,
            payload=payload,
            created_at=created_at,
            updated_at=updated_at,
        )

        whatsapp_webhook.record(
            WhatsappWebhookCreatedDomainEvent(
                aggregate_id=id,
                payload=payload,
            )
        )

        return whatsapp_webhook
