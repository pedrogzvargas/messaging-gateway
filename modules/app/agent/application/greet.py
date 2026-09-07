from uuid import UUID
from modules.app.business_prompt.domain import BusinessPromptRepository


class Greet:

    def __init__(self, business_prompt_repository: BusinessPromptRepository):
        self.business_prompt_repository = business_prompt_repository

    async def execute(self, business_id: UUID):
        greet = await self.business_prompt_repository.get_by_fields(business_id=business_id, key="greeting")
        return greet.content
