from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from modules.app.conversation.domain import ConversationRepository
from modules.app.conversation.domain.exceptions import ConversationDoesNotExist
from modules.app.conversation.infrastructure import PgConversationRepository
from modules.app.conversation.infrastructure import ConversationResponse
from modules.app.message.domain import MessageRepository
from modules.app.message.infrastructure import PgMessageRepository
from modules.app.message.application import ConversationMessageFinder
from modules.shared.http.domain import status
from modules.shared.http.domain import messages
from .message_response import MessageResponse


class ConversationMessageFinderController:
    """
    Class controller to get a Conversation detail with its Messages
    """

    def __init__(
        self,
        session: AsyncSession,
        conversation_repository: ConversationRepository | None = None,
        message_repository: MessageRepository | None = None,
    ):
        """
        Args:
            conversation_repository: repository for conversation database table operations
            message_repository: repository for message database table operations
        """

        self.__session = session
        self.__conversation_repository = conversation_repository or PgConversationRepository(session=self.__session)
        self.__message_repository = message_repository or PgMessageRepository(session=self.__session)

    async def find(self, conversation_id: UUID, limit: int = 10):
        try:
            conversation_message_finder = ConversationMessageFinder(
                conversation_repository=self.__conversation_repository,
                message_repository=self.__message_repository,
            )
            conversation_messages = await conversation_message_finder.find(
                conversation_id=conversation_id,
                limit=limit,
            )

            response = {
                "success": True,
                "message": messages.SUCCESS_MESSAGE,
                "data": {
                    "conversation": ConversationResponse.model_validate(conversation_messages.conversation),
                    "messages": [
                        MessageResponse.model_validate(message) for message in conversation_messages.messages
                    ],
                }
            }, status.HTTP_200_OK

        except ConversationDoesNotExist as ex:
            response = {"success": False, "message": f"{ex}", "data": {}}, status.HTTP_404_NOT_FOUND
            return response

        except Exception as ex:
            response = {
                "success": False,
                "message": messages.INTERNAL_SERVER_ERROR,
                "data": {}
            }, status.HTTP_500_INTERNAL_SERVER_ERROR
            return response

        else:
            return response
