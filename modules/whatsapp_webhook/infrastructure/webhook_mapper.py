from sqlalchemy_models import WhatsappWebhookModel
from modules.whatsapp_webhook.domain import WhatsappWebhook


class WebhookMapper:

    @staticmethod
    def to_model(entity: WhatsappWebhook) -> WhatsappWebhookModel:
        return WhatsappWebhookModel(
            id=entity.id,
            payload=entity.payload,
        )

    @staticmethod
    def to_domain(model: WhatsappWebhookModel) -> WhatsappWebhook:
        return WhatsappWebhook(
            id=model.id,
            payload=model.payload,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
