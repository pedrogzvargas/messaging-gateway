import importlib

SUBSCRIBERS_MODULES = [
    "modules.whatsapp_message.application.whatsapp_webhook_created_subscriber",
    "modules.chat.application.message_created_subscriber",
]

def load_subscribers():
    for module in SUBSCRIBERS_MODULES:
        importlib.import_module(module)
