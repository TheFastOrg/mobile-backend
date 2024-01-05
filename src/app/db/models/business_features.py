
from sqlalchemy import (
    ForeignKey,
    Index,
    Integer,
)
from sqlalchemy.orm import Mapped  # type: ignore
from sqlalchemy.orm import mapped_column

from src.app.db.models import Base


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


Index("business_features_business_id_index", BusinessFeatures.business_id)
Index("business_features_feature_id_index", BusinessFeatures.feature_id)
