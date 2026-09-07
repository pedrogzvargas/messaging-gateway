from uuid import UUID
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Response
from typing import Annotated
from fast_app.core.db_session import get_session
from fast_app.api.v1.app.schemas import CustomerNotificationQueryParams
from modules.app.customer_notification.infrastructure import CustomerNotificationSearcherController
from fast_app.core.auth import require_permission

router = APIRouter()

@router.get("/customer-notification")
async def list_customer_notifications(
    response: Response,
    query_params: Annotated[CustomerNotificationQueryParams, Depends()],
    db_session = Depends(get_session),
    current_user = Depends(require_permission("customer_notifications:view:owner")),
):
    query_params = query_params.model_dump(exclude_none=True)
    customer_notification_searcher_controller = CustomerNotificationSearcherController(session=db_session)
    controller_response, code = await customer_notification_searcher_controller.search(
        query_params=query_params,
        user_id=UUID(current_user["sub"]),
    )
    response.status_code = code
    return controller_response
