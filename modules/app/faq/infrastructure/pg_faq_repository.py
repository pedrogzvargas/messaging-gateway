from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from langchain_openai import OpenAIEmbeddings
from modules.app.faq.domain import FaqRepository
from sqlalchemy_models import FAQModel


class PgFaqRepository(FaqRepository):

    def __init__(self, session: AsyncSession, embeddings: OpenAIEmbeddings):
        self.__session = session
        self.__embeddings = embeddings

    async def search(self, question: str, limit: int = 2):
        query_embedding = await self.__embeddings.aembed_query(question)
        stmt = (
            select(FAQModel)
            # .where(
            #     FAQModel.service == "general"
            # )
            .order_by(
                FAQModel.embedding.cosine_distance(
                    query_embedding
                )
            )
            .limit(2)
        )

        result = await self.__session.execute(stmt)
        faqs = result.scalars().all()
        return faqs
