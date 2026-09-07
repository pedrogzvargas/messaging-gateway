from uuid import UUID
from datetime import datetime
import pytest
from unittest.mock import AsyncMock
from modules.app.business_prompt.infrastructure import BusinessPromptPatcherController
from modules.app.business_prompt.domain import BusinessPrompt


def _build_business_prompt(business_id: UUID) -> BusinessPrompt:
    return BusinessPrompt(
        id=UUID("41ad6238-a88f-495a-9254-cca57fbb735b"),
        business_id=business_id,
        key="greeting",
        description="Greeting prompt",
        content="Say hello to the customer",
        role="system",
        is_active=True,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


@pytest.mark.asyncio
async def test_business_prompt_patcher() -> None:
    user_id = "611f6649-527b-4af1-8a1a-b66479b5eb2e"
    business_id = UUID("c75e8241-2de8-462d-b673-cfd55c0edc0f")
    session = AsyncMock()
    unit_of_work = AsyncMock()
    business_prompt_repository = AsyncMock()
    business_prompt_repository.get_business_id_by_user_id.return_value = business_id
    business_prompt_repository.get_by_fields.return_value = _build_business_prompt(business_id)

    business_prompt_patcher_controller = BusinessPromptPatcherController(
        session=session,
        unit_of_work=unit_of_work,
        business_prompt_repository=business_prompt_repository,
    )

    response, code = await business_prompt_patcher_controller.patch(
        user_id=UUID(user_id),
        key="greeting",
        data={"content": "Hola, bienvenido"},
    )

    assert response.get("success") is True
    assert code == 200
    assert "data" not in response
    business_prompt_repository.patch.assert_awaited_once()
    patched_business_prompt = business_prompt_repository.patch.call_args.args[0]
    assert patched_business_prompt.content == "Hola, bienvenido"


@pytest.mark.asyncio
async def test_business_prompt_patcher_only_patches_whitelisted_fields() -> None:
    user_id = "611f6649-527b-4af1-8a1a-b66479b5eb2e"
    business_id = UUID("c75e8241-2de8-462d-b673-cfd55c0edc0f")
    session = AsyncMock()
    unit_of_work = AsyncMock()
    business_prompt_repository = AsyncMock()
    business_prompt_repository.get_business_id_by_user_id.return_value = business_id
    business_prompt_repository.get_by_fields.return_value = _build_business_prompt(business_id)

    business_prompt_patcher_controller = BusinessPromptPatcherController(
        session=session,
        unit_of_work=unit_of_work,
        business_prompt_repository=business_prompt_repository,
    )

    other_key = "faq"
    response, code = await business_prompt_patcher_controller.patch(
        user_id=UUID(user_id),
        key="greeting",
        data={"content": "Hola", "key": other_key},
    )

    assert code == 200
    assert "data" not in response
    patched_business_prompt = business_prompt_repository.patch.call_args.args[0]
    assert patched_business_prompt.key == "greeting"
    assert patched_business_prompt.content == "Hola"


@pytest.mark.asyncio
async def test_business_does_not_exist_on_business_prompt_patcher() -> None:
    user_id = "611f6649-527b-4af1-8a1a-b66479b5eb2e"
    session = AsyncMock()
    unit_of_work = AsyncMock()
    business_prompt_repository = AsyncMock()
    business_prompt_repository.get_business_id_by_user_id.return_value = None

    business_prompt_patcher_controller = BusinessPromptPatcherController(
        session=session,
        unit_of_work=unit_of_work,
        business_prompt_repository=business_prompt_repository,
    )

    response, code = await business_prompt_patcher_controller.patch(
        user_id=UUID(user_id),
        key="greeting",
        data={"content": "Hola"},
    )

    assert response.get("success") is False
    assert code == 404
    business_prompt_repository.patch.assert_not_awaited()


@pytest.mark.asyncio
async def test_business_prompt_does_not_exist_on_business_prompt_patcher() -> None:
    user_id = "611f6649-527b-4af1-8a1a-b66479b5eb2e"
    business_id = UUID("c75e8241-2de8-462d-b673-cfd55c0edc0f")
    session = AsyncMock()
    unit_of_work = AsyncMock()
    business_prompt_repository = AsyncMock()
    business_prompt_repository.get_business_id_by_user_id.return_value = business_id
    business_prompt_repository.get_by_fields.return_value = None

    business_prompt_patcher_controller = BusinessPromptPatcherController(
        session=session,
        unit_of_work=unit_of_work,
        business_prompt_repository=business_prompt_repository,
    )

    response, code = await business_prompt_patcher_controller.patch(
        user_id=UUID(user_id),
        key="context",
        data={"content": "Hola"},
    )

    assert response.get("success") is False
    assert code == 404
    business_prompt_repository.patch.assert_not_awaited()
