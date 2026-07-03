from uuid import UUID
from typing import Optional
from datetime import datetime
from dataclasses import dataclass
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import text
from sqlalchemy.sql import func
from sqlalchemy.dialects import postgresql
from .mapper import metadata
from .mapper import mapper_registry


@dataclass
class RolePermissionModel:
    id: UUID
    role_id: UUID
    permission_id: UUID
    is_active: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

role_permission_table = Table(
    "role_permission",
    metadata,
    Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
    Column("role_id", postgresql.UUID(as_uuid=True), ForeignKey("role.id", ondelete="RESTRICT"), nullable=False),
    Column("permission_id", postgresql.UUID(as_uuid=True), ForeignKey("permission.id", ondelete="RESTRICT"), nullable=False),
    Column("is_active", Boolean(), default=False, server_default=text("true"), nullable=False),
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

mapper_registry.map_imperatively(RolePermissionModel, role_permission_table)
