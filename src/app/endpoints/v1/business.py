"""Endpoints module."""


from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Response, status

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
):
    coreQuery = BusinessMapper.to_core_query(query)
    business = service.get_all(coreQuery)
    print("Database connectivity test successful:", business)
    return Response(
        content="Hey, ba7besh started here!", status_code=status.HTTP_200_OK
    )
