from datetime import time
from enum import Enum
from typing import List, Optional, Dict

import pydantic
from pydantic import Field

from src.app.dtos.base_dto import BaseDTO, BasePaginationRequest
from src.core.entities.business.enums import BusinessType, Day


class LocationModel(BaseDTO):
    latitude: float = Field(...)
    longitude: float = Field(...)


class AddressModel(BaseDTO):
    address_line1: str
    address_line2: str
    city: str


class SearchBusinessLocationModel(LocationModel):
    radiusInKM: Optional[float] = Field(5, description="Radius in KM")


class SearchBusinessSortModel(Enum):
    RATING = "rating"
    DISTANCE = "distance"


class SearchBusinessRequest(BasePaginationRequest):
    type: BusinessType = Field(default=BusinessType.RESTAURANT)
    name: Optional[str] = Field(default=None, min_length=1)
    categoryName: Optional[str] = Field(default=None, min_length=1)
    categories: Optional[List[str]] = Field(
        default=None, description="List of category ids"
    )
    tags: Optional[List[str]] = Field(default=None, description="List of tags")
    features: Optional[List[str]] = Field(
        default=None, description="List of feature ids"
    )
    location: Optional[SearchBusinessLocationModel] = Field(default=None)
    openedNow: Optional[bool] = Field(default=None)
    sortBy: SearchBusinessSortModel = Field(default=SearchBusinessSortModel.DISTANCE)

    @pydantic.model_validator(mode="before")
    def validate_name_or_category_name_should_be_present(cls, values: Dict):
        if values.get("name") is None and values.get("categoryName") is None:
            raise ValueError("Name or categoryName should be present")
        return values


class WorkingHourModel(BaseDTO):
    day: Day
    opening_time: time
    closing_time: time


class SearchBusinessResponse(BaseDTO):
    id: str
    name: str
    location: LocationModel
    number_of_reviews: int = Field(default=0, ge=0)
    tags: List[str]
    overall_rating: float = Field(default=0, ge=0, le=5)
    address: Optional[AddressModel] = None
    working_hours: List[WorkingHourModel]
