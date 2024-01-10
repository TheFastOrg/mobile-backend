"""Endpoints module."""

from typing import Annotated
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Response, status, Header
from starlette.requests import Request

from src.app.configurator.containers import Container
from src.app.dtos.business import SearchBusinessRequest
from src.core.entities.business.enums import BusinessStatus, Day
from src.core.services.business_service import BusinessService
from src.app.mappers.business import BusinessMapper

businessRouter = APIRouter(prefix="/v1/businesses", tags=["Business"])


@businessRouter.post("/search")
@inject
async def search(
    request: Request,
    query: SearchBusinessRequest,
    service: BusinessService = Depends(Provide[Container.business_service]),
):
    core_query = BusinessMapper.to_core_query(query)
    language = request.scope.get("language", "en")
    core_query.language = language
    business = service.search(core_query)
    return business
