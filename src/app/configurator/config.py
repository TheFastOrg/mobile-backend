import os
from typing import Callable, Optional, Literal

from dotenv import load_dotenv
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_ENV: Literal["dev", "staging", "prod", "local"] = "dev"
    API_DESCRIPTION: str = (
        "Ba7besh Back-End API for the mobile app,"
        + "it will be used privately by the ba7besh mobile "
        "app"
    )
    API_TITLE: str = "Ba7besh API"
    API_VERSION: str = "1.0"
    USE_IN_MEMORY_DB: bool = bool(os.getenv("USE_IN_MEMORY_DB", True))
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: Optional[str] = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "postgres")
    POSTGRES_SCHEMA: str = os.getenv("POSTGRES_SCHEMA", "public")
    DATABASE_URL: PostgresDsn | str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}?options=-csearch_path={POSTGRES_SCHEMA}"

    @staticmethod
    def _configure_initial_settings() -> Callable[[], "Settings"]:
        load_dotenv()
        settings = Settings()

        def fn() -> Settings:
            return settings

        return fn


get_settings = Settings._configure_initial_settings()
