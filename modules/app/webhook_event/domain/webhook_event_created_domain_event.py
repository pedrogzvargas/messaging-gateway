from uuid import UUID
from modules.shared.bus.event.domain import DomainEvent


class WebhookEventCreatedDomainEvent(DomainEvent):

    def __init__(
        self,
        aggregate_id: UUID,
        provider: str,
        provider_id: str,
        payload: dict,
        event_id=None,
        occurred_on=None,
    ):
        super().__init__(aggregate_id=aggregate_id, event_id=event_id, occurred_on=occurred_on)
        self.__provider = provider
        self.__provider_id = provider_id
        self.__payload = payload

    def event_name(self):
        return "app.webhook_event.created"

    def to_primitives(self):
        return dict(
            provider=self.__provider,
            provider_id=self.__provider_id,
            payload=self.__payload,
            aggregate_id=self.aggregate_id,
            event_id=self.event_id,
            event_name=self.event_name(),
            occurred_on=self.occurred_on,
        )

    def from_primitives(self, aggregate_id, body, event_id, occurred_on):
        return WebhookEventCreatedDomainEvent(
            provider=body.get("provider"),
            provider_id=body.get("provider_id"),
            payload=body.get("payload"),
            aggregate_id=aggregate_id,
            event_id=event_id,
            occurred_on=occurred_on,
        )

    @property
    def provider(self):
        return self.__provider

    @property
    def provider_id(self):
        return self.__provider_id

    @property
    def payload(self):
        return self.__payload
