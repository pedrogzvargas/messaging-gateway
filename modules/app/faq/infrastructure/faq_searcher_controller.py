from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from modules.app.faq.domain import FaqRepository
from modules.app.faq.application import FaqSearcher
from modules.app.faq.infrastructure import PgFaqRepository
from modules.shared.http.domain import status
from modules.shared.http.domain import messages
from modules.shared.http.infrastructure import PageResponse
from .faq_response import FaqResponse


class FaqSearcherController:
    """
    Class controller to search FAQs
    """

    def __init__(
        self,
        session: AsyncSession,
        faq_repository: FaqRepository | None = None,
    ):
        """
        Args:
            session: database session
            faq_repository: repository for faq database table operations
        """

        self.__session = session
        self.__faq_repository = faq_repository or PgFaqRepository(session=self.__session)

    async def search(self, query_params: dict, user_id: UUID):
        try:
            faq_searcher = FaqSearcher(faq_repository=self.__faq_repository)
            faqs_response = await faq_searcher.search(query_params=query_params, user_id=user_id)
            faqs = PageResponse[FaqResponse](
                page=faqs_response.page,
                limit=faqs_response.limit,
                total=faqs_response.total,
                pages=faqs_response.pages,
                results=[
                    FaqResponse.model_validate(item)
                    for item in faqs_response.items
                ]
            )
            response = faqs, status.HTTP_200_OK

        except Exception as ex:
            response = {
                "success": False,
                "message": messages.INTERNAL_SERVER_ERROR,
                "data": {}
            }, status.HTTP_500_INTERNAL_SERVER_ERROR
            return response

        else:
            return response
