from fastapi import APIRouter

from src.app.configurator.config import get_settings
from src.app.dtos.health_check import HealthCheckModel

rootRouter = APIRouter()


@rootRouter.get(
    "/status",
    response_model=HealthCheckModel,
    tags=["Health Check"],
    summary="Performs health check",
    description="Performs health check and returns information about running service.",
)
def health_check():
    settings = get_settings()
    return HealthCheckModel(
        title=settings.API_TITLE,
        description=settings.API_DESCRIPTION,
        version=settings.API_VERSION,
        status="OK",
    )
