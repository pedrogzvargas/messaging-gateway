from dataclasses import dataclass
from modules.app.conversation.application import ConversationItem
from modules.app.message.domain import Message


@dataclass
class ConversationMessages:
    conversation: ConversationItem
    messages: list[Message]
