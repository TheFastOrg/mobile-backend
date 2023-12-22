from typing import List

from geoalchemy2 import Geography
from sqlalchemy import Boolean, DateTime, ForeignKey, Index, Integer, String, Time
from sqlalchemy.orm import Mapped  # type: ignore
from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship, validates
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    __abstract__ = True

    created_at = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = mapped_column(DateTime(timezone=True), default=None, nullable=True)
    deleted_at = mapped_column(DateTime(timezone=True), nullable=True, default=None)
    is_deleted = mapped_column(Boolean, nullable=False, default=False)


class Business(Base):
    __tablename__ = "business"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    location = mapped_column(
        Geography(geometry_type="POINT", srid=4326), nullable=False
    )
    address_line1: Mapped[str] = mapped_column(String(255))
    address_line2: Mapped[str] = mapped_column(String(255))
    ar_name: Mapped[str] = mapped_column(String(255), nullable=False)
    city: Mapped[str] = mapped_column(String(255))
    country: Mapped[str] = mapped_column(String(255), nullable=False)
    en_name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug = mapped_column(String(255), nullable=False, unique=True)
    status = mapped_column(String(255), nullable=False)
    type = mapped_column(String(255), nullable=False)
    business_working_hours: Mapped[List["BusinessWorkingHours"]] = relationship(
        "BusinessWorkingHours", back_populates="business"
    )

    # Validation example (you can add more validation as needed)
    @validates("status", "type")
    def validate_status_type(self, key, value):
        # Example: Ensure that 'status' and 'type' are not empty
        if not value or not value.strip():
            raise ValueError(f"{key} cannot be empty")
        return value

    def __repr__(self):
        return f"Business: {self.en_name}"


# Index creation
ba7besh_business_location_index = Index(
    "ba7besh_business_location_fc3ec09e_id", Business.location
)
ba7besh_business_slug_index = Index(
    "ba7besh_business_slug_ce0fd4e6_like", Business.slug
)


class BusinessWorkingHours(Base):
    __tablename__ = "business_working_hours"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    business_id = mapped_column(
        Integer, ForeignKey("business.id", ondelete="CASCADE"), nullable=False
    )
    day = mapped_column(Integer, nullable=False)  # Starting from 1 = Monday
    opening_time = mapped_column(Time, nullable=False)
    closing_time = mapped_column(Time, nullable=False)
    business: Mapped["Business"] = relationship(
        "Business", back_populates="business_working_hours"
    )


class BusinessContacts(Base):
    __tablename__ = "business_contacts"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    business_id = mapped_column(
        Integer, ForeignKey("business.id", ondelete="CASCADE"), nullable=False
    )
    contact_type = mapped_column(String(15), nullable=False)
    contact_value = mapped_column(String(255), nullable=False)


class Category(Base):
    __tablename__ = "category"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    slug = mapped_column(String(255), unique=True, nullable=False)
    ar_name = mapped_column(String(255))
    en_name = mapped_column(String(255))
    parent_id = mapped_column(Integer, ForeignKey("category.id", ondelete="SET NULL"))


class BusinessCategories(Base):
    __tablename__ = "business_categories"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    business_id = mapped_column(
        Integer, ForeignKey("business.id", ondelete="CASCADE"), nullable=False
    )
    category_id = mapped_column(
        Integer, ForeignKey("category.id", ondelete="PROTECT"), nullable=False
    )


class Feature(Base):
    __tablename__ = "feature"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    category_id = mapped_column(
        Integer, ForeignKey("category.id", ondelete="CASCADE"), nullable=False
    )
    ar_name = mapped_column(String(255), nullable=False)
    en_name = mapped_column(String(255), nullable=False)


class BusinessFeatures(Base):
    __tablename__ = "business_features"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    business_id = mapped_column(
        Integer, ForeignKey("business.id", ondelete="CASCADE"), nullable=False
    )
    feature_id = mapped_column(
        Integer, ForeignKey("feature.id", ondelete="PROTECT"), nullable=False
    )


class BusinessTags(Base):
    __tablename__ = "business_tags"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    business_id = mapped_column(
        Integer, ForeignKey("business.id", ondelete="CASCADE"), nullable=False
    )
    tag = mapped_column(String(255), nullable=False)


class FeaturesCategory(Base):
    __tablename__ = "features_category"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    ar_name = mapped_column(String(255), nullable=False)
    en_name = mapped_column(String(255), nullable=False)
