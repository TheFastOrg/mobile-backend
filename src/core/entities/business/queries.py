from datetime import time
from typing import Optional
from pydantic import BaseModel

from src.core.entities.business.enums import BusinessStatus, Day


# @dataclass
# class BusinessListQuery:
#     status: Optional[BusinessStatus] = None
#     min_opening_time: Optional[time] = None
#     max_closing_time: Optional[time] = None
#     day_filter: Optional[Day] = None

#     page_size: int = 100
#     page_number: int


class BusinessSearchQuery(BaseModel):
    status: Optional[BusinessStatus] = None
    min_opening_time: Optional[time] = None
    max_closing_time: Optional[time] = None
    day_filter: Optional[Day] = None

    page_size: int = 100
    page_number: int = 1
