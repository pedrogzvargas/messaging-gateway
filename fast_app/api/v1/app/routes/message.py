from uuid import UUID
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Response
from typing import Annotated
from fast_app.core.db_session import get_session
from fast_app.api.v1.app.schemas import MessageQueryParams
from modules.app.message.infrastructure import ConversationMessageFinderController

router = APIRouter()

@router.get("/conversation/{conversation_id}/message")
async def list_conversation_messages(
    response: Response,
    conversation_id: UUID,
    query_params: Annotated[MessageQueryParams, Depends()],
    db_session = Depends(get_session),
):
    query_params = query_params.model_dump(exclude_none=True)
    conversation_message_finder_controller = ConversationMessageFinderController(session=db_session)
    controller_response, code = await conversation_message_finder_controller.find(
        conversation_id=conversation_id,
        **query_params,
    )
    response.status_code = code
    return controller_response
