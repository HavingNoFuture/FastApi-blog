import uuid

from pydantic import BaseModel

from app.schemas.users import UserPreview


class SubscriptionPreviewScheme(BaseModel):
    id: int


class SubscriptionCreateScheme(BaseModel):
    author_id: uuid.UUID


class SubscriptionReadScheme(SubscriptionPreviewScheme):
    author: UserPreview


class SubscriptionListScheme(BaseModel):
    total_count: int
    subscriptions: list[SubscriptionReadScheme]
