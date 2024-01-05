
from sqlalchemy import (
    ForeignKey,
    Index,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped  # type: ignore
from sqlalchemy.orm import mapped_column

from src.app.db.models import Base


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


Index("business_tags_business_id_index", BusinessTags.business_id)
