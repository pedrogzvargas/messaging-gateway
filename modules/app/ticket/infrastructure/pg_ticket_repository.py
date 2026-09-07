from uuid import UUID
from sqlalchemy import select
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from modules.app.ticket.domain import TicketRepository
from modules.app.ticket.application import TicketItem
from modules.shared.http.infrastructure import PageResult
from sqlalchemy_models import TicketModel
from .ticket_mapper import TicketMapper


class PgTicketRepository(TicketRepository):

    def __init__(self, session: AsyncSession):
        self.__session = session

    async def get(self, id: UUID):
        """get ticket"""

        ticket = await self.__session.get(TicketModel, id)

        if ticket:
            return TicketMapper.to_domain(ticket)

        return None

    async def add(self, ticket):
        """add ticket to session"""

        self.__session.add(TicketMapper.to_model(ticket))
        await self.__session.flush()

    async def simple_search(self, filters: dict, limit: int = 10, page: int = 1) -> PageResult[TicketItem]:
        """simple search for ticket"""

        allowed_filters = {
            "status": (TicketModel.status, "eq"),
            "customer_id": (TicketModel.customer_id, "eq"),
        }

        stmt = select(
            TicketModel.id,
            TicketModel.customer_id,
            TicketModel.details,
            TicketModel.status,
            TicketModel.created_at,
            TicketModel.updated_at,
        ).order_by(TicketModel.created_at.desc())

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

        return PageResult[TicketItem](
            page=page,
            limit=limit,
            total=total,
            pages=pages,
            items=results,
        )

    async def patch(self, ticket):
        """patch ticket"""

        await self.__session.merge(TicketMapper.to_model(ticket))
