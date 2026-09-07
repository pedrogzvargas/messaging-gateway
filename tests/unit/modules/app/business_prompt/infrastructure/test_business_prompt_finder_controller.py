from uuid import UUID
from datetime import datetime
import pytest
from unittest.mock import AsyncMock
from modules.app.business_prompt.infrastructure import BusinessPromptFinderController
from modules.app.business_prompt.domain import BusinessPrompt


@pytest.mark.asyncio
async def test_business_prompt_finder() -> None:
    user_id = "611f6649-527b-4af1-8a1a-b66479b5eb2e"
    business_id = "c75e8241-2de8-462d-b673-cfd55c0edc0f"
    session = AsyncMock()
    business_prompt_repository = AsyncMock()
    business_prompt_repository.get_business_id_by_user_id.return_value = UUID(business_id)
    business_prompt_repository.get_by_fields.return_value = BusinessPrompt(
        id=UUID("41ad6238-a88f-495a-9254-cca57fbb735b"),
        business_id=UUID(business_id),
        key="greeting",
        description="Greeting prompt",
        content="Say hello to the customer",
        role="system",
        is_active=True,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    business_prompt_finder_controller = BusinessPromptFinderController(
        session=session,
        business_prompt_repository=business_prompt_repository,
    )

    response, code = await business_prompt_finder_controller.find(user_id=UUID(user_id), key="greeting")

    assert response.get("success") is True
    assert code == 200
    assert response.get("data").key == "greeting"
    business_prompt_repository.get_by_fields.assert_awaited_once_with(business_id=UUID(business_id), key="greeting")


@pytest.mark.asyncio
async def test_business_does_not_exist_on_business_prompt_finder() -> None:
    user_id = "611f6649-527b-4af1-8a1a-b66479b5eb2e"
    session = AsyncMock()
    business_prompt_repository = AsyncMock()
    business_prompt_repository.get_business_id_by_user_id.return_value = None

    business_prompt_finder_controller = BusinessPromptFinderController(
        session=session,
        business_prompt_repository=business_prompt_repository,
    )

    response, code = await business_prompt_finder_controller.find(user_id=UUID(user_id), key="greeting")

    assert response.get("success") is False
    assert code == 404
    business_prompt_repository.get_by_fields.assert_not_awaited()


@pytest.mark.asyncio
async def test_business_prompt_does_not_exist_on_business_prompt_finder() -> None:
    user_id = "611f6649-527b-4af1-8a1a-b66479b5eb2e"
    business_id = "c75e8241-2de8-462d-b673-cfd55c0edc0f"
    session = AsyncMock()
    business_prompt_repository = AsyncMock()
    business_prompt_repository.get_business_id_by_user_id.return_value = UUID(business_id)
    business_prompt_repository.get_by_fields.return_value = None

    business_prompt_finder_controller = BusinessPromptFinderController(
        session=session,
        business_prompt_repository=business_prompt_repository,
    )

    response, code = await business_prompt_finder_controller.find(user_id=UUID(user_id), key="main_context")

    assert response.get("success") is False
    assert code == 404
