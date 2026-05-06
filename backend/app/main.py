"""FastAPI application entrypoint."""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.database import (
    create_database_if_not_exists,
    create_db_and_tables,
    dispose_engine,
)
from app.core.settings_database import settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Application startup/shutdown hook.

    Keep this simple in the base project. Forks can initialize shared resources
    here, for example database engines, caches, background clients, etc.
    """

    if settings.db_create_database:
        create_database_if_not_exists()
    if settings.db_create_tables:
        await create_db_and_tables()

    yield

    await dispose_engine()


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)


@app.get("/health", tags=["health"])
async def health_check() -> dict[str, str]:
    return {"status": "ok"}
