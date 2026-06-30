from uuid import UUID
from typing import Optional
from datetime import datetime
from dataclasses import dataclass
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import text
from sqlalchemy.sql import func
from sqlalchemy.dialects import postgresql
from .mapper import metadata
from .mapper import mapper_registry


@dataclass
class ChannelModel:
    id: UUID
    name: str
    is_active: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

channel_table = Table(
    "channel",
    metadata,
    Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
    Column("name", String(100), nullable=False),
    Column("is_active", Boolean(), default=True, server_default=text("true"), nullable=False),
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

mapper_registry.map_imperatively(ChannelModel, channel_table)
