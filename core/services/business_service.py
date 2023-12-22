from typing import List

from core.entities.business.business import Business
from core.entities.business.queries import BusinessListQuery
from core.entities.business.value_types import BusinessId
from core.interfaces.repositories.business_repository import BusinessRepository


class BusinessService:
    business_repository: BusinessRepository

    def __init__(self, business_repository: BusinessRepository):
        self.business_repository = business_repository

    def list(self, query: BusinessListQuery) -> List[Business]:
        return self.business_repository.list(query)

    def get_by_id(self, business_id: BusinessId) -> Business:
        return self.business_repository.get_by_id(business_id)
