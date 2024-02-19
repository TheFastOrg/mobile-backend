import uuid
from sqlalchemy import ForeignKey, Index, String, UUID
from sqlalchemy.orm import Mapped  # type: ignore
from sqlalchemy.orm import mapped_column

from src.app.db.models.base import Base


class BusinessContacts(Base):
    __tablename__ = "business_contacts"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    contact_type: Mapped[str] = mapped_column(String(15), nullable=False)
    contact_value: Mapped[str] = mapped_column(String(255), nullable=False)

    business_id = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("business.id", deferrable=True, initially="DEFERRED"),
        nullable=False,
    )


Index("business_contacts_business_id_index", BusinessContacts.business_id)
