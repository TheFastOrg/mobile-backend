
from sqlalchemy import (
    Boolean,
    DateTime,
)
from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    __abstract__ = True

    created_at = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = mapped_column(DateTime(timezone=True), default=None, nullable=True)
    deleted_at = mapped_column(DateTime(timezone=True), nullable=True, default=None)
    is_deleted = mapped_column(Boolean, nullable=False, default=False)
