from typing import List

from geoalchemy2 import Geography
from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Time,
)
from sqlalchemy.orm import Mapped  # type: ignore
from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship
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

    business_working_hours: Mapped[List["BusinessWorkingHours"]] = relationship(
        "BusinessWorkingHours", back_populates="business"
    )

    def __repr__(self):
        return f"Business: {self.en_name}"


class BusinessWorkingHours(Base):
    __tablename__ = "business_working_hours"

    id: Mapped[Integer] = mapped_column(Integer, primary_key=True, autoincrement=True)
    day: Mapped[Integer] = mapped_column(
        Integer,
        CheckConstraint("day >= 1 AND day <= 7"),
        nullable=False,
    )
    opening_time: Mapped[Time] = mapped_column(Time, nullable=False)
    closing_time: Mapped[Time] = mapped_column(Time, nullable=False)
    business_id: Mapped[Integer] = mapped_column(
        Integer,
        ForeignKey("business.id", deferrable=True, initially="DEFERRED"),
        nullable=False,
    )
    business: Mapped["Business"] = relationship(
        "Business", back_populates="business_working_hours"
    )


class BusinessContacts(Base):
    __tablename__ = "business_contacts"

    id: Mapped[Integer] = mapped_column(Integer, primary_key=True, autoincrement=True)
    contact_type: Mapped[str] = mapped_column(String(15), nullable=False)
    contact_value: Mapped[str] = mapped_column(String(255), nullable=False)
    business_id: Mapped[Integer] = mapped_column(
        Integer,
        ForeignKey("business.id", deferrable=True, initially="DEFERRED"),
        nullable=False,
    )

    business: Mapped["Business"] = relationship(
        "Business", back_populates="business_contacts"
    )


class Category(Base):
    __tablename__ = "category"

    id: Mapped[Integer] = mapped_column(Integer, primary_key=True, autoincrement=True)
    slug = mapped_column(String(255), unique=True, nullable=False)
    ar_name: Mapped[str] = mapped_column(String(255))
    en_name: Mapped[str] = mapped_column(String(255))
    parent_id: Mapped[Integer] = mapped_column(
        Integer, ForeignKey("category.id"), nullable=True
    )


class BusinessCategories(Base):
    __tablename__ = "business_categories"

    id: Mapped[Integer] = mapped_column(Integer, primary_key=True, autoincrement=True)
    business_id: Mapped[Integer] = mapped_column(
        ForeignKey("business.id", deferrable=True, initially="DEFERRED"),
        nullable=False,
    )
    category_id: Mapped[Integer] = mapped_column(
        Integer,
        ForeignKey("category.id", deferrable=True, initially="DEFERRED"),
        nullable=False,
    )

    business: Mapped["Business"] = relationship(
        "Business", back_populates="business_categories"
    )
    # category: Mapped["mapped_column.mapped_class"] = mapped_column(
    #     mapped_column.class_of_type("Category")
    # )


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


class BusinessFeatures(Base):
    __tablename__ = "business_features"

    id: Mapped[Integer] = mapped_column(Integer, primary_key=True, autoincrement=True)
    business_id: Mapped[Integer] = mapped_column(
        Integer,
        ForeignKey("business.id", deferrable=True, initially="DEFERRED"),
        nullable=False,
    )
    feature_id: Mapped[Integer] = mapped_column(
        Integer,
        ForeignKey("feature.id", deferrable=True, initially="DEFERRED"),
        nullable=False,
    )

    # business: Mapped["mapped_column.mapped_class"] = mapped_column(
    #     mapped_column.class_of_type("Business")
    # )
    # feature: Mapped["mapped_column.mapped_class"] = mapped_column(
    #     mapped_column.class_of_type("Feature")
    # )


class BusinessTags(Base):
    __tablename__ = "business_tags"

    id: Mapped[Integer] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tag: Mapped[str] = mapped_column(String(255), nullable=False)
    business_id: Mapped[Integer] = mapped_column(
        Integer,
        ForeignKey("business.id", deferrable=True, initially="DEFERRED"),
        nullable=False,
    )

    # business: Mapped["mapped_column.mapped_class"] = mapped_column(
    #     mapped_column.class_of_type("Business")
    # )


class FeaturesCategory(Base):
    __tablename__ = "features_category"

    id: Mapped[Integer] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ar_name: Mapped[str] = mapped_column(String(255), nullable=False)
    en_name: Mapped[str] = mapped_column(String(255), nullable=False)


Index(
    "business_working_hours_business_id_day_index",
    BusinessWorkingHours.business_id,
    BusinessWorkingHours.day,
)
Index("business_tags_business_id_index", BusinessTags.business_id)
Index("business_features_business_id_index", BusinessFeatures.business_id)
Index("business_features_feature_id_index", BusinessFeatures.feature_id)
Index("business_contacts_business_id_index", BusinessContacts.business_id)
Index("business_categories_business_id_index", BusinessCategories.business_id)
Index("business_categories_category_id_index", BusinessCategories.category_id)
