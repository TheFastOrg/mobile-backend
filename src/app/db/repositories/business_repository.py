import datetime
from contextlib import AbstractContextManager
from typing import Callable, Iterator, Optional
from geoalchemy2.shape import to_shape
from sqlalchemy import select, and_, func
from sqlalchemy.orm import Session, selectinload
from src.app.db.models.business import Business as DBBusiness
from src.app.db.models.business_tags import BusinessTags
from src.app.db.models.business_working_hours import BusinessWorkingHours
from src.app.db.models.category import Category
from src.app.db.models.feature import Feature
from src.core.entities.business.business import Business as Business
from src.core.entities.business.enums import (
    BusinessType,
    BusinessStatus,
    Day,
    SupportedLanguage,
)
from src.core.entities.business.queries import BusinessSearchQuery
from src.core.entities.business.value_types import (
    Address,
    BusinessId,
    Location,
    MultilingualName,
    WorkingDay,
)
from src.core.interfaces.repositories.business_repository import BusinessRepository


class DBBusinessRepository(BusinessRepository):
    def __init__(
        self, session_factory: Callable[..., AbstractContextManager[Session]]
    ) -> None:
        self.session_factory = session_factory

    def get_by_id(self, business_id: BusinessId) -> Optional[Business]:
        return None

    def get_all(self, query: BusinessSearchQuery) -> tuple[int, Iterator[Business]]:
        db_query = (
            select(DBBusiness, DBBusiness.tags, DBBusiness.working_hours)
            .distinct()
            .outerjoin(DBBusiness.tags)
            .outerjoin(DBBusiness.working_hours)
            .options(
                selectinload(DBBusiness.tags), selectinload(DBBusiness.working_hours)
            )
            .where(
                DBBusiness.status.in_(
                    [BusinessStatus.CLAIMED.value, BusinessStatus.VERIFIED.value]
                )
            )
        )

        if query.type:
            db_query = db_query.where(DBBusiness.type == query.type.value)

        if query.name:
            name_to_search = "%{}%".format(query.name)
            if query.language == SupportedLanguage.AR:
                db_query = db_query.where(DBBusiness.ar_name.like(name_to_search))
            else:
                db_query = db_query.where(DBBusiness.en_name.ilike(name_to_search))

        if query.openedNow is not None:
            today = datetime.datetime.now(tz=datetime.timezone.utc)
            now = today.time()
            time_filter = (
                and_(
                    now >= BusinessWorkingHours.opening_time,
                    now <= BusinessWorkingHours.closing_time,
                )
                if query.openedNow
                else and_(
                    now < BusinessWorkingHours.opening_time,
                    now > BusinessWorkingHours.closing_time,
                )
            )
            day = today.isoweekday()
            db_query = db_query.where(
                DBBusiness.working_hours.any(
                    and_(BusinessWorkingHours.day == day, time_filter)
                )
            )
        if query.categoryName:
            category_to_search = "%{}%".format(query.categoryName)
            category_name_filter = (
                Category.ar_name.like(category_to_search)
                if query.language == SupportedLanguage.AR
                else Category.en_name.ilike(category_to_search)
            )

            db_query = db_query.where(DBBusiness.categories.any(category_name_filter))
        if query.categories:
            db_query = db_query.where(
                DBBusiness.categories.any(Category.id.in_(query.categories))
            )
        if query.tags:
            db_query = db_query.where(
                DBBusiness.tags.any(BusinessTags.tag.in_(query.tags))
            )
        if query.features:
            db_query = db_query.where(
                DBBusiness.features.any(Feature.id.in_(query.features))
            )

        if query.latitude and query.longitude:
            db_query = db_query.where(
                func.ST_DWithin(
                    DBBusiness.location,
                    func.ST_SetSRID(
                        func.ST_MakePoint(query.longitude, query.latitude, srid=4326),
                        4326,
                    ),
                    query.radius_in_meters(),
                )
            )

        with self.session_factory() as session:
            total_count = session.execute(
                select(func.count()).select_from(db_query.subquery())
            ).scalar()
            total_count = total_count if total_count else 0

        # TODO implement sorting
        db_query = db_query.order_by(DBBusiness.created_at.desc())

        if query.page_size:
            db_query = db_query.limit(query.page_size)

        if query.page_number and query.page_size:
            offset = (query.page_number - 1) * query.page_size
            db_query = db_query.offset(offset).limit(query.page_size)

        with self.session_factory() as session:
            db_results = session.scalars(db_query).all()
        items = iter([self.from_db_to_business(item) for item in db_results])

        return total_count, items

    @staticmethod
    def from_db_to_business(db_business: DBBusiness) -> Business:
        point = to_shape(db_business.location)  # type: ignore
        return Business(
            business_id=BusinessId(db_business.id.__str__()),
            names=MultilingualName(db_business.ar_name, db_business.en_name),
            address=Address(
                db_business.country,
                db_business.city,
                db_business.address_line1,
                db_business.address_line2,
            ),
            location=Location(point.y, point.x),
            type=BusinessType.RESTAURANT,
            tags=[item.tag for item in db_business.tags],
            working_days=[
                WorkingDay(
                    day=Day(item.day),
                    opening_time=item.opening_time,  # type: ignore
                    closing_time=item.closing_time,  # type: ignore
                )
                for item in db_business.working_hours
            ],
        )
