from typing import Iterator, Optional

from src.core.entities.business.business import Business
from src.core.entities.business.exceptions import BusinessNotFoundError
from src.core.entities.business.queries import BusinessSearchQuery
from src.core.entities.business.value_types import BusinessId
from src.core.interfaces.repositories.business_repository import BusinessRepository


class BusinessService:
    business_repository: BusinessRepository

    def __init__(self, business_repository: BusinessRepository):
        self.business_repository = business_repository

    def search(self, query: BusinessSearchQuery) -> tuple[int, Iterator[Business]]:
        return self.business_repository.get_all(query)

    def get_by_id(self, business_id: BusinessId) -> Optional[Business]:
        business = self.business_repository.get_by_id(business_id)
        if business is None:
            raise BusinessNotFoundError(business_id)
        return business
