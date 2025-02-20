import datetime

from pydantic import BaseModel

from app.schemas.users import UserPreview


class PostBaseScheme(BaseModel):
    header: str
    content: str


class PostCreateScheme(PostBaseScheme):
    pass


class PostReadScheme(PostBaseScheme):
    id: int
    author: UserPreview
    created_at: datetime.datetime
    updated_at: datetime.datetime


class PostUpdateScheme(PostBaseScheme):
    pass
