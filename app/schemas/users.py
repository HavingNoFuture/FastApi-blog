import uuid

from fastapi_users import schemas
from pydantic import BaseModel, EmailStr


class UserPreview(BaseModel):
    email: EmailStr


class UserRead(schemas.BaseUser[uuid.UUID]):
    pass


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass
