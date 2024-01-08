from datetime import time

import pytest

from src.core.entities.business.business import Business
from src.core.entities.business.enums import Day
from src.core.entities.business.exceptions import (
    BusinessNotFoundError,
    WorkingDayOverlapError,
)
from src.core.entities.business.value_types import (
    BusinessId,
    WorkingDay,
    Location,
    MultilingualName,
)


class TestBusiness:
    def test_get_by_id_should_raise_error(self, container):
        service = container.business_service()
        with pytest.raises(BusinessNotFoundError):
            service.get_by_id(BusinessId())

    def test_add_valid_business_working_day(self):
        business = Business.create(
            names=MultilingualName(
                en_name="co-worker restaurant", ar_name="مطعم كووركر"
            ),
            location=Location(33.507780, 36.285530),
        )
        working_day = WorkingDay(
            day=Day.MONDAY, opening_time=time(9), closing_time=time(17)
        )

        business.add_working_day(working_day)

        assert working_day in business.working_days

    def test_add_invalid_business_opening_time_overlap(self):
        business = Business.create(
            names=MultilingualName(
                en_name="co-worker restaurant", ar_name="مطعم كووركر"
            ),
            location=Location(33.507780, 36.285530),
        )
        existing_working_day = WorkingDay(
            day=Day.MONDAY, opening_time=time(8), closing_time=time(16)
        )
        business.add_working_day(existing_working_day)

        working_day = WorkingDay(
            day=Day.MONDAY, opening_time=time(9), closing_time=time(17)
        )
        with pytest.raises(WorkingDayOverlapError):
            business.add_working_day(working_day)

    def test_add_invalid_business_closing_time_overlap(self):
        business = Business.create(
            names=MultilingualName(
                en_name="co-worker restaurant", ar_name="مطعم كووركر"
            ),
            location=Location(33.507780, 36.285530),
        )
        existing_working_day = WorkingDay(
            day=Day.MONDAY, opening_time=time(8), closing_time=time(16)
        )
        business.add_working_day(existing_working_day)

        working_day = WorkingDay(
            day=Day.MONDAY, opening_time=time(7), closing_time=time(15)
        )
        with pytest.raises(WorkingDayOverlapError):
            business.add_working_day(working_day)
