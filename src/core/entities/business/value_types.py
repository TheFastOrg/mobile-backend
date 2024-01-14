import datetime
import uuid
from dataclasses import dataclass, field

from src.core.entities.business.enums import Day, SupportedLanguage


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
        return self.en_name

    def name(self, language: SupportedLanguage) -> str:
        if language == SupportedLanguage.AR:
            return self.ar_name

        return self.default_name()


@dataclass(frozen=True)
class WorkingDay:
    """
    Attributes:
        day (int): An integer representing the day of the week (from 1 to 7 where 1 represents Monday).
    """

    day: Day
    opening_time: datetime.time
    closing_time: datetime.time


@dataclass(frozen=True)
class BusinessId:
    value: str = field(default_factory=lambda: str(uuid.uuid4()))

    @classmethod
    def generate(cls) -> "BusinessId":
        return cls()

    def __repr__(self):
        return self.value
