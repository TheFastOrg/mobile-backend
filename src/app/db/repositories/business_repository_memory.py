from typing import Dict, Iterator, Optional

from src.core.entities.business.business import Business
from src.core.entities.business.queries import BusinessSearchQuery
from src.core.entities.business.value_types import (
    BusinessId,
    Location,
    MultilingualName,
)
from src.core.interfaces.repositories.business_repository import BusinessRepository


class InMemoryBusinessRepository(BusinessRepository):
    _data: Dict[BusinessId, Business]

    def __init__(self):
        self._data = {}  # Store businesses in a dictionary
        self.save(
            Business.create(
                names=MultilingualName(
                    en_name="co-worker restaurant", ar_name="مطعم كووركر"
                ),
                location=Location(33.507780, 36.285530),
            )
        )

    def save(self, business: Business) -> Business:
        if not business.business_id:
            business.business_id = BusinessId.generate()
        self._data[business.business_id] = business
        return business

    def get_by_id(self, business_id: BusinessId) -> Optional[Business]:
        return self._data.get(business_id)

    def get_all(self, query: BusinessSearchQuery) -> Iterator[Business]:
        for business in self._data.values():
            yield business
