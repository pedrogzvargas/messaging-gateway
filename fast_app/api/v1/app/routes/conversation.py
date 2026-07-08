from uuid import UUID
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Response
from typing import Annotated
from fast_app.core.db_session import get_session
from fast_app.api.v1.app.schemas import ConversationQueryParams
from modules.app.conversation.infrastructure import ConversationSearcherController
from modules.app.conversation.infrastructure import ConversationFinderController

router = APIRouter()

@router.get("/conversation")
async def list_conversations(
    response: Response,
    query_params: Annotated[ConversationQueryParams, Depends()],
    db_session = Depends(get_session),
    # dependencies = (Depends(require_permission("customer:list"))),
):
    query_params = query_params.model_dump(exclude_none=True)
    conversation_searcher_controller = ConversationSearcherController(session=db_session)
    controller_response, code = await conversation_searcher_controller.search(query_params=query_params)
    response.status_code = code
    return controller_response

@router.get("/conversation/{conversation_id}")
async def get_conversation(
    response: Response,
    conversation_id: UUID,
    db_session = Depends(get_session),
    # dependencies = (Depends(require_permission("customer:list"))),
):
    conversation_finder_controller = ConversationFinderController(session=db_session)
    controller_response, code = await conversation_finder_controller.find(conversation_id=conversation_id)
    response.status_code = code
    return controller_response
