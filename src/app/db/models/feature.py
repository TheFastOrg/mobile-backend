import uuid
from sqlalchemy import ForeignKey, String, UUID
from sqlalchemy.orm import Mapped  # type: ignore
from sqlalchemy.orm import mapped_column

from src.app.db.models.base import Base


class Feature(Base):
    __tablename__ = "feature"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ar_name: Mapped[str] = mapped_column(String(255), nullable=False)
    en_name: Mapped[str] = mapped_column(String(255), nullable=False)
    category_id = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("category.id", deferrable=True, initially="DEFERRED"),
        nullable=False,
    )
