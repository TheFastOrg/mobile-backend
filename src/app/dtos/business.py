from enum import Enum
from typing import List, Optional

from pydantic import Field

from src.app.dtos.base_dto import BaseDTO
from src.core.entities.business.enums import BusinessType

"""
{
type: BusinessTypeEnum,
name: string,
categoryName: string,
categories: array of categoryId,
tags: array of string,
features: array of featureId,
location: {latitude: floating number, longitude: floating number, radiusInMeter: optional +real number},
openedNow: boolean,
sortBy: SortByOptions (see below),
pageSize: (default 100),
pageNumber: (default 1)
}
"""


class LocationRequest(BaseDTO):
    latitude: float = Field(...)
    longitude: float = Field(...)
    radiusInMeter: float = Field(..., description="Radius in meter")


class SearchBusinessSortOptions(Enum):
    RATING = "rating"
    DISTANCE = "distance"


class SearchBusinessRequest(BaseDTO):
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
