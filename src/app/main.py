import os

from fastapi import FastAPI

from src.app import endpoints
from src.app.containers import Container

USE_IN_MEMORY_DB = os.environ.get("USE_IN_MEMORY_DB", False)


def create_app() -> FastAPI:
    container = Container()
    if not USE_IN_MEMORY_DB:
        db = container.db()
        db.create_database()

    fast_api_app = FastAPI()
    # app.container = container
    fast_api_app.include_router(endpoints.router)
    return fast_api_app


app = create_app()
