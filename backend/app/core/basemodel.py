"""Base SQLModel definitions shared by all persisted entities.

This module is intentionally small and domain-neutral because this repository is
meant to be forked. Concrete projects should inherit ``BaseModel`` with
``table=True`` and add domain fields in their own modules.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, ClassVar

from sqlalchemy import BigInteger, Column, DateTime, MetaData, func
from sqlalchemy.orm import declared_attr
from sqlmodel import Field, SQLModel


NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


SQLMODEL_METADATA = MetaData(naming_convention=NAMING_CONVENTION)
SQLModel.metadata = SQLMODEL_METADATA


def utc_now() -> datetime:
    """Return an aware UTC datetime for app-managed timestamps."""

    return datetime.now(timezone.utc)


class Base(SQLModel):
    """Project SQLModel base with deterministic constraint names."""

    metadata: ClassVar[MetaData] = SQLMODEL_METADATA


class BaseModel(Base):
    """Base model with BIGSERIAL id, audit timestamps, and soft delete.

    PostgreSQL ``BIGSERIAL`` is represented through a SQLAlchemy ``BigInteger``
    primary key with autoincrement. ``created_at`` and ``updated_at`` are managed
    by the database; ``deleted_at`` is nullable and used by repositories for
    soft-delete semantics.
    """

    id: int | None = Field(
        default=None,
        sa_column=Column(
            BigInteger,
            primary_key=True,
            autoincrement=True,
            index=True,
        ),
    )
    created_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            server_default=func.now(),
        ),
    )
    updated_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            server_default=func.now(),
            onupdate=func.now(),
        ),
    )
    deleted_at: datetime | None = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), nullable=True),
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """Default table name: lowercase class name plus ``s``."""

        return f"{cls.__name__.lower()}s"

    def mark_deleted(self) -> None:
        """Mark the entity as softly deleted."""

        self.deleted_at = utc_now()

    def to_dict(self) -> dict[str, Any]:
        """Return a plain dict with model values."""

        if hasattr(self, "model_dump"):
            return self.model_dump()
        return self.dict()

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(id={self.id})>"
