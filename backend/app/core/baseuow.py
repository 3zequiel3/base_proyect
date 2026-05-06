"""Simple async Unit of Work.

Flow:
    Router -> Service -> UnitOfWork -> Repository -> Model/DB

Designed to stay very close to the food_store version:
- open one session on enter;
- commit automatically if the block succeeds;
- rollback if the block fails or commit fails;
- close the session always;
- expose ``refresh``.

The only difference is that this base is async and receives the session factory
instead of importing a project-specific engine, so forks can wire their own DB.
"""

from __future__ import annotations

from types import TracebackType
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class UnitOfWork:
    """Context manager that owns one database transaction."""

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory
        self.session: AsyncSession | None = None

    async def __aenter__(self) -> "UnitOfWork":
        self.session = self._session_factory()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if self.session is None:
            return

        try:
            if exc_type is None:
                await self.session.commit()
            else:
                await self.session.rollback()
        except Exception:
            await self.session.rollback()
            raise
        finally:
            await self.session.close()
            self.session = None

    async def refresh(self, instance: Any) -> None:
        if self.session is None:
            raise RuntimeError("UnitOfWork must be used inside 'async with'")
        await self.session.refresh(instance)
