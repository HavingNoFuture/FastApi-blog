from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base
from app.models.utils import TimestampModelMixin

if TYPE_CHECKING:
    from app.models import Post, User


class Comment(TimestampModelMixin, Base):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(Text(), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("comment.id"), nullable=True)

    author: Mapped[User] = relationship(back_populates="comments")
    post: Mapped[Post] = relationship(back_populates="comments")

    parent: Mapped[Comment | None] = relationship(back_populates="replies", remote_side="Comment.id")

    replies: Mapped[list[Comment]] = relationship("Comment", back_populates="parent", lazy="selectin")

    def __repr__(self) -> str:
        return f"Comment(id={self.id!r}, text={self.text!r}, post_id={self.post_id!r})"
