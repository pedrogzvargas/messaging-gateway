from sqlalchemy_models import NotificationSubscriptionModel
from modules.app.notification_subscription.domain import NotificationSubscription


class NotificationSubscriptionMapper:

    @staticmethod
    def to_model(entity: NotificationSubscription) -> NotificationSubscriptionModel:
        return NotificationSubscriptionModel(
            id=entity.id,
            session_id=entity.session_id,
            payload=entity.payload,
            enabled=entity.enabled,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    @staticmethod
    def to_domain(model: NotificationSubscriptionModel) -> NotificationSubscription:
        return NotificationSubscription(
            id=model.id,
            session_id=model.session_id,
            payload=model.payload,
            enabled=model.enabled,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
