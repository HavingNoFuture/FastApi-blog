from datetime import UTC, datetime, timedelta
from typing import NoReturn

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from app.db import get_async_session
from app.models import Comment, User
from app.routes.posts import async_get_post
from app.schemas.comments import CommentCreateScheme, CommentReadScheme, CommentReadTreeScheme, CommentUpdateScheme
from app.services.users import get_current_user
from app.services.utils import create_object, delete_object
from app.urls import POSTS_URL

comments_router = APIRouter(
    prefix=POSTS_URL + "/{post_id}",
    tags=["comments"],
)

COMMENT_URL = "/comments"


@comments_router.post(COMMENT_URL, response_model=CommentReadScheme)
async def create_comment(
    post_id: int,
    comment_data: CommentCreateScheme,
    db_session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    post = await async_get_post(post_id, db_session)

    obj = Comment(text=comment_data.text, author=current_user, post=post, parent_id=comment_data.parent_id)
    return await create_object(obj, db_session)


@comments_router.get(COMMENT_URL, response_model=list[CommentReadTreeScheme])
async def get_comments(
    post_id: int,
    db_session: AsyncSession = Depends(get_async_session),
):
    query = (
        select(Comment).where(Comment.post_id == post_id).order_by(Comment.id.asc()).options(joinedload(Comment.author))
    )
    result = await db_session.execute(query)
    comments = result.scalars().all()

    # build comment tree
    id_to_comment = {}
    data = []
    for comment in comments:
        comment_dict = jsonable_encoder(comment)
        comment_dict['replies'] = []

        id_to_comment[comment_dict['id']] = comment_dict

        parent_id = comment.parent_id
        if not parent_id:
            data.append(comment_dict)
        else:
            id_to_comment[parent_id]['replies'].append(comment_dict)
    return data


@comments_router.patch(COMMENT_URL + "/{comment_id}", response_model=CommentReadScheme)
async def update_comment(
    post_id: int,
    comment_id: int,
    comment_data: CommentUpdateScheme,
    db_session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    comment = await async_get_comment(comment_id, post_id, db_session)

    check_can_update_comment(comment, current_user)

    for key, value in comment_data.model_dump(exclude_unset=True).items():
        setattr(comment, key, value)

    await db_session.commit()
    await db_session.refresh(comment)
    return comment


@comments_router.delete(COMMENT_URL + "/{comment_id}", status_code=204)
async def delete_comment(
    post_id: int,
    comment_id: int,
    db_session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    comment: Comment = await async_get_comment(comment_id, post_id, db_session)

    check_can_update_comment(comment, current_user)

    await delete_object(comment, db_session)

    return None


async def async_get_comment(comment_id: int, post_id: int, db_session: AsyncSession) -> Comment:
    query = (
        select(Comment)
        .where(
            Comment.id == comment_id,
            Comment.post_id == post_id,
        )
        .options(selectinload(Comment.author))
    )
    result = await db_session.execute(query)
    comment = result.scalars().first()

    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")

    return comment


def check_can_update_comment(comment: Comment, current_user: User) -> NoReturn | HTTPException:
    """
    Check if the current user is allowed to update the given comment.

    The user can update the comment if he is the author and the comment was created within the last 30 minutes.
    """
    now = datetime.now(UTC)
    comment_update_deadline = comment.created_at + timedelta(minutes=30)
    if not comment.author_id == current_user.id and now < comment_update_deadline:
        raise HTTPException(status_code=403, detail="Can't update comment")
