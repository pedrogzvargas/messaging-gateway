from uuid import UUID
from fastapi import APIRouter
from fastapi import Response
from fastapi import Depends
from fastapi.responses import JSONResponse
from fast_app.core.db_session import get_session
from fast_app.core.auth import require_permission
from fast_app.api.v1.app.schemas import MeResponse
from fast_app.api.v1.app.schemas import PatchCustomer
from modules.shared.http.domain import status
from modules.shared.http.infrastructure import ErrorResponse
from modules.app.customer.infrastructure import CustomerFinderController
from modules.app.customer.infrastructure import CustomerPatcherController

router = APIRouter()

@router.get(
    "/me",
    response_model=MeResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse},
    },
)
async def get_me(
    response: Response,
    db_session = Depends(get_session),
    current_user = Depends(require_permission("faqs:view:owner"))
):
    customer_finder_controller = CustomerFinderController(session=db_session)
    controller_response, code = await customer_finder_controller.find(
        customer_id=UUID(current_user["sub"]),
    )

    if code != status.HTTP_200_OK:
        return JSONResponse(status_code=code, content=controller_response)

    response.status_code = code
    return controller_response

@router.patch(
    "/me",
    response_model=MeResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse},
    },
)
async def patch_me(
    response: Response,
    payload: PatchCustomer,
    db_session = Depends(get_session),
    current_user = Depends(require_permission("customers:patch:owner"))
):
    customer_patcher_controller = CustomerPatcherController(session=db_session)
    controller_response, code = await customer_patcher_controller.patch(
        customer_id=UUID(current_user["sub"]),
        data=payload.model_dump(),
    )

    if code != status.HTTP_200_OK:
        return JSONResponse(status_code=code, content=controller_response)

    response.status_code = code
    return controller_response
