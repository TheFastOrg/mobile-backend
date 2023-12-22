from typing import List

from geoalchemy2.shape import to_shape

from core.entities.business.business import Business
from core.entities.business.enums import BusinessType
from core.entities.business.queries import BusinessListQuery
from core.entities.business.value_types import (
    BusinessId,
    MultilingualName,
    Address,
    Location,
)
from core.interfaces.repositories.business_repository import BusinessRepository
from db.engine import Session
from db.models import Ba7beshBusiness


class DBBusinessRepository(BusinessRepository):
    # def get_by_id(self, business_id: BusinessId) -> Business:
    #     pass

    def list_all(self, query: BusinessListQuery) -> List[Business]:
        with Session() as session:
            results = session.query(Ba7beshBusiness).limit(10).all()
            return [self.from_db_to_business(item) for item in results]

    @staticmethod
    def from_db_to_business(db_business: Ba7beshBusiness) -> Business:
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
