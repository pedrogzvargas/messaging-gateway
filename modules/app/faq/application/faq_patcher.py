from uuid import UUID
from modules.app.faq.domain.exceptions import FaqDoesNotExist
from modules.shared.persistence.domain import UnitOfWork
from modules.shared.bus.event.domain import EventBus
from modules.app.faq.domain import FaqRepository
from modules.app.business.domain import BusinessRepository
from modules.app.business.domain.exceptions import  BusinessDoesNotExist
from openai import AsyncOpenAI


class FaqPatcher:

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

    async def patch(
        self,
        faq_id: UUID,
        customer_id: UUID,
        data: dict,
    ):

        business = await self.__business_repository.get_by_customer_id(customer_id=customer_id)

        if not business:
            raise BusinessDoesNotExist(f"Business with customer_id:{customer_id} does not exist")

        faq = await self.__faq_repository.get_by_fields(id=faq_id, business_id=business.id)

        if not faq:
            raise FaqDoesNotExist(f"Faq with id:{faq_id} does not exist")

        question = data.get("question", faq.question)
        answer = data.get("answer", faq.answer)
        embedding = faq.embedding

        if question != faq.question or answer != faq.answer:

            embedding = await self.__open_ai.embeddings.create(
                model="text-embedding-3-small",
                input=f"""
                    Pregunta:
                    {question}
        
                    Respuesta:
                    {answer}
                """
            )

            embedding = embedding.data[0].embedding

        data.update({"embedding": embedding})

        faq.patch(data=data)

        async with self.__unit_of_work:
            await self.__faq_repository.patch(faq)
