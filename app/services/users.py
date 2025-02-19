import contextlib

from fastapi_users.exceptions import UserAlreadyExists

from app.db import get_async_session
from app.models.users import get_user_db, get_user_manager
from app.schemas.users import UserCreate

get_async_session_context = contextlib.asynccontextmanager(get_async_session)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def create_user(email: str, password: str, is_superuser: bool = False, is_verified: bool = False):
    try:
        async with (
            get_async_session_context() as session,
            get_user_db_context(session) as user_db,
            get_user_manager_context(user_db) as user_manager,
        ):
            user = await user_manager.create(
                UserCreate(email=email, password=password, is_superuser=is_superuser, is_verified=is_verified)
            )
            return user
    except UserAlreadyExists:
        raise
