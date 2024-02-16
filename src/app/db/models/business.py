import uuid
from sqlalchemy.dialects.postgresql import UUID
from typing import List

from geoalchemy2 import Geography
from sqlalchemy import (
    String,
)
from sqlalchemy.orm import Mapped  # type: ignore
from sqlalchemy.orm import mapped_column, relationship

from src.app.db.models.base import Base
from src.app.db.models.business_contacts import BusinessContacts
from src.app.db.models.business_tags import BusinessTags
from src.app.db.models.business_working_hours import BusinessWorkingHours
from src.app.db.models.category import Category
from src.app.db.models.feature import Feature


class Business(Base):
    __tablename__ = "business"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
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
    working_hours: Mapped[List["BusinessWorkingHours"]] = relationship()
    business_contacts: Mapped[List["BusinessContacts"]] = relationship()
    tags: Mapped[List["BusinessTags"]] = relationship()
    categories: Mapped[List["Category"]] = relationship(
        "Category", secondary="business_categories"
    )
    features: Mapped[List["Feature"]] = relationship(
        "Feature", secondary="business_features"
    )
