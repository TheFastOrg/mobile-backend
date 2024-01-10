"""Endpoints module."""


from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Response, status

from src.app.configurator.containers import Container
from src.app.dtos.business import SearchBusinessRequest
from src.core.entities.business.queries import BusinessSearchQuery
from src.core.services.business_service import BusinessService

businessRouter = APIRouter(prefix="/v1/businesses", tags=["Business"])


@businessRouter.post("/search")
@inject
async def search(
    query: SearchBusinessRequest,
    service: BusinessService = Depends(Provide[Container.business_service]),
):
    # coreQuery = BusinessListQuery(
    #     day_filter=Day.MONDAY,
    #     status=BusinessStatus.DRAFT,
    #     min_opening_time=time(10, 0, 0),
    #     max_closing_time=time(23, 59, 59),
    #     page_size=10,
    #     page_number=2,
    # )
    coreQuery = BusinessSearchQuery()
    business = service.get_all(coreQuery)
    print("Database connectivity test successful:", list(business))
    return Response(
        content="Hey, ba7besh started here!", status_code=status.HTTP_200_OK
    )
