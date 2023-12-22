from enum import Enum, auto


class Day(Enum):
    MONDAY = auto()
    TUESDAY = auto()
    WEDNESDAY = auto()
    THURSDAY = auto()
    FRIDAY = auto()
    SATURDAY = auto()
    SUNDAY = auto()


class BusinessStatus(Enum):
    DRAFT = auto()
    VERIFIED = auto()
    CLAIMED = auto()
    DISCONTINUED = auto()


class BusinessType(Enum):
    RESTAURANT = auto()
