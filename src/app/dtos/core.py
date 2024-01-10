from pydantic import Field

from src.app.dtos.base_dto import BaseDTO


class PaginationRequest(BaseDTO):
    page_size: int = Field(default=100)
    page_number: int = Field(default=1)
