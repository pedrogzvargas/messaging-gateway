from modules.shared.bus.event.domain import EventBus


class FakeEventBus(EventBus):
    """
    Fake event bus creator
    """

    def __init__(self):
        self.__producer = None

    def publish(self, domain_events):
        """function to publish on Fake"""
        pass
