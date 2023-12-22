from contextlib import AbstractContextManager
from typing import Callable, Iterator

from geoalchemy2.shape import to_shape
from sqlalchemy.orm import Session

from src.app.db.models import Business as DBBusiness
from src.app.db.models import BusinessWorkingHours
from src.core.entities.business.business import Business as Business
from src.core.entities.business.enums import BusinessType
from src.core.entities.business.queries import BusinessListQuery
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

    def get_by_id(self, business_id: BusinessId) -> Business:
        pass

    def get_all(self, query: BusinessListQuery) -> Iterator[Business]:
        with self.session_factory() as session:
            db_query = session.query(DBBusiness)
            if query.status:
                db_query = db_query.filter(DBBusiness.status == query.status)
            if query.day_filter:
                db_query = db_query.filter(
                    DBBusiness.business_working_hours.any(day=query.day_filter)
                )
            if query.max_closing_time:
                db_query = db_query.filter(
                    DBBusiness.business_working_hours.any(
                        BusinessWorkingHours.closing_time <= query.max_closing_time
                    )
                )
            if query.min_opening_time:
                db_query = db_query.filter(
                    DBBusiness.business_working_hours.any(
                        BusinessWorkingHours.opening_time >= query.min_opening_time
                    )
                )
            if query.page_size:
                db_query = db_query.limit(query.page_size)

            if query.page_number and query.page_size:
                offset = query.page_number * query.page_size
                db_query = db_query.offset(offset).limit(query.page_size)

            results = db_query.all()

            return [self.from_db_to_business(item) for item in results]

    @staticmethod
    def from_db_to_business(db_business: DBBusiness) -> Business:
        point = to_shape(db_business.location)
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
