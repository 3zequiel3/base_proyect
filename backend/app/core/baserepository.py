"""Simple generic CRUD repository for SQLModel models."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Generic, TypeVar, cast

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.core.basemodel import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)


class BaseRepository(Generic[ModelType]):
    """Base repository for each module.

    Usage in a module:
        class UserRepository(BaseRepository[User]):
            model = User
    """

    model: type[ModelType]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    def add(self, entity: ModelType) -> None:
        self.session.add(entity)

    async def create(self, data: Mapping[str, Any] | ModelType) -> ModelType:
        entity = data if isinstance(data, self.model) else self.model(**dict(data))
        entity = cast(ModelType, entity)
        self.add(entity)
        await self.session.flush()
        await self.session.refresh(entity)
        return entity

    async def get_by_id(self, entity_id: int) -> ModelType | None:
        result = await self.session.execute(
            select(self.model).where(
                self.model.id == entity_id,
                self.model.deleted_at.is_(None),
            )
        )
        return result.scalar_one_or_none()

    async def list_active(self) -> list[ModelType]:
        result = await self.session.execute(
            select(self.model).where(self.model.deleted_at.is_(None))
        )
        return list(result.scalars().all())

    async def update(self, entity_id: int, data: Mapping[str, Any]) -> ModelType | None:
        entity = await self.get_by_id(entity_id)
        if entity is None:
            return None

        for field, value in data.items():
            if field in {"id", "created_at", "updated_at", "deleted_at"}:
                continue
            if hasattr(entity, field):
                setattr(entity, field, value)

        self.add(entity)
        await self.session.flush()
        await self.session.refresh(entity)
        return entity

    async def delete(self, entity_id: int) -> bool:
        entity = await self.get_by_id(entity_id)
        if entity is None:
            return False

        entity.mark_deleted()
        self.add(entity)
        await self.session.flush()
        await self.session.refresh(entity)
        return True
