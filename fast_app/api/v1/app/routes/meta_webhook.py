from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter
from fastapi import Request
from fastapi import Query
from fastapi import HTTPException
from fastapi import Depends
from fastapi import Response
from fastapi.responses import PlainTextResponse
from fast_app.core.config import get_settings
from fast_app.core.db_session import get_session
from modules.app.webhook_event.infrastructure import WebhookEventCreatorController

router = APIRouter()

@router.get("/meta/webhook")
async def verify_webhook(
    hub_mode: str = Query(alias="hub.mode"),
    hub_verify_token: str = Query(alias="hub.verify_token"),
    hub_challenge: str = Query(alias="hub.challenge"),
):
    settings = get_settings()
    if hub_mode == "subscribe" and hub_verify_token == settings.wa_verify_token:
        return PlainTextResponse(content=hub_challenge)

    raise HTTPException(status_code=403)

@router.post("/meta/webhook/{provider_id}")
async def receive_webhook(request: Request, response: Response, provider_id: str, session: AsyncSession = Depends(get_session)):
    payload = await request.json()

    container = request.app.state.container
    webhook_event_creator_controller = WebhookEventCreatorController(
        session=session,
        event_bus=container.event_bus,
    )
    provider = payload.get("entry", [])[0].get("changes", [])[0].get("value", {}).get("messaging_product", "")
    controller_response, code = await webhook_event_creator_controller.create(
        id=uuid4(),
        provider=provider,
        provider_id=provider_id,
        payload=payload,
    )
    response.status_code = code

    return controller_response
