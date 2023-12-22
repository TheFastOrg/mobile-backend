"""Endpoints module."""

from datetime import time

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Response, status

from src.core.entities.business.queries import BusinessListQuery
from src.core.services.business_service import BusinessService

from .containers import Container

router = APIRouter()


@router.post("/search")
@inject
async def search(
    service: BusinessService = Depends(Provide[Container.business_service]),
):
    query = BusinessListQuery(
        day_filter=1,
        status="draft",
        min_opening_time=time(10, 0, 0),
        max_closing_time=time(23, 59, 59),
        page_size=10,
        page_number=2,
    )
    business = service.get_all(query)
    print("Database connectivity test successful:", list(business))
    return Response(
        content="Hey, ba7besh started here!", status_code=status.HTTP_200_OK
    )


@router.get("/status")
def get_status():
    return {"status": "OK"}
