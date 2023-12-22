from dataclasses import dataclass
from datetime import time
from typing import Optional

from src.core.entities.business.enums import BusinessStatus, Day


@dataclass
class BusinessListQuery:
    status: Optional[BusinessStatus] = None
    min_opening_time: Optional[time] = None
    max_closing_time: Optional[time] = None
    day_filter: Optional[Day] = None
    page_size: Optional[int] = None
    page_number: Optional[int] = None
