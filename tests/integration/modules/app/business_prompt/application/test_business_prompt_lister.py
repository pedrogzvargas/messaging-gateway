from uuid import UUID
import pytest
from modules.app.business_prompt.infrastructure import PgBusinessPromptRepository
from modules.app.business_prompt.application import BusinessPromptLister
from modules.app.business_prompt.domain.exceptions import BusinessDoesNotExist
from sqlalchemy_models import BusinessPromptModel
from sqlalchemy_models import BusinessModel
from sqlalchemy_models import CustomerModel
from sqlalchemy_models import UserModel
from tests.integration.fixtures import db_session


async def _seed_business(db_session):
    user = UserModel(
        id=UUID("611f6649-527b-4af1-8a1a-b66479b5eb2e"),
        email="demo@noemail.com",
        password="test",
        is_active=True,
    )
    customer = CustomerModel(
        id=UUID("611f6649-527b-4af1-8a1a-b66479b5eb2e"),
        user_id=UUID("611f6649-527b-4af1-8a1a-b66479b5eb2e"),
        name="Pedro",
        last_name="Gonzalez"
    )
    business = BusinessModel(
        id=UUID("c75e8241-2de8-462d-b673-cfd55c0edc0f"),
        customer_id=UUID("611f6649-527b-4af1-8a1a-b66479b5eb2e"),
        name="Vualdex",
    )
    db_session.add_all([user, customer, business])

    return user, business


def _build_lister(db_session):
    return BusinessPromptLister(business_prompt_repository=PgBusinessPromptRepository(db_session))


@pytest.mark.asyncio
async def test_list_business_prompts_for_user(db_session):
    user, business = await _seed_business(db_session)
    prompt_1 = BusinessPromptModel(
        id=UUID("41ad6238-a88f-495a-9254-cca57fbb735b"),
        business_id=business.id,
        key="greeting",
        description="Greeting prompt",
        content="Say hello to the customer",
        role="system",
        is_active=True,
    )
    prompt_2 = BusinessPromptModel(
        id=UUID("3d9400dc-206a-4301-8e19-099fc5d28b18"),
        business_id=business.id,
        key="faq",
        description="FAQ prompt",
        content="Answer using the FAQ context",
        role="system",
        is_active=True,
    )
    db_session.add_all([prompt_1, prompt_2])

    business_prompt_lister = _build_lister(db_session)
    business_prompts = await business_prompt_lister.list(user_id=user.id)

    assert len(business_prompts) == 2
    assert {business_prompt.key for business_prompt in business_prompts} == {"greeting", "faq"}


@pytest.mark.asyncio
async def test_list_raises_when_business_does_not_exist_for_user(db_session):
    business_prompt_lister = _build_lister(db_session)

    with pytest.raises(BusinessDoesNotExist):
        await business_prompt_lister.list(user_id=UUID("611f6649-527b-4af1-8a1a-b66479b5eb2e"))
