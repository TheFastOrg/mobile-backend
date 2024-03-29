from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from src.app.configurator.config import get_settings
from src.app.configurator.containers import Container
from src.app.endpoints.root import rootRouter
from src.app.endpoints.v1.business import businessRouter
from fastapi.middleware.gzip import GZipMiddleware


def create_app() -> FastAPI:
    settings = get_settings()
    fast_api_app = FastAPI(
        title=settings.API_TITLE,
        version=settings.API_VERSION,
        openapi_tags=[{"name": "Business"}],
        openapi_url=None if settings.APP_ENV == "prod" else "/openapi.json",
    )
    fast_api_app.add_middleware(GZipMiddleware)
    if settings.APP_ENV == "prod":
        fast_api_app.add_middleware(HTTPSRedirectMiddleware)
    fast_api_app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])
    fast_api_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    fast_api_app.include_router(rootRouter)
    fast_api_app.include_router(businessRouter)
    Container()
    return fast_api_app


app = create_app()
