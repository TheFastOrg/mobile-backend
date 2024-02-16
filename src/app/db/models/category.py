import uuid
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy import (
    ForeignKey,
    String,
)
from sqlalchemy.orm import Mapped  # type: ignore
from sqlalchemy.orm import mapped_column

from src.app.db.models.base import Base


class Category(Base):
    __tablename__ = "category"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    slug = mapped_column(String(255), unique=True, nullable=False)
    ar_name: Mapped[str] = mapped_column(String(255))
    en_name: Mapped[str] = mapped_column(String(255))
    parent_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("category.id"), nullable=True
    )
