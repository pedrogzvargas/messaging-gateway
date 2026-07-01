import importlib

SUBSCRIBERS_MODULES = [
    "modules.app.message.application.webhook_event_created_subscriber",
    "modules.app.agent.application.message_created_subscriber",
]

def load_subscribers():
    for module in SUBSCRIBERS_MODULES:
        importlib.import_module(module)
