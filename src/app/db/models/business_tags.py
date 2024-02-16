import uuid
from sqlalchemy import (
    ForeignKey,
    Index,
    String,
)
from sqlalchemy.orm import Mapped  # type: ignore
from sqlalchemy.orm import mapped_column
from sqlalchemy.dialects.postgresql import UUID
from src.app.db.models.base import Base


class BusinessTags(Base):
    __tablename__ = "business_tags"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tag: Mapped[str] = mapped_column(String(255), nullable=False)
    business_id = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("business.id", deferrable=True, initially="DEFERRED"),
        nullable=False,
    )


Index("business_tags_business_id_index", BusinessTags.business_id)
