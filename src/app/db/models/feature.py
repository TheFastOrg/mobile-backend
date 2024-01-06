from sqlalchemy import (
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped  # type: ignore
from sqlalchemy.orm import mapped_column

from src.app.db.models.base import Base


class Feature(Base):
    __tablename__ = "feature"

    id: Mapped[Integer] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ar_name: Mapped[str] = mapped_column(String(255), nullable=False)
    en_name: Mapped[str] = mapped_column(String(255), nullable=False)
    category_id: Mapped[Integer] = mapped_column(
        Integer,
        ForeignKey("category.id", deferrable=True, initially="DEFERRED"),
        nullable=False,
    )
