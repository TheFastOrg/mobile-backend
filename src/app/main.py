from fastapi import FastAPI

from src.app.configurator.config import get_settings
from src.app.containers import Container
from src.app.endpoints.root import rootRouter
from src.app.endpoints.v1.business import businessRouter


def create_app() -> FastAPI:
    settings = get_settings()
    container = Container()
    if not settings.USE_IN_MEMORY_DB:
        db = container.db()
        db.create_database()

    fast_api_app = FastAPI(
        title=settings.API_TITLE,
        version=settings.API_VERSION,
        openapi_tags=[{"name": "Business"}],
    )
    # app.container = container
    fast_api_app.include_router(rootRouter)
    fast_api_app.include_router(businessRouter)
    return fast_api_app


app = create_app()
