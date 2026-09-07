from uuid import UUID
import pytest
from unittest.mock import AsyncMock
from modules.app.dashboard.infrastructure import DashboardSummaryFinderController


@pytest.mark.asyncio
async def test_dashboard_summary_finder() -> None:
    user_id = "611f6649-527b-4af1-8a1a-b66479b5eb2e"
    business_id = UUID("c75e8241-2de8-462d-b673-cfd55c0edc0f")
    session = AsyncMock()
    conversation_repository = AsyncMock()
    conversation_repository.get_business_id_by_user_id.return_value = business_id
    conversation_repository.count_by_business_id.side_effect = [3, 42]

    dashboard_summary_finder_controller = DashboardSummaryFinderController(
        session=session,
        conversation_repository=conversation_repository,
    )

    response, code = await dashboard_summary_finder_controller.find(user_id=UUID(user_id))

    assert response.get("success") is True
    assert code == 200
    assert response.get("data").conversations_today == 3
    assert response.get("data").conversations_total == 42
    assert conversation_repository.count_by_business_id.await_count == 2


@pytest.mark.asyncio
async def test_business_does_not_exist_on_dashboard_summary_finder() -> None:
    user_id = "611f6649-527b-4af1-8a1a-b66479b5eb2e"
    session = AsyncMock()
    conversation_repository = AsyncMock()
    conversation_repository.get_business_id_by_user_id.return_value = None

    dashboard_summary_finder_controller = DashboardSummaryFinderController(
        session=session,
        conversation_repository=conversation_repository,
    )

    response, code = await dashboard_summary_finder_controller.find(user_id=UUID(user_id))

    assert response.get("success") is False
    assert code == 404
    conversation_repository.count_by_business_id.assert_not_awaited()
