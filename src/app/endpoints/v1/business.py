"""Endpoints module."""

from typing import List
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from starlette.requests import Request

from src.app.configurator.containers import Container
from src.app.dtos.business.search_business_request import SearchBusinessRequest
from src.app.dtos.business.search_business_response import SearchBusinessResponse
from src.app.dtos.core import PaginationJSONResponse
from src.app.endpoints.utilities import language_parser
from src.core.services.business_service import BusinessService
from src.app.mappers.business import BusinessMapper

businessRouter = APIRouter(prefix="/v1/businesses", tags=["Business"])


@businessRouter.post(
    "/search",
    response_model=List[SearchBusinessResponse],
    dependencies=[Depends(language_parser)],
)
@inject
async def search(
    request: Request,
    query: SearchBusinessRequest,
    service: BusinessService = Depends(Provide[Container.business_service]),
):
    language = language_parser(request)
    core_query = BusinessMapper.to_core_query(query, language)
    total_count, businesses = service.search(core_query)
    result = [BusinessMapper.to_search_response(item, language) for item in businesses]
    return PaginationJSONResponse(
        total_count, query.page_number, query.page_size, result
    )
