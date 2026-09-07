from uuid import UUID
from typing import Optional
from datetime import datetime
from dataclasses import dataclass
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.dialects import postgresql
from .mapper import metadata
from .mapper import mapper_registry


@dataclass
class TicketModel:
    id: UUID
    details: str
    status: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

ticket_table = Table(
    "ticket",
    metadata,
    Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
    Column("customer_id", postgresql.UUID(as_uuid=True), ForeignKey("customer.id", ondelete="RESTRICT"), nullable=True),
    Column("details", Text, nullable=False),
    Column("status", String(50), nullable=False),
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

mapper_registry.map_imperatively(TicketModel, ticket_table)
