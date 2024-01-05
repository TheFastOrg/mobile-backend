
from sqlalchemy import (
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped  # type: ignore
from sqlalchemy.orm import mapped_column

from src.app.db.models import Base


class Category(Base):
    __tablename__ = "category"

    id: Mapped[Integer] = mapped_column(Integer, primary_key=True, autoincrement=True)
    slug = mapped_column(String(255), unique=True, nullable=False)
    ar_name: Mapped[str] = mapped_column(String(255))
    en_name: Mapped[str] = mapped_column(String(255))
    parent_id: Mapped[Integer] = mapped_column(
        Integer, ForeignKey("category.id"), nullable=True
    )
