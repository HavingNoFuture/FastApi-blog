from fastapi import APIRouter, Depends
from fastapi_users import fastapi_users
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db import get_async_session
from app.models.users import User, get_user_manager
from app.routes.auth import fastapi_users_component
from app.schemas.users import UserRead, UserUpdate
from app.urls import API_URL

user_router = APIRouter()


user_router.include_router(
    fastapi_users.get_users_router(get_user_manager, UserRead, UserUpdate, fastapi_users_component.authenticator),
    prefix=API_URL + "/users",
    tags=["users"],
)


@user_router.get("/users/")
async def get_users(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(User))
    return result.scalars().all()
