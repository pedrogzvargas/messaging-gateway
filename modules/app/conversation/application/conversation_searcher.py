from modules.app.conversation.domain import ConversationRepository
from modules.shared.http.infrastructure import PageResult


class ConversationSearcher:
    """
    Class to get search Conversations
    """

    def __init__(self, conversation_repository: ConversationRepository):
        """
        Args:
            conversation_repository: repository for customer database table operations
        """

        self.__conversation_repository = conversation_repository

    async def search(self, query_params: dict) -> PageResult:
        """
        Args:
            query_params (dict): query params.
        Returns:
            dict: paginated conversations.
        """

        if not isinstance(query_params, dict):
            raise ValueError(f"query_params: {query_params} is not instance of dict")

        limit = query_params.pop("limit", 10)
        page = query_params.pop("page", 1)

        cleaned_query_params = {key: value for key, value in query_params.items() if value not in [None, ""]}

        conversation_results: PageResult = await self.__conversation_repository.simple_search(
            filters=cleaned_query_params,
            limit=limit,
            page=page,
        )

        return conversation_results
