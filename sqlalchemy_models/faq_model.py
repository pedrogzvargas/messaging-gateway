from uuid import UUID
from typing import Optional
from datetime import datetime
from dataclasses import dataclass
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Text
from sqlalchemy import ForeignKey
from sqlalchemy import Boolean
from sqlalchemy import text
from pgvector.sqlalchemy import Vector
from sqlalchemy.sql import func
from sqlalchemy.dialects import postgresql
from .mapper import metadata
from .mapper import mapper_registry


@dataclass
class FAQModel:
    id: UUID
    business_id: UUID
    question: str
    answer: str
    embedding: list[float]
    is_active: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

faq_table = Table(
    "faq",
    metadata,
    Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
    Column("business_id", postgresql.UUID(as_uuid=True), ForeignKey("business.id", ondelete="RESTRICT"), nullable=True),
    Column("question", Text, nullable=False),
    Column("answer", Text, nullable=False),
    Column("embedding", Vector(1536), nullable=False),
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

mapper_registry.map_imperatively(FAQModel, faq_table)
