import os
from typing import Callable, Optional

from dotenv import load_dotenv
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENV: str = "dev"
    API_DESCRIPTION: str = (
        "Ba7besh Back-End API for the mobile app, it will be used privately by the ba7besh mobile "
        "app"
    )
    API_TITLE: str = "Ba7besh API"
    API_VERSION: str = "1.0"
    USE_IN_MEMORY_DB: bool = False
    POSTGRES_USERNAME: str = os.getenv("POSTGRES_USERNAME", "postgres")
    POSTGRES_PASSWORD: Optional[str] = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DATABASE: str = os.getenv("POSTGRES_DATABASE", "ba7besh")
    DATABASE_URL: PostgresDsn | str = f"postgresql://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"


def _configure_initial_settings() -> Callable[[], Settings]:
    load_dotenv()
    settings = Settings()

    def fn() -> Settings:
        return settings

    return fn


get_settings = _configure_initial_settings()
