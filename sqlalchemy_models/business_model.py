from uuid import UUID
from typing import Optional
from datetime import datetime
from dataclasses import dataclass
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.dialects import postgresql
from .mapper import metadata
from .mapper import mapper_registry


@dataclass
class BusinessModel:
    id: UUID
    customer_id: UUID
    name: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

business_table = Table(
    "business",
    metadata,
    Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
    Column("customer_id", postgresql.UUID(as_uuid=True), ForeignKey("customer.id", ondelete="RESTRICT"), nullable=False),
    Column("name", String(255), nullable=False),
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

mapper_registry.map_imperatively(BusinessModel, business_table)
