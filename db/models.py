from geoalchemy2 import Geography
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Time,
)
from sqlalchemy.dialects.postgresql import BOOLEAN, TIMESTAMP
from sqlalchemy.orm import Mapped, validates, DeclarativeBase, mapped_column
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    __abstract__ = True

    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(DateTime(timezone=True), default=None, nullable=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True, default=None)
    is_deleted = Column(Boolean, nullable=False, default=False)


class Ba7beshBusiness(Base):
    __tablename__ = "ba7besh_business"

    id = Column(Integer, primary_key=True, autoincrement=True)
    location = Column(Geography(geometry_type="POINT", srid=4326), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True))
    address_line1: Mapped[str] = mapped_column(String(255))
    address_line2: Mapped[str] = mapped_column(String(255))
    ar_name = Column(String(255), nullable=False)
    city: Mapped[str] = mapped_column(String(255))
    country: Mapped[str] = mapped_column(String(255), nullable=False)
    en_name = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False, unique=True)
    status = Column(String(255), nullable=False)
    type = Column(String(255), nullable=False)

    # Validation example (you can add more validation as needed)
    @validates("status", "type")
    def validate_status_type(self, key, value):
        # Example: Ensure that 'status' and 'type' are not empty
        if not value or not value.strip():
            raise ValueError(f"{key} cannot be empty")
        return value

    def __repr__(self):
        return f"object: Ba7beshBusiness  id: {self.id}, name: {self.en_name}"


# Index creation
ba7besh_business_location_index = Index(
    "ba7besh_business_location_fc3ec09e_id", Ba7beshBusiness.location
)
ba7besh_business_slug_index = Index(
    "ba7besh_business_slug_ce0fd4e6_like", Ba7beshBusiness.slug
)


class BusinessWorkingHours(Base):
    __tablename__ = "business_working_hours"

    id = Column(Integer, primary_key=True, autoincrement=True)
    business_id = Column(
        Integer, ForeignKey("business.id", ondelete="CASCADE"), nullable=False
    )
    day = Column(Integer, nullable=False)  # Starting from 1 = Monday
    opening_time = Column(Time, nullable=False)
    closing_time = Column(Time, nullable=False)


class BusinessContacts(Base):
    __tablename__ = "business_contacts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    business_id = Column(
        Integer, ForeignKey("business.id", ondelete="CASCADE"), nullable=False
    )
    contact_type = Column(String(15), nullable=False)
    contact_value = Column(String(255), nullable=False)


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, autoincrement=True)
    slug = Column(String(255), unique=True, nullable=False)
    ar_name = Column(String(255))
    en_name = Column(String(255))
    parent_id = Column(Integer, ForeignKey("category.id", ondelete="SET NULL"))


class BusinessCategories(Base):
    __tablename__ = "business_categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    business_id = Column(
        Integer, ForeignKey("business.id", ondelete="CASCADE"), nullable=False
    )
    category_id = Column(
        Integer, ForeignKey("category.id", ondelete="PROTECT"), nullable=False
    )


class Feature(Base):
    __tablename__ = "feature"

    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(
        Integer, ForeignKey("category.id", ondelete="CASCADE"), nullable=False
    )
    ar_name = Column(String(255), nullable=False)
    en_name = Column(String(255), nullable=False)


class BusinessFeatures(Base):
    __tablename__ = "business_features"

    id = Column(Integer, primary_key=True, autoincrement=True)
    business_id = Column(
        Integer, ForeignKey("business.id", ondelete="CASCADE"), nullable=False
    )
    feature_id = Column(
        Integer, ForeignKey("feature.id", ondelete="PROTECT"), nullable=False
    )


class BusinessTags(Base):
    __tablename__ = "business_tags"

    id = Column(Integer, primary_key=True, autoincrement=True)
    business_id = Column(
        Integer, ForeignKey("business.id", ondelete="CASCADE"), nullable=False
    )
    tag = Column(String(255), nullable=False)


class FeaturesCategory(Base):
    __tablename__ = "features_category"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ar_name = Column(String(255), nullable=False)
    en_name = Column(String(255), nullable=False)
