from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from modules.app.business_prompt.domain import BusinessPromptRepository
from modules.app.business_prompt.domain.exceptions import BusinessDoesNotExist
from modules.app.business_prompt.application import BusinessPromptLister
from modules.app.business_prompt.infrastructure import PgBusinessPromptRepository
from modules.shared.http.domain import status
from modules.shared.http.domain import messages
from .business_prompt_response import BusinessPromptResponse


class BusinessPromptListerController:
    """
    Class controller to list the Business Prompts of a user's business
    """

    def __init__(
        self,
        session: AsyncSession,
        business_prompt_repository: BusinessPromptRepository | None = None,
    ):
        """
        Args:
            session: database session
            business_prompt_repository: repository for business prompt database table operations
        """

        self.__session = session
        self.__business_prompt_repository = business_prompt_repository or PgBusinessPromptRepository(session=self.__session)

    async def list(self, user_id: UUID):
        try:
            business_prompt_lister = BusinessPromptLister(business_prompt_repository=self.__business_prompt_repository)
            business_prompts = await business_prompt_lister.list(user_id=user_id)

            response = {
                "success": True,
                "message": messages.SUCCESS_MESSAGE,
                "results": [
                    BusinessPromptResponse.model_validate(business_prompt) for business_prompt in business_prompts
                ]
            }, status.HTTP_200_OK

        except BusinessDoesNotExist as ex:
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
