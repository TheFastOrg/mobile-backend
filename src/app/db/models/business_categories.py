
from sqlalchemy import (
    ForeignKey,
    Index,
    Integer,
)
from sqlalchemy.orm import Mapped  # type: ignore
from sqlalchemy.orm import mapped_column, relationship

from src.app.db.models import Base
from src.app.db.models.business import Business


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


Index("business_categories_business_id_index", BusinessCategories.business_id)
Index("business_categories_category_id_index", BusinessCategories.category_id)
