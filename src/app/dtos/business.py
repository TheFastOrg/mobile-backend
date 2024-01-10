from enum import Enum
from typing import List, Optional

from pydantic import Field

from src.app.dtos.base_dto import BaseDTO, BasePaginationRequest
from src.core.entities.business.enums import BusinessType


class LocationRequest(BaseDTO):
    latitude: float = Field(...)
    longitude: float = Field(...)
    radiusInMeter: float = Field(..., description="Radius in meter")


class SearchBusinessSortOptions(Enum):
    RATING = "rating"
    DISTANCE = "distance"


class SearchBusinessRequest(BasePaginationRequest):
    type: BusinessType = Field(default=BusinessType.RESTAURANT)
    name: str = Field(...)
    categoryName: str = Field(...)
    categories: Optional[List[str]] = Field(
        default=None, description="List of category ids"
    )
    tags: List[str] = Field(..., description="List of tags")
    features: List[str] = Field(..., description="List of feature ids")
    location: LocationRequest = Field(...)
    openedNow: bool = Field(...)
    sortBy: SearchBusinessSortOptions = Field(...)
