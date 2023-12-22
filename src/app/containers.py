"""Containers module."""
import os

from dependency_injector import containers, providers

from src.app.db.manager import Database
from src.app.db.repositories.business_repository import DBBusinessRepository
from src.core.services.business_service import BusinessService

DB_HOST = os.environ["POSTGRES_HOST"]
DB_NAME = os.environ["POSTGRES_DATABASE"]
DB_USER = os.environ["POSTGRES_USERNAME"]
DB_PASSWORD = os.environ["POSTGRES_PASSWORD"]


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["src.app.endpoints"])
    config = providers.Configuration(yaml_files=["config.yml"])
    db_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    db = providers.Singleton(Database, db_url=db_url)

    business_repository = providers.Factory(
        DBBusinessRepository,
        session_factory=db.provided.session,
    )

    business_service = providers.Factory(
        BusinessService,
        business_repository=business_repository,
    )
