import datetime
from contextlib import AbstractContextManager
from typing import Callable, Iterator, Optional
from geoalchemy2.shape import to_shape
from sqlalchemy.orm import Session
from src.app.db.models.business import Business as DBBusiness
from src.core.entities.business.business import Business as Business
from src.core.entities.business.enums import BusinessType, Day
from src.core.entities.business.queries import BusinessSearchQuery
from src.core.entities.business.value_types import (
    Address,
    BusinessId,
    Location,
    MultilingualName,
)
from src.core.interfaces.repositories.business_repository import BusinessRepository


class DBBusinessRepository(BusinessRepository):
    def __init__(
        self, session_factory: Callable[..., AbstractContextManager[Session]]
    ) -> None:
        self.session_factory = session_factory

    def get_by_id(self, business_id: BusinessId) -> Optional[Business]:
        return None

    def get_all(self, query: BusinessSearchQuery) -> Iterator[Business]:
        with self.session_factory() as session:
            db_query = session.query(DBBusiness)
            if query.type:
                db_query = db_query.filter(DBBusiness.type == query.type)

            if query.name:
                if query.language == "ar":
                    db_query = db_query.filter(DBBusiness.ar_name == query.name)
                else:
                    db_query = db_query.filter(DBBusiness.en_name == query.name)

            if query.openedNow:
                today = datetime.datetime.now()
                day = Day(today.isoweekday())
                now = today.now().time()
                #TODO obay, plase check this in the real db
                db_query = db_query.filter(
                        DBBusiness.business_working_hours.any(
                            day=day, opening_time__gte=now, closing_time__lte=now
                        )
                    )
            # if query.categoryName:
            #     db_query = db_query.filter(
            #         DBBusiness.categories.any(=query.day_filter)
            #     )
            # if query.day_filter:
            #     db_query = db_query.filter(
            #         DBBusiness.business_working_hours.any(day=query.day_filter)
            #     )
            # if query.max_closing_time:
            #     db_query = db_query.filter(
            #         DBBusiness.business_working_hours.any(
            #             BusinessWorkingHours.closing_time <= query.max_closing_time
            #         )
            #     )
            # if query.min_opening_time:
            #     db_query = db_query.filter(
            #         DBBusiness.business_working_hours.any(
            #             BusinessWorkingHours.opening_time >= query.min_opening_time
            #         )
            #     )
            if query.page_size:
                db_query = db_query.limit(query.page_size)

            if query.page_number and query.page_size:
                offset = query.page_number * query.page_size
                db_query = db_query.offset(offset).limit(query.page_size)

            results = db_query.all()

            return iter([self.from_db_to_business(item) for item in results])

    @staticmethod
    def from_db_to_business(db_business: DBBusiness) -> Business:
        point = to_shape(db_business.location)  # type: ignore
        return Business(
            business_id=BusinessId(""),
            names=MultilingualName(db_business.ar_name, db_business.en_name),
            address=Address(
                db_business.country,
                db_business.city,
                db_business.address_line1,
                db_business.address_line2,
            ),
            location=Location(point.y, point.x),
            type=BusinessType.RESTAURANT,
        )
