from uuid import UUID
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Response
from typing import Annotated
from fast_app.core.db_session import get_session
from fast_app.api.v1.app.schemas import ChannelAccountQueryParams
from modules.app.channel_account.infrastructure import ChannelAccountSearcherController

router = APIRouter()

@router.get("/channel-account")
async def list_channel_accounts(
    response: Response,
    query_params: Annotated[ChannelAccountQueryParams, Depends()],
    db_session = Depends(get_session),
    # dependencies = (Depends(require_permission("customer:list"))),
):
    query_params = query_params.model_dump(exclude_none=True)
    channel_account_searcher_controller = ChannelAccountSearcherController(session=db_session)
    controller_response, code = await channel_account_searcher_controller.search(query_params=query_params)
    response.status_code = code
    return controller_response

# @router.get("/channel-account/{channel_account_id}")
# async def get_conversation(
#     response: Response,
#     conversation_id: UUID,
#     db_session = Depends(get_session),
#     # dependencies = (Depends(require_permission("customer:list"))),
# ):
#     conversation_finder_controller = ConversationFinderController(session=db_session)
#     controller_response, code = await conversation_finder_controller.find(conversation_id=conversation_id)
#     response.status_code = code
#     return controller_response
