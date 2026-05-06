"""Simple generic CRUD service."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Generic, TypeVar

from app.core.basemodel import BaseModel
from app.core.baserepository import BaseRepository
from app.core.baseuow import UnitOfWork

ModelType = TypeVar("ModelType", bound=BaseModel)
RepositoryType = TypeVar("RepositoryType", bound=BaseRepository[Any])


class BaseService(Generic[ModelType, RepositoryType]):
    """Base service for each module.

    Usage in a module:
        class UserService(BaseService[User, UserRepository]):
            def __init__(self, uow: UnitOfWork):
                super().__init__(uow, UserRepository)
    """

    def __init__(self, uow: UnitOfWork, repository_class: type[RepositoryType]) -> None:
        self.uow = uow
        self.repository_class = repository_class

    def _repository(self, uow: UnitOfWork) -> RepositoryType:
        if uow.session is None:
            raise RuntimeError("UnitOfWork must be used inside 'async with'")
        return self.repository_class(uow.session)

    async def create(self, data: Mapping[str, Any] | ModelType) -> ModelType:
        async with self.uow as uow:
            return await self._repository(uow).create(data)

    async def get_by_id(self, entity_id: int) -> ModelType | None:
        async with self.uow as uow:
            return await self._repository(uow).get_by_id(entity_id)

    async def list_active(self) -> list[ModelType]:
        async with self.uow as uow:
            return await self._repository(uow).list_active()

    async def update(self, entity_id: int, data: Mapping[str, Any]) -> ModelType | None:
        async with self.uow as uow:
            return await self._repository(uow).update(entity_id, data)

    async def delete(self, entity_id: int) -> bool:
        async with self.uow as uow:
            return await self._repository(uow).delete(entity_id)
