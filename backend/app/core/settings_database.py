"""Environment settings for the backend database and app metadata."""

from __future__ import annotations

from pathlib import Path

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL


BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    """Application settings loaded from environment variables or `.env`."""

    app_name: str = "Base Project API"
    app_version: str = "0.1.0"
    app_env: str = "development"

    db_user: str = "postgres"
    db_password: str = "postgres"
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "base_project"
    db_echo: bool = False
    db_create_database: bool = False
    db_create_tables: bool = False

    database_url: str | None = None
    sync_database_url: str | None = None
    master_database_url: str | None = None

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @computed_field
    @property
    def async_database_url(self) -> str:
        if self.database_url:
            return self.database_url
        return str(
            URL.create(
                "postgresql+asyncpg",
                username=self.db_user,
                password=self.db_password,
                host=self.db_host,
                port=self.db_port,
                database=self.db_name,
            ).render_as_string(hide_password=False)
        )

    @computed_field
    @property
    def resolved_sync_database_url(self) -> str:
        if self.sync_database_url:
            return self.sync_database_url
        return str(
            URL.create(
                "postgresql+psycopg",
                username=self.db_user,
                password=self.db_password,
                host=self.db_host,
                port=self.db_port,
                database=self.db_name,
            ).render_as_string(hide_password=False)
        )

    @computed_field
    @property
    def resolved_master_database_url(self) -> str:
        if self.master_database_url:
            return self.master_database_url
        return str(
            URL.create(
                "postgresql+psycopg",
                username=self.db_user,
                password=self.db_password,
                host=self.db_host,
                port=self.db_port,
                database="postgres",
            ).render_as_string(hide_password=False)
        )


settings = Settings()
