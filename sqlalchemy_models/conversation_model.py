from uuid import UUID
from typing import Optional
from datetime import datetime
from dataclasses import dataclass
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.dialects import postgresql
from .mapper import metadata
from .mapper import mapper_registry


@dataclass
class ConversationModel:
    id: UUID
    channel_account_id: UUID
    contact_id: UUID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

conversation_table = Table(
    "conversation",
    metadata,
    Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
    Column("channel_account_id", postgresql.UUID(as_uuid=True), ForeignKey("channel_account.id", ondelete="RESTRICT"), nullable=False),
    Column("contact_id", postgresql.UUID(as_uuid=True), ForeignKey("contact.id", ondelete="RESTRICT"), nullable=False),
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

mapper_registry.map_imperatively(ConversationModel, conversation_table)
