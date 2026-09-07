from sqlalchemy import select
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from modules.app.customer_notification.domain import CustomerNotificationRepository
from modules.app.customer_notification.application import CustomerNotificationItem
from modules.shared.http.infrastructure import PageResult
from sqlalchemy_models import CustomerNotificationModel


class PgCustomerNotificationRepository(CustomerNotificationRepository):

    def __init__(self, session: AsyncSession):
        self.__session = session

    async def simple_search(self, filters: dict, limit: int = 10, page: int = 1) -> PageResult[CustomerNotificationItem]:
        """simple search for customer notification"""

        allowed_filters = {
            "status": (CustomerNotificationModel.status, "eq"),
            "customer_id": (CustomerNotificationModel.customer_id, "eq"),
        }

        stmt = select(
            CustomerNotificationModel.id,
            CustomerNotificationModel.customer_id,
            CustomerNotificationModel.content,
            CustomerNotificationModel.status,
            CustomerNotificationModel.created_at,
            CustomerNotificationModel.updated_at,
        ).order_by(CustomerNotificationModel.created_at.desc())

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

        return PageResult[CustomerNotificationItem](
            page=page,
            limit=limit,
            total=total,
            pages=pages,
            items=results,
        )
