from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_async_session
from app.models import Post, Rating, User
from app.routes.posts import async_get_post
from app.schemas.ratings import RatingCreateScheme, RatingReadScheme
from app.services.users import get_current_user
from app.services.utils import create_object, delete_object
from app.urls import POSTS_URL

ratings_router = APIRouter(
    prefix=POSTS_URL,
    tags=["post_rating"],
)


@ratings_router.post(POSTS_URL + '/{post_id}/rating', response_model=RatingReadScheme)
async def create_rating(
    post_id: int,
    rating_data: RatingCreateScheme,
    db_session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    post = await async_get_post(post_id, db_session)

    query = select(exists().where(Rating.user == current_user, Rating.post == post))
    result = await db_session.execute(query)
    rating_exists = result.scalar()

    if rating_exists:
        raise HTTPException(status_code=400, detail="User is already rate the post")

    obj = Rating(score=rating_data.score, user=current_user, post=post)
    return await create_object(obj, db_session)


@ratings_router.delete(POSTS_URL + "/{post_id}/rating", status_code=204)
async def delete_rating(
    post_id: int,
    db_session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    post = await async_get_post(post_id, db_session)
    rating = await get_rating(post, current_user, db_session)

    await delete_object(rating, db_session)

    return None


async def get_rating(post: Post, user: User, db_session: AsyncSession) -> Rating | None:
    query = select(Rating).where(Rating.post == post, Rating.user == user)
    result = await db_session.execute(query)
    rating = result.scalars().first()

    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")

    return rating
