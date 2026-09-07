from uuid import UUID
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Response
from fast_app.core.db_session import get_session
from fast_app.api.v1.app.schemas import NotificationSubscription
from fast_app.api.v1.app.schemas import PatchNotificationSubscription
from modules.app.notification_subscription.infrastructure import NotificationSubscriptionCreatorController
from modules.app.notification_subscription.infrastructure import NotificationSubscriptionFinderController
from modules.app.notification_subscription.infrastructure import NotificationSubscriptionPatcherController
from fast_app.core.auth import require_permission

router = APIRouter()

@router.get("/notification-subscription")
async def get_notification_subscription(
    response: Response,
    db_session = Depends(get_session),
    current_user = Depends(require_permission("notification_subscriptions:view:owner")),
):
    notification_subscription_finder_controller = NotificationSubscriptionFinderController(session=db_session)
    controller_response, code = await notification_subscription_finder_controller.find(
        session_id=UUID(current_user.get("session_id")),
    )
    response.status_code = code
    return controller_response

@router.patch("/notification-subscription")
async def patch_notification_subscription(
    response: Response,
    payload: PatchNotificationSubscription,
    db_session = Depends(get_session),
    current_user = Depends(require_permission("notification_subscriptions:patch:owner")),
):
    notification_subscription_patcher_controller = NotificationSubscriptionPatcherController(session=db_session)
    controller_response, code = await notification_subscription_patcher_controller.patch(
        session_id=UUID(current_user.get("session_id")),
        data=payload.model_dump(),
    )
    response.status_code = code
    return controller_response

@router.post("/notification-subscription")
async def create_notification_subscription(
    response: Response,
    payload: NotificationSubscription,
    db_session = Depends(get_session),
    current_user = Depends(require_permission("notification_subscriptions:create:owner")),
):
    notification_subscription_creator_controller = NotificationSubscriptionCreatorController(session=db_session)
    body = payload.model_dump()
    controller_response, code = await notification_subscription_creator_controller.create(
        id=body.get("id"),
        session_id=UUID(current_user.get("session_id")),
        payload=body.get("payload"),
    )
    response.status_code = code
    return controller_response
