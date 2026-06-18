from typing import List
from modules.shared.bus.event.domain import DomainEvent


class AggregateRoot:

    def __init__(self):
        self._domain_events = []

    def pull_domain_events(self) -> List[DomainEvent]:
        domain_events = self._domain_events
        self._domain_events = []
        return domain_events

    def record(self, domain_event: DomainEvent) -> None:
        self._domain_events.append(domain_event)
