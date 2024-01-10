from typing import Optional, List
from pydantic import BaseModel, Field

from src.core.entities.business.enums import BusinessType

#
# @dataclass
# class BusinessListQuery:
#     status: Optional[BusinessStatus] = None
#     min_opening_time: Optional[time] = None
#     max_closing_time: Optional[time] = None
#     day_filter: Optional[Day] = None
#
#     page_size: int = 100
#     page_number: int


class BusinessSearchQuery(BaseModel):
    type: BusinessType = Field(default=BusinessType.RESTAURANT)
    name: str = Field(...)
    categoryName: str = Field(...)
    categories: Optional[List[str]] = Field(
        default=None, description="List of category ids"
    )
    tags: List[str] = Field(..., description="List of tags")
    features: List[str] = Field(..., description="List of feature ids")
    latitude: float = Field(...)
    longitude: float = Field(...)
    radiusInMeter: float = Field(..., description="Radius in meter")
    openedNow: bool = Field(...)
    # sortBy: SearchBusinessSortOptions = Field(...)
    page_size: int = 100
    page_number: int = 1
