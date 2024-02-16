import uuid
from sqlalchemy import (
    ForeignKey,
    Index,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column

from src.app.db.models.base import Base


class BusinessCategories(Base):
    __tablename__ = "business_categories"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    business_id = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("business.id", deferrable=True, initially="DEFERRED"),
        nullable=False,
    )
    category_id = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("category.id", deferrable=True, initially="DEFERRED"),
        nullable=False,
    )


Index("business_categories_business_id_index", BusinessCategories.business_id)
Index("business_categories_category_id_index", BusinessCategories.category_id)
