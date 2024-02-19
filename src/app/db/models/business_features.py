import uuid
from sqlalchemy import ForeignKey, Index, UUID
from sqlalchemy.orm import mapped_column

from src.app.db.models.base import Base


class BusinessFeatures(Base):
    __tablename__ = "business_features"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    business_id = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("business.id", deferrable=True, initially="DEFERRED"),
        nullable=False,
    )
    feature_id = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("feature.id", deferrable=True, initially="DEFERRED"),
        nullable=False,
    )


Index("business_features_business_id_index", BusinessFeatures.business_id)
Index("business_features_feature_id_index", BusinessFeatures.feature_id)
