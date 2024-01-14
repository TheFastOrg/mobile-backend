from datetime import time

from src.app.dtos.base_dto import BaseDTO
from src.core.entities.business.enums import Day


class WorkingHourModel(BaseDTO):
    day: Day
    opening_time: time
    closing_time: time
