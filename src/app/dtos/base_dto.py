from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

from fastapi.encoders import jsonable_encoder
from humps import camelize
from pydantic import BaseModel, ConfigDict, model_validator


def to_camel(string):
    return camelize(string)


def convert_datetime_to_gmt(dt: datetime) -> str:
    if not dt.tzinfo:
        dt = dt.replace(tzinfo=ZoneInfo("UTC"))

    return dt.strftime("%Y-%m-%dT%H:%M:%S%z")


class BaseDTO(BaseModel):
    model_config = ConfigDict(
        json_encoders={datetime: convert_datetime_to_gmt},
        populate_by_name=True,
        alias_generator=to_camel,
    )

    @model_validator(mode="before")
    @classmethod
    def set_null_microseconds(cls, data: dict[str, Any]) -> dict[str, Any]:
        datetime_fields = {
            k: v.replace(microsecond=0)
            for k, v in data.items()
            if isinstance(k, datetime)
        }

        return {**data, **datetime_fields}

    def serializable_dict(self, **kwargs):
        """Return a dict which contains only serializable fields."""
        default_dict = self.model_dump()

        return jsonable_encoder(default_dict)