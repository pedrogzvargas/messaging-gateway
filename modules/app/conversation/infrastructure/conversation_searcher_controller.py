from sqlalchemy.ext.asyncio import AsyncSession
from modules.app.conversation.domain import ConversationRepository
from modules.app.conversation.application import ConversationSearcher
from modules.app.conversation.infrastructure import PgConversationRepository
from modules.shared.http.domain import status
from modules.shared.http.domain import messages
from modules.shared.environ.domain import Environ
from modules.shared.logger.domain import Logger
from modules.shared.environ.infrastructure import PyEnviron
from modules.shared.logger.infrastructure import PyLogger
from modules.shared.http.infrastructure import PageResponse
from .conversation_response import ConversationResponse


class ConversationSearcherController:
    """
    Class controller to search Customers
    """

    def __init__(
        self,
        session: AsyncSession,
        conversation_repository: ConversationRepository | None = None,
        environ: Environ | None = None,
        logger: Logger | None = None,
    ):
        """
        Args:
            conversation_repository: repository for conversation database table operations
            entity_serializer: serializer class
            environ: environ variable reader
            logger: logger
        """

        self.__session = session
        self.__environ = environ or PyEnviron()
        self.__conversation_repository = conversation_repository or PgConversationRepository(session=self.__session)

        self.__logger = logger or PyLogger(
            level=self.__environ.get_str("LOG_LEVEL"),
            format=self.__environ.get_str("LOG_FORMAT"),
        )

    async def search(self, query_params: dict):
        try:
            conversation_searcher = ConversationSearcher(conversation_repository=self.__conversation_repository)
            customers_response = await conversation_searcher.search(query_params=query_params)
            customers = PageResponse[ConversationResponse](
                page=customers_response.page,
                limit=customers_response.limit,
                total=customers_response.total,
                pages=customers_response.pages,
                results=[
                    ConversationResponse.model_validate(item)
                    for item in customers_response.items
                ]
            )
            response = customers, status.HTTP_200_OK

        except Exception as ex:
            self.__logger.error(f"ConversationSearcherController: {ex}")
            response = {
                "success": False,
                "message": messages.INTERNAL_SERVER_ERROR,
                "data": {}
            }, status.HTTP_500_INTERNAL_SERVER_ERROR
            return response

        else:
            return response
