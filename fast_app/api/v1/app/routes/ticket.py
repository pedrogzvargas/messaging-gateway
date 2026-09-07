from uuid import UUID
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Response
from typing import Annotated
from fast_app.core.db_session import get_session
from fast_app.api.v1.app.schemas import TicketQueryParams
from fast_app.api.v1.app.schemas import Ticket
from modules.app.ticket.infrastructure import TicketSearcherController
from modules.app.ticket.infrastructure import TicketCreatorController
from modules.app.ticket.infrastructure import TicketFinderController
from modules.app.ticket.infrastructure import TicketCloserController
from fast_app.core.auth import require_permission

router = APIRouter()

@router.get("/ticket")
async def list_tickets(
    response: Response,
    query_params: Annotated[TicketQueryParams, Depends()],
    db_session = Depends(get_session),
    current_user = Depends(require_permission("tickets:view:owner")),
):
    query_params = query_params.model_dump(exclude_none=True)
    ticket_searcher_controller = TicketSearcherController(session=db_session)
    controller_response, code = await ticket_searcher_controller.search(
        query_params=query_params,
        user_id=UUID(current_user["sub"]),
    )
    response.status_code = code
    return controller_response

@router.post("/ticket")
async def create_ticket(
    response: Response,
    payload: Ticket,
    db_session = Depends(get_session),
    current_user = Depends(require_permission("tickets:create:owner")),
):
    ticket_creator_controller = TicketCreatorController(session=db_session)
    body = payload.model_dump()
    controller_response, code = await ticket_creator_controller.create(
        id=body.get("id"),
        customer_id=UUID(current_user.get("sub")),
        details=body.get("details"),
    )
    response.status_code = code
    return controller_response

@router.get("/ticket/{ticket_id}")
async def get_ticket(
    response: Response,
    ticket_id: UUID,
    db_session = Depends(get_session),
    current_user = Depends(require_permission("tickets:view:owner")),
):
    ticket_finder_controller = TicketFinderController(session=db_session)
    controller_response, code = await ticket_finder_controller.find(
        ticket_id=ticket_id,
        user_id=UUID(current_user["sub"]),
    )
    response.status_code = code
    return controller_response

@router.patch("/ticket/{ticket_id}/close")
async def close_ticket(
    response: Response,
    ticket_id: UUID,
    db_session = Depends(get_session),
    current_user = Depends(require_permission("tickets:close:owner")),
):
    ticket_closer_controller = TicketCloserController(session=db_session)
    controller_response, code = await ticket_closer_controller.close(
        ticket_id=ticket_id,
        user_id=UUID(current_user["sub"]),
    )
    response.status_code = code
    return controller_response
