from uuid import UUID
from typing import Optional
from datetime import datetime
from dataclasses import dataclass
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import TIMESTAMP
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from sqlalchemy.dialects import postgresql
from .mapper import metadata
from .mapper import mapper_registry


@dataclass
class WhatsappMessageModel:
    id: UUID
    conversation_id: UUID
    role: str
    wa_message_id: str
    from_number: str
    to_number: str
    message_type: str
    message_text: str
    direction: str
    timestamp: TIMESTAMP
    raw_payload: JSONB
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

whatsapp_message_table = Table(
    "whatsapp_message",
    metadata,
    Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
    Column("conversation_id", postgresql.UUID(as_uuid=True), ForeignKey("whatsapp_conversation.id", ondelete="RESTRICT"), nullable=False),
    Column("role", String(50), nullable=False),
    Column("wa_message_id", String(255), nullable=False),
    Column("from_number", String(20), nullable=False),
    Column("to_number", String(20), nullable=False),
    Column("message_type", String(50), nullable=False),
    Column("message_text", Text, nullable=False),
    Column("direction", String(10), nullable=False),
    Column("timestamp", TIMESTAMP, nullable=False),
    Column("raw_payload", JSONB, nullable=False),
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

mapper_registry.map_imperatively(WhatsappMessageModel, whatsapp_message_table)
