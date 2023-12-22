from abc import ABC, abstractmethod
from typing import List

from core.entities.business.business import Business
from core.entities.business.queries import BusinessListQuery
from core.entities.business.value_types import BusinessId


class BusinessRepository(ABC):
    @abstractmethod
    def list(self, query: BusinessListQuery) -> List[Business]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, business_id: BusinessId) -> Business:
        raise NotImplementedError
