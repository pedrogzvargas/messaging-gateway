from .registry import CLASS_SUBSCRIBERS


def subscriber(event_name):
    """
    Args:
        event_name (str): Event name.
    """

    def wrapper(cls):
        CLASS_SUBSCRIBERS[event_name].append(cls)
        return cls

    return wrapper
