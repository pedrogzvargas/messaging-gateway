from uuid import UUID
from typing import Optional
from datetime import datetime
from dataclasses import dataclass
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects import postgresql
from .mapper import metadata
from .mapper import mapper_registry


@dataclass
class WebhookEventModel:
    id: UUID
    provider: str
    provider_id: str
    payload: dict
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

webhook_event_table = Table(
    "webhook_event",
    metadata,
    Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
    Column("provider", String(50), nullable=False),
    Column("provider_id", String(100), nullable=False),
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

mapper_registry.map_imperatively(WebhookEventModel, webhook_event_table)
