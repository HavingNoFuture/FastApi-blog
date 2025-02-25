from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base
from app.models.utils import TimestampModelMixin

if TYPE_CHECKING:
    from app.models import User


class Post(TimestampModelMixin, Base):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True)
    header: Mapped[str] = mapped_column(String(120), nullable=False)
    content: Mapped[str] = mapped_column(Text(), nullable=False)
    author_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"), nullable=False)

    author: Mapped[User] = relationship(back_populates="posts")

    comments = relationship("Comment", back_populates="post")

    def __repr__(self) -> str:
        return f"Post(id={self.id!r}, header={self.header!r}, text={self.content!r})"
