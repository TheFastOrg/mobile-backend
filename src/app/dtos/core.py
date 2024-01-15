import typing

from fastapi.encoders import jsonable_encoder
from starlette.background import BackgroundTask
from starlette.responses import JSONResponse


def _calculate_total_pages(total_count, page_size):
    total_pages = max(
        1, total_count // page_size + (1 if total_count % page_size > 0 else 0)
    )
    return total_pages


class PaginationJSONResponse(JSONResponse):
    def __init__(
        self,
        total_count: int,
        page_number: int,
        page_size: int,
        content: typing.Any,
        status_code: int = 200,
        headers: typing.Optional[typing.Dict[str, str]] = None,
        media_type: typing.Optional[str] = None,
        background: typing.Optional[BackgroundTask] = None,
    ) -> None:
        total_pages = _calculate_total_pages(total_count, page_size)
        if headers is None:
            headers = {}
        headers["Pagination-Total-Count"] = str(total_count)
        headers["Pagination-Total-Pages"] = str(total_pages)
        headers["Pagination-Current-Page"] = str(page_number)
        headers["Pagination-Page-Size"] = str(page_size)
        super().__init__(content, status_code, headers, media_type, background)

    def render(self, content: typing.Any) -> bytes:
        json = jsonable_encoder(content)
        return super().render(json)
