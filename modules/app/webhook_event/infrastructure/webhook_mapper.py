from sqlalchemy_models import WebhookEventModel
from modules.app.webhook_event.domain import WebhookEvent


class WebhookMapper:

    @staticmethod
    def to_model(entity: WebhookEvent) -> WebhookEventModel:
        return WebhookEventModel(
            id=entity.id,
            provider=entity.provider,
            provider_id=entity.provider_id,
            payload=entity.payload,
        )

    @staticmethod
    def to_domain(model: WebhookEventModel) -> WebhookEvent:
        return WebhookEvent(
            id=model.id,
            provider=model.provider,
            provider_id=model.provider_id,
            payload=model.payload,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
