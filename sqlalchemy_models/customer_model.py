from uuid import UUID
from typing import Optional
from datetime import datetime
from dataclasses import dataclass
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.dialects import postgresql
from .mapper import metadata
from .mapper import mapper_registry


@dataclass
class CustomerModel:

    id: UUID
    user_id: UUID
    name: str
    last_name: str
    second_last_name: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


customer_table = Table(
    "customer",
    metadata,
    Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
    Column("user_id", postgresql.UUID(as_uuid=True), ForeignKey("user.id", ondelete="RESTRICT"), nullable=False),
    Column("name", String(100), nullable=False),
    Column("last_name", String(100), nullable=False),
    Column("second_last_name", String(100), nullable=True),
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

mapper_registry.map_imperatively(CustomerModel, customer_table)
