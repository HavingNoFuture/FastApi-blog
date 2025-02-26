from __future__ import annotations

import enum
import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base
from app.models.utils import EnumAsInteger, TimestampModelMixin

if TYPE_CHECKING:
    from app.models import Post, User


class RatingScore(enum.IntEnum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5


class Rating(TimestampModelMixin, Base):
    __tablename__ = "rating"

    id: Mapped[int] = mapped_column(primary_key=True)
    score: Mapped[RatingScore] = mapped_column(EnumAsInteger(RatingScore), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"), nullable=False)

    post: Mapped[Post] = relationship(back_populates="ratings")
    user: Mapped[User] = relationship(back_populates="ratings")

    __table_args__ = (UniqueConstraint("user_id", "post_id", name="unique_user_post_rating"),)

    def __repr__(self) -> str:
        return f"Rating(id={self.id!r}, score={self.score!r}, post_id={self.post_id!r})"
