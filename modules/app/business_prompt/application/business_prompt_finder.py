from uuid import UUID
from modules.app.business_prompt.domain import BusinessPromptRepository
from modules.app.business_prompt.domain.exceptions import BusinessDoesNotExist
from modules.app.business_prompt.domain.exceptions import BusinessPromptDoesNotExist


class BusinessPromptFinder:
    """
    Class to find a single Business Prompt owned by a user's business, by key
    """

    def __init__(self, business_prompt_repository: BusinessPromptRepository):
        """
        Args:
            business_prompt_repository: repository for business prompt database table operations
        """

        self.__business_prompt_repository = business_prompt_repository

    async def find(self, user_id: UUID, key: str):
        business_id = await self.__business_prompt_repository.get_business_id_by_user_id(user_id)
        if not business_id:
            raise BusinessDoesNotExist(f"Business for user with id: {user_id} does not exist")

        business_prompt = await self.__business_prompt_repository.get_by_fields(business_id=business_id, key=key)
        if not business_prompt:
            raise BusinessPromptDoesNotExist(f"Business prompt with key: {key} not found")

        return business_prompt
