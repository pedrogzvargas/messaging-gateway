from uuid import UUID
from datetime import datetime
from datetime import timezone
from modules.app.conversation.domain import ConversationRepository
from modules.app.business.domain.exceptions import BusinessDoesNotExist
from .dashboard_summary import DashboardSummary


class DashboardSummaryFinder:
    """
    Class to get the summary metrics shown in a user's dashboard
    """

    def __init__(self, conversation_repository: ConversationRepository):
        """
        Args:
            conversation_repository: repository for conversation database table operations
        """

        self.__conversation_repository = conversation_repository

    async def find(self, user_id: UUID) -> DashboardSummary:
        business_id = await self.__conversation_repository.get_business_id_by_user_id(user_id)
        if not business_id:
            raise BusinessDoesNotExist(f"Business for user with id: {user_id} does not exist")

        today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)

        conversations_today = await self.__conversation_repository.count_by_business_id(
            business_id=business_id, since=today_start
        )
        conversations_total = await self.__conversation_repository.count_by_business_id(
            business_id=business_id
        )

        return DashboardSummary(
            conversations_today=conversations_today,
            conversations_total=conversations_total,
        )
