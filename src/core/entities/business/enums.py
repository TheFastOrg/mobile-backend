from enum import Enum, auto


class Day(Enum):
    MONDAY = auto()
    TUESDAY = auto()
    WEDNESDAY = auto()
    THURSDAY = auto()
    FRIDAY = auto()
    SATURDAY = auto()
    SUNDAY = auto()


class BusinessStatus(str, Enum):
    DRAFT = "draft"
    VERIFIED = "verified"
    CLAIMED = "claimed"
    DISCONTINUED = "discontinued"


class BusinessType(Enum):
    RESTAURANT = "restaurant"


class SupportedLanguage(Enum):
    EN = "en"
    AR = "ar"
