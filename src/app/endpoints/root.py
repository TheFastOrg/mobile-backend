from fastapi import APIRouter, status, Response

from src.app.configurator.config import get_settings
from src.app.dtos.health_check import HealthCheckModel

rootRouter = APIRouter()


@rootRouter.get(
    "/status",
    response_model=HealthCheckModel,
    status_code=status.HTTP_200_OK,
    tags=["Health Check"],
    summary="Performs health check",
    description="Performs health check and returns information about running service.",
)
def health_check():
    settings = get_settings()
    return Response(
        content=HealthCheckModel(
            title=settings.API_TITLE,
            description=settings.API_DESCRIPTION,
            version=settings.API_VERSION,
            status="OK",
        ).model_dump_json(),
        media_type="application/json",
        status_code=status.HTTP_200_OK,
    )
