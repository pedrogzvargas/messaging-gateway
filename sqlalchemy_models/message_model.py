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
class MessageModel:
    id: UUID
    conversation_id: UUID
    role: str
    message_id: str
    message_type: str
    message: str
    direction: str
    timestamp: TIMESTAMP
    payload: JSONB
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

message_table = Table(
    "message",
    metadata,
    Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
    Column("conversation_id", postgresql.UUID(as_uuid=True), ForeignKey("conversation.id", ondelete="RESTRICT"), nullable=False),
    Column("role", String(50), nullable=False),
    Column("message_id", String(255), nullable=False),
    Column("message_type", String(50), nullable=False),
    Column("message", Text, nullable=False),
    Column("direction", String(10), nullable=False),
    Column("timestamp", TIMESTAMP, nullable=False),
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

mapper_registry.map_imperatively(MessageModel, message_table)
