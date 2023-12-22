import datetime
import uuid
from dataclasses import dataclass, field

from src.core.entities.business.enums import Day


@dataclass(frozen=True)
class Location:
    latitude: float
    longitude: float


@dataclass(frozen=True)
class Address:
    country: str
    city: str
    address_line1: str
    address_line2: str


@dataclass(frozen=True)
class MultilingualName:
    ar_name: str
    en_name: str

    def default_name(self) -> str:
        return self.en_name  # You can choose another default language if needed


@dataclass(frozen=True)
class WorkingDay:
    day: Day
    opening_time: datetime.time
    closing_time: datetime.time


@dataclass(frozen=True)
class BusinessId:
    value: str = field(default_factory=lambda: str(uuid.uuid4()))

    @classmethod
    def generate(cls) -> "BusinessId":
        return cls()
