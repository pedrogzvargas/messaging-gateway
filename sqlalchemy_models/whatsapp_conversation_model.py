from uuid import UUID
from typing import Optional
from datetime import datetime
from dataclasses import dataclass
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy.sql import func
from sqlalchemy.dialects import postgresql
from .mapper import metadata
from .mapper import mapper_registry


@dataclass
class WhatsappConversationModel:
    id: UUID
    phone_number: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

whatsapp_conversation_table = Table(
    "whatsapp_conversation",
    metadata,
    Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
    Column("phone_number", String(20), nullable=False),
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

mapper_registry.map_imperatively(WhatsappConversationModel, whatsapp_conversation_table)
