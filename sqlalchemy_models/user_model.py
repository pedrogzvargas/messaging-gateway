from uuid import UUID
from typing import Optional
from datetime import datetime
from dataclasses import dataclass
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import text
from sqlalchemy.sql import func
from sqlalchemy.dialects import postgresql
from .mapper import metadata
from .mapper import mapper_registry


@dataclass
class UserModel:
    id: UUID
    email: str
    password: str
    is_active: bool
    username: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

user_table = Table(
    "user",
    metadata,
    Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
    Column("email", String(254), nullable=False, unique=True),
    Column("username", String(100), nullable=True, unique=True),
    Column("password", String(200), nullable=False),
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

mapper_registry.map_imperatively(UserModel, user_table)
