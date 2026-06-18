from uuid import UUID
from modules.shared.bus.event.domain import DomainEvent


class WhatsappWebhookCreatedDomainEvent(DomainEvent):

    def __init__(
        self,
        aggregate_id: UUID,
        payload: dict,
        event_id=None,
        occurred_on=None,
    ):
        super().__init__(aggregate_id=aggregate_id, event_id=event_id, occurred_on=occurred_on)
        self.__payload = payload

    def event_name(self):
        return "app.whatsapp_webhook.created"

    def to_primitives(self):
        return dict(
            payload=self.__payload,
            aggregate_id=self.aggregate_id,
            event_id=self.event_id,
            event_name=self.event_name(),
            occurred_on=self.occurred_on,
        )

    def from_primitives(self, aggregate_id, body, event_id, occurred_on):
        return WhatsappWebhookCreatedDomainEvent(
            payload=body.get("payload"),
            aggregate_id=aggregate_id,
            event_id=event_id,
            occurred_on=occurred_on,
        )

    @property
    def payload(self):
        return self.__payload
