from uuid import UUID
from typing import Optional
from datetime import datetime
from dataclasses import dataclass
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import BigInteger
from sqlalchemy.sql import func
from sqlalchemy.dialects import postgresql
from .mapper import metadata
from .mapper import mapper_registry


@dataclass
class TokenUsageModel:
    id: UUID
    customer_id: UUID
    customer_plan_id: UUID
    input_tokens: int
    output_tokens: int
    total_tokens: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

token_usage_table = Table(
    "token_usage",
    metadata,
    Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
    Column("customer_id", postgresql.UUID(as_uuid=True), ForeignKey("customer.id", ondelete="RESTRICT"), nullable=False),
    Column("plan_id", postgresql.UUID(as_uuid=True), ForeignKey("plan.id", ondelete="RESTRICT"), nullable=False),
    Column("input_tokens", BigInteger, nullable=False),
    Column("output_tokens", BigInteger, nullable=False),
    Column("total_tokens", BigInteger, nullable=False),
    Column("ended_at", DateTime(timezone=True), nullable=False),
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

mapper_registry.map_imperatively(TokenUsageModel, token_usage_table)
