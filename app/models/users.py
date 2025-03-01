from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, UUIDIDMixin
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, relationship

from app.config import settings
from app.db import Base, get_async_session

if TYPE_CHECKING:
    from app.models import Subscription


class User(SQLAlchemyBaseUserTableUUID, Base):
    posts = relationship(
        "Post",
        back_populates="author",
        cascade="all, delete-orphan",
    )
    comments = relationship(
        "Comment",
        back_populates="author",
        cascade="all, delete-orphan",
    )
    subscriptions: Mapped[Subscription] = relationship(
        "Subscription",
        foreign_keys="Subscription.user_id",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    subscribers = relationship(
        "Subscription",
        foreign_keys="Subscription.author_id",
        back_populates="author",
        cascade="all, delete-orphan",
    )
    ratings = relationship(
        "Rating",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"User(email={self.email!r}, is_active={self.is_active!r}, is_superuser={self.is_superuser!r}"


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = settings.SECRET_KEY
    verification_token_secret = settings.SECRET_KEY

    # region hooks

    async def on_after_register(self, user: User, request: Request | None = None):
        pass

    async def on_after_forgot_password(self, user: User, token: str, request: Request | None = None):
        pass

    async def on_after_request_verify(self, user: User, token: str, request: Request | None = None):
        pass

    # endregion hooks


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
