"""Containers module."""

from dependency_injector import containers, providers

from src.app.configurator.config import get_settings
from src.app.db.manager import Database
from src.app.db.repositories.business_repository import DBBusinessRepository
from src.app.db.repositories.business_repository_memory import (
    InMemoryBusinessRepository,
)
from src.core.services.business_service import BusinessService

settings = get_settings()


def _get_business_repository():
    if settings.USE_IN_MEMORY_DB:
        return providers.Factory(InMemoryBusinessRepository)
    db = providers.ThreadSafeSingleton(Database, db_url=settings.DATABASE_URL)

    business_repository = providers.Factory(
        DBBusinessRepository,
        session_factory=db.provided.session,
    )
    return business_repository


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["src.app"])

    business_service = providers.Factory(
        BusinessService,
        business_repository=_get_business_repository(),
    )
