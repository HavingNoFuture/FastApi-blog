from fastapi import APIRouter, Depends
from fastapi_users import fastapi_users
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db import get_async_session
from app.models.users import User, get_user_manager
from app.routes.auth import fastapi_users_component
from app.schemas.users import UserRead, UserUpdate
from app.services.users import get_current_user
from app.urls import USERS_URL

router_kwargs = {
    'prefix': USERS_URL,
    'tags': ["users"],
}

user_router = APIRouter(**router_kwargs)


user_router.include_router(
    fastapi_users.get_users_router(get_user_manager, UserRead, UserUpdate, fastapi_users_component.authenticator),
    **router_kwargs,
)


@user_router.get("/current_user", response_model=UserRead)
async def get_current_user(current_user: User = Depends(get_current_user)):
    return current_user


@user_router.get("/")
async def get_users(session: AsyncSession = Depends(get_async_session)):
    # todo: delete after testing
    result = await session.execute(select(User))
    return result.scalars().all()
