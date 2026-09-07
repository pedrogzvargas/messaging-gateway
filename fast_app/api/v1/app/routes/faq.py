from uuid import UUID
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Response
from fastapi import Request
from typing import Annotated
from fast_app.core.db_session import get_session
from fast_app.api.v1.app.schemas import FaqQueryParams
from fast_app.api.v1.app.schemas import Faq
from fast_app.api.v1.app.schemas import PatchFaq
from modules.app.faq.infrastructure import FaqSearcherController
from modules.app.faq.infrastructure import FaqCreatorController
from modules.app.faq.infrastructure import FaqPatcherController
from fast_app.core.auth import require_permission

router = APIRouter()

@router.get("/faq")
async def list_faqs(
    response: Response,
    query_params: Annotated[FaqQueryParams, Depends()],
    db_session = Depends(get_session),
    current_user = Depends(require_permission("faqs:view:owner")),
):
    query_params = query_params.model_dump(exclude_none=True)
    faq_searcher_controller = FaqSearcherController(session=db_session)
    controller_response, code = await faq_searcher_controller.search(
        query_params=query_params,
        user_id=UUID(current_user["sub"]),
    )
    response.status_code = code
    return controller_response

@router.post("/faq")
async def create_faq(
    request: Request,
    response: Response,
    payload: Faq,
    db_session = Depends(get_session),
    current_user = Depends(require_permission("faqs:create:owner")),
):
    container = request.app.state.container
    faq_creator_controller = FaqCreatorController(
        session=db_session,
        event_bus=container.event_bus,
    )
    body = payload.model_dump()
    controller_response, code = await faq_creator_controller.create(
        id=body.get("id"),
        customer_id=UUID(current_user.get("sub")),
        question=body.get("question"),
        answer=body.get("answer"),
        is_active=body.get("is_active"),
    )
    response.status_code = code
    return controller_response

@router.patch("/faq/{faq_id}")
async def patch_faq(
    request: Request,
    response: Response,
    faq_id: UUID,
    payload: PatchFaq,
    db_session = Depends(get_session),
    current_user = Depends(require_permission("faqs:patch:owner")),
):
    container = request.app.state.container
    faq_patcher_controller = FaqPatcherController(
        session=db_session,
        event_bus=container.event_bus,
    )
    body = payload.model_dump()
    controller_response, code = await faq_patcher_controller.patch(
        faq_id=faq_id,
        customer_id=UUID(current_user.get("sub")),
        data=body,
    )
    response.status_code = code
    return controller_response
