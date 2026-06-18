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
from modules.whatsapp_webhook.infrastructure import WhatsappWebhookCreatorController

router = APIRouter()

@router.get("/whatsapp/webhook")
async def verify_webhook(
    hub_mode: str = Query(alias="hub.mode"),
    hub_verify_token: str = Query(alias="hub.verify_token"),
    hub_challenge: str = Query(alias="hub.challenge"),
):
    settings = get_settings()
    if hub_mode == "subscribe" and hub_verify_token == settings.wa_verify_token:
        return PlainTextResponse(content=hub_challenge)

    raise HTTPException(status_code=403)

@router.post("/whatsapp/webhook")
async def receive_webhook(request: Request, response: Response, session: AsyncSession = Depends(get_session)):
    payload = await request.json()

    container = request.app.state.container
    whatsapp_webhook_creator_controller = WhatsappWebhookCreatorController(
        session=session,
        event_bus=container.event_bus,
    )
    controller_response, code = await whatsapp_webhook_creator_controller.create(payload)
    response.status_code = code

    return controller_response
