from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from modules.app.conversation.domain import ConversationRepository
from modules.app.conversation.domain.exceptions import ConversationDoesNotExist
from modules.app.conversation.infrastructure import PgConversationRepository
from modules.app.conversation.application import ConversationFinder
from modules.shared.http.domain import status
from modules.shared.http.domain import messages
from .conversation_response import ConversationResponse


class ConversationFinderController:
    """
    Class controller to get Conversation
    """

    def __init__(
        self,
        session: AsyncSession,
        conversation_repository: ConversationRepository | None = None,
    ):
        """
        Args:
            conversation_repository: repository for conversation database table operations
        """

        self.__session = session
        self.__conversation_repository = conversation_repository or PgConversationRepository(session=self.__session)

    async def find(self, conversation_id: UUID):
        try:
            conversation_finder = ConversationFinder(conversation_repository=self.__conversation_repository)
            conversation = await conversation_finder.find(conversation_id=conversation_id)
            conversation = ConversationResponse.model_validate(conversation)
            response = {
                "success": True,
                "message": messages.SUCCESS_MESSAGE,
                "data": conversation
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
