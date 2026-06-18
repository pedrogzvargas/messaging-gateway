from uuid import UUID
from typing import Optional
from datetime import datetime
from dataclasses import dataclass
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects import postgresql
from .mapper import metadata
from .mapper import mapper_registry


@dataclass
class WhatsappWebhookModel:
    id: UUID
    payload: dict
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

whatsapp_webhook_table = Table(
    "whatsapp_webhook",
    metadata,
    Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
    Column("payload", JSONB, nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False, default=func.now(), server_default=func.now()),
    Column(
        "updated_at",
        DateTime(timezone=True),
        nullable=False,
        default=func.now(),
        server_default=func.now(),
        onupdate=func.now(),
    ),
)

mapper_registry.map_imperatively(WhatsappWebhookModel, whatsapp_webhook_table)
