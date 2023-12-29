"""Containers module."""
import os

from dependency_injector import containers, providers

from src.app.db.manager import Database
from src.app.db.repositories.business_repository import DBBusinessRepository
from src.app.db.repositories.business_repository_memory import (
    InMemoryBusinessRepository,
)
from src.core.services.business_service import BusinessService

USE_IN_MEMORY_DB = os.environ.get("USE_IN_MEMORY_DB", False)


def _get_business_repository():
    if USE_IN_MEMORY_DB:
        return InMemoryBusinessRepository()
    db_host = os.environ.get("POSTGRES_HOST", None)
    db_name = os.environ["POSTGRES_DATABASE"]
    db_user = os.environ["POSTGRES_USERNAME"]
    db_password = os.environ["POSTGRES_PASSWORD"]
    db_url = f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}"
    db = providers.Singleton(Database, db_url=db_url)

    business_repository = providers.Factory(
        DBBusinessRepository,
        session_factory=db.provided.session,
    )
    return business_repository


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["src.app.endpoints"])
    config = providers.Configuration(yaml_files=["config.yml"])

    business_service = providers.Factory(
        BusinessService,
        business_repository=_get_business_repository(),
    )
