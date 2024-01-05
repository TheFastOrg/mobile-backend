from typing import List, Any

from geoalchemy2 import Geography
from sqlalchemy import (
    Integer,
    String,
)
from sqlalchemy.orm import Mapped  # type: ignore
from sqlalchemy.orm import mapped_column, relationship

from src.app.db.models import Base


class Business(Base):
    __tablename__ = "business"

    id: Mapped[Integer] = mapped_column(Integer, primary_key=True, autoincrement=True)
    location: Mapped[Geography] = mapped_column(
        Geography(geometry_type="POINT", srid=4326), nullable=False
    )
    address_line1: Mapped[str] = mapped_column(String(255))
    address_line2: Mapped[str] = mapped_column(String(255))
    ar_name: Mapped[str] = mapped_column(String(255), nullable=False)
    city: Mapped[str] = mapped_column(String(255))
    country: Mapped[str] = mapped_column(String(255), nullable=False)
    en_name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    status: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[str] = mapped_column(String(255), nullable=False)

    # using Any to avoid circular import
    # (alternative: move `BusinessWorkingHours` to `Business.py`)
    business_working_hours: Mapped[List[Any]] = relationship(
        "BusinessWorkingHours", back_populates="business"
    )

    def __repr__(self):
        return f"Business: {self.en_name}"
