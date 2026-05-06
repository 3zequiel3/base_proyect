"""Database configuration for SQLModel + PostgreSQL."""

from __future__ import annotations

import re
from collections.abc import AsyncIterator

from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlmodel import SQLModel

from app.core.settings_database import settings


engine: AsyncEngine = create_async_engine(
    settings.async_database_url,
    echo=settings.db_echo,
)
SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


def create_database_if_not_exists() -> None:
    """Create the configured PostgreSQL database if it does not exist.

    This is useful for local development. In production, prefer migrations and
    database provisioning outside the app process.
    """

    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", settings.db_name):
        raise ValueError("DB_NAME must contain only letters, numbers, and underscores")

    master_engine = create_engine(
        settings.resolved_master_database_url,
        echo=False,
        isolation_level="AUTOCOMMIT",
    )

    try:
        with master_engine.connect() as conn:
            exists = conn.execute(
                text("SELECT 1 FROM pg_database WHERE datname = :name"),
                {"name": settings.db_name},
            ).scalar()
            if not exists:
                quoted_db_name = conn.dialect.identifier_preparer.quote(settings.db_name)
                conn.execute(text(f"CREATE DATABASE {quoted_db_name}"))
    finally:
        master_engine.dispose()


async def create_db_and_tables() -> None:
    """Create SQLModel tables registered in metadata.

    Import module models before calling this function in a fork so SQLModel has
    all tables registered. For real projects, Alembic migrations are preferred.
    """

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def dispose_engine() -> None:
    await engine.dispose()


async def get_session() -> AsyncIterator[AsyncSession]:
    async with SessionLocal() as session:
        yield session
