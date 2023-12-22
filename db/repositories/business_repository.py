from typing import List

from geoalchemy2.shape import to_shape

from core.entities import (
    Address,
    Business,
    BusinessId,
    BusinessListQuery,
    BusinessType,
    Location,
    MultilingualName,
)
from core.interfaces.repositories.business_repository import BusinessRepository
from db.engine import Session
from db.models import Ba7beshBusiness


class DBBusinessRepository(BusinessRepository):
    def list(self, query: BusinessListQuery) -> List[Business]:
        with Session() as session:
            results = session.query(Ba7beshBusiness).limit(10).all()
            return []

    # def get_by_id(self, business_id: BusinessId) -> Business:
    #     return Business()

    @staticmethod
    def from_db_to_business(db_business: Ba7beshBusiness) -> Business:  # ignore
        point = to_shape(db_business.location)
        return Business(
            business_id=BusinessId("db_business.id"),
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
