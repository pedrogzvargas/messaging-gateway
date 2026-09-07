from uuid import UUID
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Response
from fast_app.core.db_session import get_session
from fast_app.core.auth import require_permission
from modules.app.dashboard.infrastructure import DashboardSummaryFinderController

router = APIRouter()

@router.get("/dashboard/summary")
async def get_dashboard_summary(
    response: Response,
    db_session = Depends(get_session),
    current_user = Depends(require_permission("dashboard:view:owner")),
):
    dashboard_summary_finder_controller = DashboardSummaryFinderController(session=db_session)
    controller_response, code = await dashboard_summary_finder_controller.find(
        user_id=UUID(current_user["sub"]),
    )
    response.status_code = code
    return controller_response
