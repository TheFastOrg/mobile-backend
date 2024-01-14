from pydantic import Field

from src.app.dtos.base_dto import BaseDTO


class LocationModel(BaseDTO):
    latitude: float = Field(...)
    longitude: float = Field(...)
