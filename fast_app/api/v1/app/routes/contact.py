from uuid import UUID
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Response
from typing import Annotated
from fast_app.core.db_session import get_session
from fast_app.api.v1.app.schemas import ContactQueryParams
from modules.app.contact.infrastructure import ContactSearcherController

router = APIRouter()

@router.get("/contact")
async def list_contacts(
    response: Response,
    query_params: Annotated[ContactQueryParams, Depends()],
    db_session = Depends(get_session),
    # dependencies = (Depends(require_permission("customer:list"))),
):
    query_params = query_params.model_dump(exclude_none=True)
    contact_searcher_controller = ContactSearcherController(session=db_session)
    controller_response, code = await contact_searcher_controller.search(query_params=query_params)
    response.status_code = code
    return controller_response

