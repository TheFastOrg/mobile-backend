from dataclasses import dataclass, field
from typing import List, Optional

from core.entities.business.enums import BusinessStatus, BusinessType
from core.entities.business.exceptions import OpeningTimeError, WorkingDayOverlapError
from core.entities.business.value_types import (
    Address,
    BusinessId,
    Location,
    MultilingualName,
    WorkingDay,
)


# Aggregate Root
@dataclass
class Business:
    business_id: BusinessId
    names: MultilingualName
    location: Location
    type: BusinessType
    address: Optional[Address] = None
    status: BusinessStatus = BusinessStatus.DRAFT
    working_days: List[WorkingDay] = field(default_factory=list)

    @classmethod
    def create(
        cls,
        names: MultilingualName,
        location: Location,
        type: BusinessType,
        address: Optional[Address] = None,
    ) -> "Business":
        business_id = BusinessId.generate()
        return cls(
            business_id=business_id,
            names=names,
            location=location,
            type=type,
            address=address,
        )

    def add_working_day(self, working_day: WorkingDay):
        # Validate that the opening time doesn't overlap with the closing time
        if working_day.opening_time >= working_day.closing_time:
            raise OpeningTimeError()

        # Validate that working days don't have overlapping days or times
        for existing_working_day in self.working_days:
            if existing_working_day.day == working_day.day:
                if (
                    existing_working_day.opening_time
                    < working_day.opening_time
                    < existing_working_day.closing_time
                ) or (
                    existing_working_day.opening_time
                    < working_day.closing_time
                    < existing_working_day.closing_time
                ):
                    raise WorkingDayOverlapError()

        self.working_days.append(working_day)

    __repr__ = __str__ = lambda self: f"Business: {self.names.en_name}"
