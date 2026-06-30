from sqlalchemy_models import ConversationModel
from modules.app.conversation.domain import Conversation


class ConversationMapper:

    @staticmethod
    def to_model(entity: Conversation) -> ConversationModel:
        return ConversationModel(
            id=entity.id,
            channel_account_id=entity.channel_account_id,
            contact_id=entity.contact_id,
        )

    @staticmethod
    def to_domain(model: ConversationModel) -> Conversation:
        return Conversation(
            id=model.id,
            channel_account_id=model.channel_account_id,
            contact_id=model.contact_id,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
