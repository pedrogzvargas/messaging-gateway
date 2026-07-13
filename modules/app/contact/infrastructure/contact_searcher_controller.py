from sqlalchemy.ext.asyncio import AsyncSession
from modules.app.contact.domain import ContactRepository
from modules.app.contact.application import ContactSearcher
from modules.app.contact.infrastructure import PgContactRepository
from modules.shared.http.domain import status
from modules.shared.http.domain import messages
from modules.shared.environ.domain import Environ
from modules.shared.logger.domain import Logger
from modules.shared.environ.infrastructure import PyEnviron
from modules.shared.logger.infrastructure import PyLogger
from modules.shared.http.infrastructure import PageResponse
from .contact_response import ContactResponse


class ContactSearcherController:
    """
    Class controller to search channel account
    """

    def __init__(
        self,
        session: AsyncSession,
        contact_repository: ContactRepository | None = None,
        environ: Environ | None = None,
        logger: Logger | None = None,
    ):
        """
        Args:
            contact_repository: repository for contact database table operations
            environ: environ variable reader
            logger: logger
        """

        self.__session = session
        self.__environ = environ or PyEnviron()
        self.__contact_repository = contact_repository or PgContactRepository(session=self.__session)

        self.__logger = logger or PyLogger(
            level=self.__environ.get_str("LOG_LEVEL"),
            format=self.__environ.get_str("LOG_FORMAT"),
        )

    async def search(self, query_params: dict):
        try:
            contact_searcher = ContactSearcher(contact_repository=self.__contact_repository)
            contacts_response = await contact_searcher.search(query_params=query_params)
            customers = PageResponse[ContactResponse](
                page=contacts_response.page,
                limit=contacts_response.limit,
                total=contacts_response.total,
                pages=contacts_response.pages,
                results=[
                    ContactResponse.model_validate(item)
                    for item in contacts_response.items
                ]
            )
            response = customers, status.HTTP_200_OK

        except Exception as ex:
            self.__logger.error(f"ContactSearcherController: {ex}")
            response = {
                "success": False,
                "message": messages.INTERNAL_SERVER_ERROR,
                "data": {}
            }, status.HTTP_500_INTERNAL_SERVER_ERROR
            return response

        else:
            return response
