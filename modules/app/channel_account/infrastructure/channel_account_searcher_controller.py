from sqlalchemy.ext.asyncio import AsyncSession
from modules.app.channel_account.domain import ChannelAccountRepository
from modules.app.channel_account.application import ChannelAccountSearcher
from modules.app.channel_account.infrastructure import PgChannelAccountRepository
from modules.shared.http.domain import status
from modules.shared.http.domain import messages
from modules.shared.environ.domain import Environ
from modules.shared.logger.domain import Logger
from modules.shared.environ.infrastructure import PyEnviron
from modules.shared.logger.infrastructure import PyLogger
from modules.shared.http.infrastructure import PageResponse
from .channel_account_response import ChannelAccountResponse


class ChannelAccountSearcherController:
    """
    Class controller to search channel account
    """

    def __init__(
        self,
        session: AsyncSession,
        channel_account_repository: ChannelAccountRepository | None = None,
        environ: Environ | None = None,
        logger: Logger | None = None,
    ):
        """
        Args:
            channel_account_repository: repository for channel account database table operations
            environ: environ variable reader
            logger: logger
        """

        self.__session = session
        self.__environ = environ or PyEnviron()
        self.__channel_account_repository = channel_account_repository or PgChannelAccountRepository(session=self.__session)

        self.__logger = logger or PyLogger(
            level=self.__environ.get_str("LOG_LEVEL"),
            format=self.__environ.get_str("LOG_FORMAT"),
        )

    async def search(self, query_params: dict):
        try:
            channel_account_searcher = ChannelAccountSearcher(channel_account_repository=self.__channel_account_repository)
            channels_response = await channel_account_searcher.search(query_params=query_params)
            customers = PageResponse[ChannelAccountResponse](
                page=channels_response.page,
                limit=channels_response.limit,
                total=channels_response.total,
                pages=channels_response.pages,
                results=[
                    ChannelAccountResponse.model_validate(item)
                    for item in channels_response.items
                ]
            )
            response = customers, status.HTTP_200_OK

        except Exception as ex:
            self.__logger.error(f"ChannelAccountSearcherController: {ex}")
            response = {
                "success": False,
                "message": messages.INTERNAL_SERVER_ERROR,
                "data": {}
            }, status.HTTP_500_INTERNAL_SERVER_ERROR
            return response

        else:
            return response
