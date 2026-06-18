from sqlalchemy_models import WhatsappMessageModel
from modules.whatsapp_message.domain import WhatsappMessage


class MessageMapper:

    @staticmethod
    def to_model(entity: WhatsappMessage) -> WhatsappMessageModel:
        return WhatsappMessageModel(
            id=entity.id,
            conversation_id=entity.conversation_id,
            role=entity.role,
            wa_message_id=entity.wa_message_id,
            from_number=entity.from_number,
            to_number=entity.to_number,
            message_type=entity.message_type,
            message_text=entity.message_text,
            direction=entity.direction,
            timestamp=entity.timestamp,
            raw_payload=entity.raw_payload,
        )

    @staticmethod
    def to_domain(model: WhatsappMessageModel) -> WhatsappMessage:
        return WhatsappMessage(
            id=model.id,
            conversation_id=model.conversation_id,
            role=model.role,
            wa_message_id=model.wa_message_id,
            from_number=model.from_number,
            to_number=model.to_number,
            message_type=model.message_type,
            message_text=model.message_text,
            direction=model.direction,
            timestamp=model.timestamp,
            raw_payload=model.raw_payload,
        )
