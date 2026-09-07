from uuid import UUID
from modules.app.business_prompt.domain import BusinessPromptRepository
from modules.app.business_prompt.domain.exceptions import BusinessDoesNotExist


class BusinessPromptLister:
    """
    Class to list the Business Prompts owned by a user's business
    """

    def __init__(self, business_prompt_repository: BusinessPromptRepository):
        """
        Args:
            business_prompt_repository: repository for business prompt database table operations
        """

        self.__business_prompt_repository = business_prompt_repository

    async def list(self, user_id: UUID):
        business_id = await self.__business_prompt_repository.get_business_id_by_user_id(user_id)
        if not business_id:
            raise BusinessDoesNotExist(f"Business for user with id: {user_id} does not exist")

        return await self.__business_prompt_repository.list_by_business_id(business_id=business_id)
