from typing import List, Optional

from pydantic import Field

from src.app.dtos.base_dto import BaseDTO
from src.app.dtos.business.address_model import AddressModel
from src.app.dtos.business.location_model import LocationModel
from src.app.dtos.business.wokring_hour_model import WorkingHourModel


class SearchBusinessResponse(BaseDTO):
    id: str
    name: str
    location: LocationModel
    number_of_reviews: int = Field(default=0, ge=0)
    tags: List[str]
    overall_rating: float = Field(default=0, ge=0, le=5)
    address: Optional[AddressModel] = None
    working_hours: List[WorkingHourModel]
