from fastapi import APIRouter
from pywebpush import webpush

router = APIRouter()
subscription = None

@router.post("/subscribe")
async def subscribe(data: dict):
    global subscription
    subscription = data
    print(subscription)
    return {"ok": True}

@router.post("/push-notification")
async def send():
    webpush(
        subscription_info=subscription,
        data='{"title":"Hola","body":"El usuario X ha agendado una cita para el día 27/09/2026"}',
        vapid_private_key="vEaALRD6cQtWl2smxlByH-p6bXiyCTF-mMe0xFzY5mg",
        vapid_claims={
            "sub": "mailto:test@test.com"
        },
    )

    return {"sent": True}
