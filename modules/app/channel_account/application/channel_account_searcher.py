from modules.app.channel_account.domain import ChannelAccountRepository
from modules.shared.http.infrastructure import PageResult


class ChannelAccountSearcher:
    """
    Class to get search Channel accounts.
    """

    def __init__(self, channel_account_repository: ChannelAccountRepository):
        """
        Args:
            channel_account_repository: repository for channel accounts database table operations
        """

        self.__channel_account_repository = channel_account_repository

    async def search(self, query_params: dict) -> PageResult:
        """
        Args:
            query_params (dict): query params.
        Returns:
            dict: paginated channels.
        """

        if not isinstance(query_params, dict):
            raise ValueError(f"query_params: {query_params} is not instance of dict")

        limit = query_params.pop("limit", 10)
        page = query_params.pop("page", 1)

        cleaned_query_params = {key: value for key, value in query_params.items() if value not in [None, ""]}

        channel_account_results: PageResult = await self.__channel_account_repository.simple_search(
            filters=cleaned_query_params,
            limit=limit,
            page=page,
        )

        return channel_account_results
