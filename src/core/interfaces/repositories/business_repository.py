from abc import ABC, abstractmethod
from typing import Iterator, Optional

from src.core.entities.business.business import Business
from src.core.entities.business.queries import BusinessSearchQuery
from src.core.entities.business.value_types import BusinessId


class BusinessRepository(ABC):
    @abstractmethod
    def get_all(self, query: BusinessSearchQuery) -> tuple[int, Iterator[Business]]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, business_id: BusinessId) -> Optional[Business]:
        raise NotImplementedError
