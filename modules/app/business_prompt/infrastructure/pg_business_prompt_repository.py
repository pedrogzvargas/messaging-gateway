from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy import desc
from sqlalchemy import func
from modules.app.business_prompt.domain import BusinessPromptRepository
from modules.app.business_prompt.application import BusinessPromptItem
from modules.shared.http.infrastructure import PageResult
from sqlalchemy_models import BusinessPromptModel
from sqlalchemy_models import BusinessModel
from sqlalchemy_models import CustomerModel
from .business_prompt_mapper import BusinessPromptMapper


class PgBusinessPromptRepository(BusinessPromptRepository):
    """
    PgBusinessPromptRepository
    """

    def __init__(self, session: AsyncSession):
        self.__session = session

    async def get(self, id: UUID):
        """get business prompt"""

        business_prompt = await self.__session.get(BusinessPromptModel, id)

        if business_prompt:
            return BusinessPromptMapper.to_domain(business_prompt)

        return None

    async def get_by_fields(self, **fields):
        """get prompt by fields"""

        stmt = select(BusinessPromptModel)

        for field, value in fields.items():
            if hasattr(BusinessPromptModel, field):
                column = getattr(BusinessPromptModel, field)
                stmt = stmt.where(column == value)

        query_result = await self.__session.execute(stmt)
        prompt = query_result.scalar_one_or_none()

        if prompt is None:
            return None

        return BusinessPromptMapper.to_domain(prompt)

    async def patch(self, business_prompt):
        """patch business prompt"""

        await self.__session.merge(BusinessPromptMapper.to_model(business_prompt))

    async def list_by_business_id(self, business_id: UUID):
        """list business prompts by business id"""

        stmt = select(BusinessPromptModel).where(
            BusinessPromptModel.business_id == business_id
        ).order_by(desc(BusinessPromptModel.created_at))

        result = await self.__session.execute(stmt)
        business_prompts = result.scalars().all()

        return [BusinessPromptMapper.to_domain(business_prompt) for business_prompt in business_prompts]

    async def simple_search(self, filters: dict, limit: int = 10, page: int = 1) -> PageResult[BusinessPromptItem]:
        """simple search for business prompt"""

        allowed_filters = {
            "key": (BusinessPromptModel.key, "contains"),
            "role": (BusinessPromptModel.role, "eq"),
            "business_id": (BusinessPromptModel.business_id, "eq"),
        }

        stmt = select(
            BusinessPromptModel.id,
            BusinessPromptModel.business_id,
            BusinessPromptModel.key,
            BusinessPromptModel.description,
            BusinessPromptModel.role,
            BusinessPromptModel.is_active,
            BusinessPromptModel.created_at,
            BusinessPromptModel.updated_at,
        ).order_by(desc(BusinessPromptModel.created_at))

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

        return PageResult[BusinessPromptItem](
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
