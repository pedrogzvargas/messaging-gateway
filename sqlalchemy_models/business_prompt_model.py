from uuid import UUID
from typing import Optional
from datetime import datetime
from dataclasses import dataclass
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import Boolean
from sqlalchemy import ForeignKey
from sqlalchemy import text
from sqlalchemy.sql import func
from sqlalchemy.dialects import postgresql
from .mapper import metadata
from .mapper import mapper_registry


@dataclass
class BusinessPromptModel:
    id: UUID
    business_id: UUID
    key: str
    description: str
    content: str
    role: str
    is_active: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

business_prompt_table = Table(
    "business_prompt",
    metadata,
    Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
    Column("business_id", postgresql.UUID(as_uuid=True), ForeignKey("business.id", ondelete="RESTRICT"), nullable=True),
    Column("key", String(100), nullable=False),
    Column("description", Text, nullable=False),
    Column("content", Text, nullable=False),
    Column("role", String(50), nullable=False),
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

mapper_registry.map_imperatively(BusinessPromptModel, business_prompt_table)
