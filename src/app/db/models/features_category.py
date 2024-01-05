
from sqlalchemy import (
    Integer,
    String,
)
from sqlalchemy.orm import Mapped  # type: ignore
from sqlalchemy.orm import mapped_column

from src.app.db.models import Base


class FeaturesCategory(Base):
    __tablename__ = "features_category"

    id: Mapped[Integer] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ar_name: Mapped[str] = mapped_column(String(255), nullable=False)
    en_name: Mapped[str] = mapped_column(String(255), nullable=False)
