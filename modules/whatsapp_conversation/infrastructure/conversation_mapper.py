from sqlalchemy_models import WhatsappConversationModel
from modules.whatsapp_conversation.domain import WhatsappConversation


class ConversationMapper:

    @staticmethod
    def to_model(entity: WhatsappConversation) -> WhatsappConversationModel:
        return WhatsappConversationModel(
            id=entity.id,
            phone_number=entity.phone_number,
        )

    @staticmethod
    def to_domain(model: WhatsappConversationModel) -> WhatsappConversation:
        return WhatsappConversation(
            id=model.id,
            phone_number=model.phone_number,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
