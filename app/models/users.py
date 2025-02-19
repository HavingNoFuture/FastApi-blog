import uuid

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, UUIDIDMixin
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.db import Base, get_async_session


class User(SQLAlchemyBaseUserTableUUID, Base):
    pass


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
