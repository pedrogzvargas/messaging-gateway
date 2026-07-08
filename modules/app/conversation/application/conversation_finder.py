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

    async def find(self, conversation_id: UUID):
        conversation = await self.__conversation_repository.get_detail(conversation_id)
        if not conversation:
            raise ConversationDoesNotExist(f"Conversation with id: {conversation_id} does not exist")

        return conversation
