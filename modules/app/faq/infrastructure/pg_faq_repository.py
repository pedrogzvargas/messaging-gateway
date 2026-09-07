from uuid import UUID
from sqlalchemy import select
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from langchain_openai import OpenAIEmbeddings
from modules.app.faq.domain import FaqRepository
from modules.app.faq.application import FaqItem
from modules.shared.http.infrastructure import PageResult
from sqlalchemy_models import FAQModel
from sqlalchemy_models import BusinessModel
from sqlalchemy_models import CustomerModel
from .faq_mapper import FaqMapper


class PgFaqRepository(FaqRepository):

    def __init__(self, session: AsyncSession, embeddings: OpenAIEmbeddings | None = None):
        self.__session = session
        self.__embeddings = embeddings

    async def get(self, id: UUID):
        """get webhook"""

        faq = await self.__session.get(FAQModel, id)

        if faq:
            return FaqMapper.to_domain(faq)

        return None

    async def get_by_fields(self, **fields):
        """get prompt by fields"""

        stmt = select(FAQModel)

        for field, value in fields.items():
            if hasattr(FAQModel, field):
                column = getattr(FAQModel, field)
                stmt = stmt.where(column == value)

        query_result = await self.__session.execute(stmt)
        faq = query_result.scalar_one_or_none()

        if faq is None:
            return None

        return FaqMapper.to_domain(faq)

    async def add(self, faq):
        """add wa faq to session"""

        self.__session.add(FaqMapper.to_model(faq))
        await self.__session.flush()

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

    async def patch(self, faq):
        """patch faq"""

        await self.__session.merge(FaqMapper.to_model(faq))

    async def simple_search(self, filters: dict, limit: int = 10, page: int = 1) -> PageResult[FaqItem]:
        """simple search for faq"""

        allowed_filters = {
            "question": (FAQModel.question, "contains"),
            "business_id": (FAQModel.business_id, "eq"),
        }

        stmt = select(
            FAQModel.id,
            FAQModel.business_id,
            FAQModel.question,
            FAQModel.answer,
            FAQModel.is_active,
            FAQModel.created_at,
            FAQModel.updated_at,
        ).order_by(FAQModel.created_at.desc())

        # filters
        for field, value in filters.items():
            column, operator = allowed_filters.get(field, (None, None))
            if column:
                match operator:
                    case "contains":
                        stmt = stmt.where(column.ilike(f"%{value}%"))
                    case "eq":
                        stmt = stmt.where(column == value)

        # count
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = await self.__session.scalar(count_stmt)

        # pagination
        pages = (total + limit - 1) // limit if total >= 1 else 0

        if total > limit:
            offset = (page - 1) * limit
            stmt = stmt.offset(offset).limit(limit)

        result = await self.__session.execute(stmt)
        results = result.mappings().all()

        return PageResult[FaqItem](
            page=page,
            limit=limit,
            total=total,
            pages=pages,
            items=results,
        )

    async def get_business_id_by_user_id(self, user_id: UUID):
        """get the business id owned by the given user"""

        stmt = select(BusinessModel.id).join(
            CustomerModel, BusinessModel.customer_id == CustomerModel.id
        ).where(
            CustomerModel.user_id == user_id
        )

        return await self.__session.scalar(stmt)
