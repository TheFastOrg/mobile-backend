from sqlalchemy import (
    ForeignKey,
    Index,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped  # type: ignore
from sqlalchemy.orm import mapped_column

from src.app.db.models.base import Base


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


Index("business_contacts_business_id_index", BusinessContacts.business_id)
