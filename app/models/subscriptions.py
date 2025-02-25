from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base
from app.models.utils import TimestampModelMixin

if TYPE_CHECKING:
    from app.models import User


class Subscription(TimestampModelMixin, Base):
    __tablename__ = "subscription"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"), nullable=False)
    author_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"), nullable=False)

    user: Mapped[User] = relationship("User", foreign_keys="Subscription.user_id", back_populates="subscriptions")
    author: Mapped[User] = relationship("User", foreign_keys="Subscription.author_id", back_populates="subscribers")

    __table_args__ = (UniqueConstraint('user_id', 'author_id', name='one_subscription_from_user_to_author'),)

    def __repr__(self) -> str:
        return f"Subscription(id={self.id!r}, user_id={self.user_id!r}, author_id={self.author_id!r})"
