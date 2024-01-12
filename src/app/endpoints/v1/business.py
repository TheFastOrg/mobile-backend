"""Endpoints module."""

from typing import List
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from starlette.requests import Request

from src.app.configurator.containers import Container
from src.app.dtos.business import SearchBusinessRequest, SearchBusinessResponse
from src.app.dtos.core import PaginationJSONResponse
from src.core.services.business_service import BusinessService
from src.app.mappers.business import BusinessMapper

businessRouter = APIRouter(prefix="/v1/businesses", tags=["Business"])


@businessRouter.post(
    "/search",
    response_model=List[SearchBusinessResponse],
)
@inject
async def search(
    request: Request,
    query: SearchBusinessRequest,
    service: BusinessService = Depends(Provide[Container.business_service]),
):
    core_query = BusinessMapper.to_core_query(query)
    language = request.scope.get("language", "en")
    core_query.language = language
    total_count, businesses = service.search(core_query)
    result = [BusinessMapper.to_search_response(item) for item in businesses]
    return PaginationJSONResponse(
        total_count, query.page_number, query.page_size, result
    )
