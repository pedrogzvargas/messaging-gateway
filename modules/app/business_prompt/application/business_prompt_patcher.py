from uuid import UUID
from modules.app.business_prompt.domain import BusinessPrompt
from modules.app.business_prompt.domain import BusinessPromptRepository
from modules.app.business_prompt.domain.exceptions import BusinessDoesNotExist
from modules.app.business_prompt.domain.exceptions import BusinessPromptDoesNotExist
from modules.shared.persistence.domain import UnitOfWork


class BusinessPromptPatcher:
    """
    Class to patch a single Business Prompt owned by a user's business, by key
    """

    def __init__(self, unit_of_work: UnitOfWork, business_prompt_repository: BusinessPromptRepository):
        """
        Args:
            unit_of_work: unit of work to persist the change
            business_prompt_repository: repository for business prompt database table operations
        """

        self.__unit_of_work = unit_of_work
        self.__business_prompt_repository = business_prompt_repository

    async def patch(self, user_id: UUID, key: str, data: dict) -> BusinessPrompt:
        business_id = await self.__business_prompt_repository.get_business_id_by_user_id(user_id)
        if not business_id:
            raise BusinessDoesNotExist(f"Business for user with id: {user_id} does not exist")

        business_prompt = await self.__business_prompt_repository.get_by_fields(business_id=business_id, key=key)
        if not business_prompt:
            raise BusinessPromptDoesNotExist(f"Business prompt with key: {key} not found")

        business_prompt.patch(data=data)
        async with self.__unit_of_work:
            await self.__business_prompt_repository.patch(business_prompt)

        return business_prompt
