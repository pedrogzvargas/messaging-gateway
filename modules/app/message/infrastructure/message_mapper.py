from sqlalchemy_models import MessageModel
from modules.app.message.domain import Message


class MessageMapper:

    @staticmethod
    def to_model(entity: Message) -> MessageModel:
        return MessageModel(
            id=entity.id,
            conversation_id=entity.conversation_id,
            role=entity.role,
            message_id=entity.message_id,
            message_type=entity.message_type,
            message=entity.message,
            direction=entity.direction,
            timestamp=entity.timestamp,
            payload=entity.payload,
        )

    @staticmethod
    def to_domain(model: MessageModel) -> Message:
        return Message(
            id=model.id,
            conversation_id=model.conversation_id,
            role=model.role,
            message_id=model.message_id,
            message_type=model.message_type,
            message=model.message,
            direction=model.direction,
            timestamp=model.timestamp,
            payload=model.payload,
        )
