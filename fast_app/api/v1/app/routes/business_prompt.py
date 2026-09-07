from uuid import UUID
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Response
from fast_app.core.db_session import get_session
from fast_app.core.auth import require_permission
from fast_app.api.v1.app.schemas import PatchBusinessPrompt
from modules.app.business_prompt.infrastructure import BusinessPromptListerController
from modules.app.business_prompt.infrastructure import BusinessPromptFinderController
from modules.app.business_prompt.infrastructure import BusinessPromptPatcherController

router = APIRouter()

@router.get("/business-prompt")
async def list_business_prompts(
    response: Response,
    db_session = Depends(get_session),
    current_user = Depends(require_permission("business_prompts:view:owner")),
):
    business_prompt_lister_controller = BusinessPromptListerController(session=db_session)
    controller_response, code = await business_prompt_lister_controller.list(user_id=UUID(current_user["sub"]))
    response.status_code = code
    return controller_response

@router.get("/business-prompt/context")
async def get_business_prompt_context(
    response: Response,
    db_session = Depends(get_session),
    current_user = Depends(require_permission("business_prompts:view:owner")),
):
    business_prompt_finder_controller = BusinessPromptFinderController(session=db_session)
    controller_response, code = await business_prompt_finder_controller.find(
        user_id=UUID(current_user["sub"]),
        key="context",
    )
    response.status_code = code
    return controller_response

@router.get("/business-prompt/greeting")
async def get_business_prompt_greeting(
    response: Response,
    db_session = Depends(get_session),
    current_user = Depends(require_permission("business_prompts:view:owner")),
):
    business_prompt_finder_controller = BusinessPromptFinderController(session=db_session)
    controller_response, code = await business_prompt_finder_controller.find(
        user_id=UUID(current_user["sub"]),
        key="greeting",
    )
    response.status_code = code
    return controller_response

@router.patch("/business-prompt/context")
async def patch_business_prompt_context(
    response: Response,
    payload: PatchBusinessPrompt,
    db_session = Depends(get_session),
    current_user = Depends(require_permission("business_prompts:patch:owner")),
):
    business_prompt_patcher_controller = BusinessPromptPatcherController(session=db_session)
    controller_response, code = await business_prompt_patcher_controller.patch(
        user_id=UUID(current_user["sub"]),
        key="context",
        data=payload.model_dump(),
    )
    response.status_code = code
    return controller_response

@router.patch("/business-prompt/greeting")
async def patch_business_prompt_greeting(
    response: Response,
    payload: PatchBusinessPrompt,
    db_session = Depends(get_session),
    current_user = Depends(require_permission("business_prompts:patch:owner")),
):
    business_prompt_patcher_controller = BusinessPromptPatcherController(session=db_session)
    controller_response, code = await business_prompt_patcher_controller.patch(
        user_id=UUID(current_user["sub"]),
        key="greeting",
        data=payload.model_dump(),
    )
    response.status_code = code
    return controller_response
