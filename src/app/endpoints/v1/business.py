"""Endpoints module."""

from typing import Annotated
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Response, status, Header

from src.app.configurator.containers import Container
from src.app.dtos.business import SearchBusinessRequest
from src.core.entities.business.enums import BusinessStatus, Day
from src.core.services.business_service import BusinessService
from src.app.mappers.business import BusinessMapper

businessRouter = APIRouter(prefix="/v1/businesses", tags=["Business"])


@businessRouter.post("/search")
@inject
async def search(
    query: SearchBusinessRequest,
    service: BusinessService = Depends(Provide[Container.business_service]),
    accept_language: Annotated[str | None, Header()] = None,
):
    core_query = BusinessMapper.to_core_query(query)
    core_query.language = accept_language or "en"
    business = service.search(core_query)
    return business
