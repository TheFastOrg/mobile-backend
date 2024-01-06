from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Index,
    Integer,
    Time,
)
from sqlalchemy.orm import Mapped  # type: ignore
from sqlalchemy.orm import mapped_column, relationship

from src.app.db.models.base import Base
from src.app.db.models.business import Business


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


Index(
    "business_working_hours_business_id_day_index",
    BusinessWorkingHours.business_id,
    BusinessWorkingHours.day,
)
