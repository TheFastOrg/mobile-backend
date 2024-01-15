from typing import Optional, List, Dict

import pydantic
from pydantic import Field

from src.app.dtos.base_dto import BasePaginationRequest
from src.app.dtos.business.search_business_location_model import (
    SearchBusinessLocationModel,
)
from src.core.entities.business.enums import BusinessType, BusinessSort


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
    sortBy: Optional[BusinessSort] = Field(default=None)

    @pydantic.model_validator(mode="before")
    def validate_name_or_category_name_should_be_present(cls, values: Dict):
        if values.get("name") is None and values.get("categoryName") is None:
            raise ValueError("Name or categoryName should be present")
        return values
