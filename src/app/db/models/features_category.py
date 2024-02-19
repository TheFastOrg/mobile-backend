import uuid
from sqlalchemy import String, UUID
from sqlalchemy.orm import Mapped  # type: ignore
from sqlalchemy.orm import mapped_column

from src.app.db.models.base import Base


class FeaturesCategory(Base):
    __tablename__ = "features_category"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ar_name: Mapped[str] = mapped_column(String(255), nullable=False)
    en_name: Mapped[str] = mapped_column(String(255), nullable=False)
