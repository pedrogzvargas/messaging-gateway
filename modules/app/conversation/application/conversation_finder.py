from uuid import UUID
from modules.app.conversation.domain import ConversationRepository
from modules.app.conversation.domain.exceptions import ConversationDoesNotExist


class ConversationFinder:
    """
    Class to get Conversation
    """

    def __init__(self, conversation_repository: ConversationRepository):
        """
        Args:
            conversation_repository: repository for customer database table operations
        """

        self.__conversation_repository = conversation_repository

    async def find(self, conversation_id: UUID, user_id: UUID):
        business_id = await self.__conversation_repository.get_business_id_by_user_id(user_id)
        if not business_id:
            raise ConversationDoesNotExist(f"Conversation with id: {conversation_id} does not exist")

        conversation = await self.__conversation_repository.get_detail(conversation_id, business_id=business_id)
        if not conversation:
            raise ConversationDoesNotExist(f"Conversation with id: {conversation_id} does not exist")

        return conversation
