from enum import Enum
from typing import List, Optional, Dict

import pydantic
from pydantic import Field

from src.app.dtos.base_dto import BaseDTO, BasePaginationRequest
from src.core.entities.business.enums import BusinessType


class LocationRequest(BaseDTO):
    latitude: float = Field(...)
    longitude: float = Field(...)
    radiusInKM: float = Field(..., description="Radius in KM")


class SearchBusinessSortOptions(Enum):
    RATING = "rating"
    DISTANCE = "distance"


class SearchBusinessRequest(BasePaginationRequest):
    type: BusinessType = Field(default=BusinessType.RESTAURANT)
    name: Optional[str] = Field(default=None)
    categoryName: Optional[str] = Field(default=None)
    categories: Optional[List[str]] = Field(
        default=None, description="List of category ids"
    )
    tags: Optional[List[str]] = Field(default=None, description="List of tags")
    features: Optional[List[str]] = Field(
        default=None, description="List of feature ids"
    )
    location: Optional[LocationRequest] = Field(default=None)
    openedNow: Optional[bool] = Field(default=None)
    sortBy: SearchBusinessSortOptions = Field(
        default=SearchBusinessSortOptions.DISTANCE
    )

    @pydantic.model_validator(mode="before")
    def validate_name_or_category_name_should_be_present(cls, values: Dict):
        if values.get("name") is None and values.get("categoryName") is None:
            raise ValueError("Name or categoryName should be present")
        return values
