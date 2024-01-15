from typing import Optional, List
from pydantic import BaseModel, Field

from src.core.entities.business.enums import (
    BusinessType,
    SupportedLanguage,
    BusinessSort,
)


class BusinessSearchQuery(BaseModel):
    type: BusinessType = Field(default=BusinessType.RESTAURANT)
    name: Optional[str] = Field(...)
    categoryName: Optional[str] = Field(...)
    categories: Optional[List[str]] = Field(
        default=None, description="List of category ids"
    )
    tags: Optional[List[str]] = Field(..., description="List of tags")
    features: Optional[List[str]] = Field(..., description="List of feature ids")
    latitude: Optional[float] = Field(default=None)
    longitude: Optional[float] = Field(default=None)
    radiusInKM: Optional[float] = Field(default=5, description="Radius in KM")
    openedNow: Optional[bool] = Field(default=None)
    sortBy: Optional[BusinessSort] = Field(default=None)
    page_size: int = 100
    page_number: int = 1
    language: SupportedLanguage = Field(default=SupportedLanguage.EN)

    def radius_in_meters(self):
        return self.radiusInKM * 1000
