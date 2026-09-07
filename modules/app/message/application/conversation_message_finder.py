from uuid import UUID
from modules.app.conversation.domain import ConversationRepository
from modules.app.conversation.domain.exceptions import ConversationDoesNotExist
from modules.app.message.domain import MessageRepository
from .conversation_messages import ConversationMessages


class ConversationMessageFinder:
    """
    Class to get a Conversation detail with its Messages
    """

    def __init__(
        self,
        conversation_repository: ConversationRepository,
        message_repository: MessageRepository,
    ):
        """
        Args:
            conversation_repository: repository for conversation database table operations
            message_repository: repository for message database table operations
        """

        self.__conversation_repository = conversation_repository
        self.__message_repository = message_repository

    async def find(self, conversation_id: UUID, limit: int = 10) -> ConversationMessages:
        conversation = await self.__conversation_repository.get_detail(conversation_id)
        if not conversation:
            raise ConversationDoesNotExist(f"Conversation with id: {conversation_id} does not exist")

        messages = await self.__message_repository.list_by_conversation(
            conversation_id=conversation_id,
            # limit=limit, # TODO add support for scroll on frontend and uncomment this
        )

        return ConversationMessages(conversation=conversation, messages=messages or [])
