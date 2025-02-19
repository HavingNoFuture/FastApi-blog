import uuid

from fastapi_users import FastAPIUsers

from app.auth_backend import auth_backend
from app.models.users import User, get_user_manager
from app.schemas.users import UserCreate, UserRead

fastapi_users_component = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

register_router = fastapi_users_component.get_register_router(UserRead, UserCreate)
auth_router = fastapi_users_component.get_auth_router(auth_backend)
pass_reset_router = fastapi_users_component.get_reset_password_router()
verify_router = fastapi_users_component.get_verify_router(UserRead)
