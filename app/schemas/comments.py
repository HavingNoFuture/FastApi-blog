import datetime

from pydantic import BaseModel

from app.schemas.users import UserPreview


class CommentBaseScheme(BaseModel):
    text: str


class CommentCreateScheme(CommentBaseScheme):
    parent_id: int | None


class CommentUpdateScheme(CommentBaseScheme):
    pass


class CommentReadScheme(CommentBaseScheme):
    id: int
    post_id: int
    author: UserPreview
    created_at: datetime.datetime
    updated_at: datetime.datetime


class CommentReadTreeScheme(CommentReadScheme):
    replies: list['CommentReadScheme']
