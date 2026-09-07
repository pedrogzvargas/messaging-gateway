from uuid import UUID
from modules.app.faq.domain import Faq
from modules.app.faq.domain.exceptions import FaqAlreadyExist
from modules.shared.persistence.domain import UnitOfWork
from modules.shared.bus.event.domain import EventBus
from modules.app.faq.domain import FaqRepository
from modules.app.business.domain import BusinessRepository
from modules.app.business.domain.exceptions import  BusinessDoesNotExist
from openai import AsyncOpenAI


class FaqCreator:

    def __init__(
        self,
        unit_of_work: UnitOfWork,
        event_bus: EventBus,
        business_repository: BusinessRepository,
        faq_repository: FaqRepository,
        open_ai: AsyncOpenAI,
    ):
        self.__unit_of_work = unit_of_work
        self.__event_bus = event_bus
        self.__business_repository = business_repository
        self.__faq_repository = faq_repository
        self.__open_ai = open_ai

    async def create(
        self,
        id: UUID,
        customer_id: UUID,
        question: str,
        answer: str,
        is_active: bool
    ):

        if await self.__faq_repository.get(id=id):
            raise FaqAlreadyExist(f"Faq with id:{id} already exists")

        business = await self.__business_repository.get_by_customer_id(customer_id=customer_id)

        if not business:
            raise BusinessDoesNotExist(f"Business with customer_id:{customer_id} does not exist")

        embedding = await self.__open_ai.embeddings.create(
            model="text-embedding-3-small",
            input=f"""
                Pregunta:
                {question}
    
                Respuesta:
                {answer}
            """
        )

        faq = Faq.create(
            id=id,
            business_id=business.id,
            question=question,
            answer=answer,
            embedding=embedding.data[0].embedding,
            is_active=is_active,
        )

        async with self.__unit_of_work:
            await self.__faq_repository.add(faq)
