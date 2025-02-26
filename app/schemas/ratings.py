import uuid

from pydantic import BaseModel

from app.models.ratings import RatingScore


class RatingBaseScheme(BaseModel):
    score: RatingScore


class RatingCreateScheme(RatingBaseScheme):
    pass


class RatingReadScheme(RatingBaseScheme):
    user_id: uuid.UUID
    post_id: int
