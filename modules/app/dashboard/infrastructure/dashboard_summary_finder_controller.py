from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from modules.app.conversation.domain import ConversationRepository
from modules.app.conversation.infrastructure import PgConversationRepository
from modules.app.business.domain.exceptions import BusinessDoesNotExist
from modules.app.dashboard.application import DashboardSummaryFinder
from modules.shared.http.domain import status
from modules.shared.http.domain import messages
from modules.shared.environ.domain import Environ
from modules.shared.environ.infrastructure import PyEnviron
from modules.shared.logger.domain import Logger
from modules.shared.logger.infrastructure import PyLogger
from .dashboard_summary_response import DashboardSummaryResponse


class DashboardSummaryFinderController:
    """
    Class controller to get the summary metrics shown in a user's dashboard
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
            session: database session
            conversation_repository: repository for conversation database table operations
            environ: environ variable reader
            logger: logger
        """

        self.__session = session
        self.__conversation_repository = conversation_repository or PgConversationRepository(session=self.__session)
        self.__environ = environ or PyEnviron()
        self.__logger = logger or PyLogger(
            level=self.__environ.get_str("LOG_LEVEL"),
            format=self.__environ.get_str("LOG_FORMAT"),
        )

    async def find(self, user_id: UUID):
        try:
            dashboard_summary_finder = DashboardSummaryFinder(conversation_repository=self.__conversation_repository)
            dashboard_summary = await dashboard_summary_finder.find(user_id=user_id)

            response = {
                "success": True,
                "message": messages.SUCCESS_MESSAGE,
                "data": DashboardSummaryResponse.model_validate(dashboard_summary),
            }, status.HTTP_200_OK

        except BusinessDoesNotExist as ex:
            response = {"success": False, "message": f"{ex}"}, status.HTTP_404_NOT_FOUND
            return response

        except Exception as ex:
            self.__logger.error(f"DashboardSummaryFinderController: {ex}")
            response = {
                "success": False,
                "message": messages.INTERNAL_SERVER_ERROR,
            }, status.HTTP_500_INTERNAL_SERVER_ERROR
            return response

        else:
            return response
