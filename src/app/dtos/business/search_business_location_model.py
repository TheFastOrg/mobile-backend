from typing import Optional

from pydantic import Field

from src.app.dtos.business.location_model import LocationModel


class SearchBusinessLocationModel(LocationModel):
    radiusInKM: Optional[float] = Field(5, description="Radius in KM")
