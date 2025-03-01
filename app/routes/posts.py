from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.params import Query
from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db import get_async_session
from app.models import Post, Rating, User
from app.schemas.posts import PostCreateScheme, PostListScheme, PostReadScheme, PostUpdateScheme
from app.services.users import get_current_user
from app.services.utils import create_object, delete_object
from app.urls import POSTS_URL

posts_router = APIRouter(
    prefix=POSTS_URL,
    tags=["posts"],
)


@posts_router.post("/", response_model=PostReadScheme)
async def create_post(
    post_data: PostCreateScheme,
    db_session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    obj = Post(header=post_data.header, content=post_data.content, author=current_user)
    return await create_object(obj, db_session)


@posts_router.get("/", response_model=list[PostListScheme])
async def get_all_posts(
    order_by: str = Query("-created_at", description="created_at/-created_at"),
    db_session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    ordering_field = desc(Post.created_at) if order_by.startswith("-") else Post.created_at

    has_voted_subquery = (
        select(func.count(Rating.id))
        .where(Rating.post_id == Post.id, Rating.user_id == current_user.id)
        .correlate(Post)
        .scalar_subquery()
    )

    query = (
        select(
            Post,
            func.coalesce(func.avg(Rating.score), 0).label("average_rating"),
            func.count(Rating.id.distinct()).label("votes_count"),
            has_voted_subquery.label("has_voted"),
        )
        .outerjoin(Rating, Post.id == Rating.post_id)
        .group_by(Post.id)
        .order_by(ordering_field)
        .options(selectinload(Post.author))
    )

    result = await db_session.execute(query)
    return [
        {
            **jsonable_encoder(post),
            "average_rating": average_rating,
            "votes_count": votes_count,
            "has_voted": bool(has_voted),
        }
        for post, average_rating, votes_count, has_voted in result.all()
    ]


@posts_router.get("/{post_id}", response_model=PostReadScheme)
async def get_post(post_id: int, db_session: AsyncSession = Depends(get_async_session)):
    return await async_get_post(post_id, db_session)


@posts_router.patch("/{post_id}", response_model=PostReadScheme)
async def update_post(
    post_id: int,
    post_data: PostUpdateScheme,
    db_session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    post = await async_get_post(post_id, db_session)

    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only author can update")

    for key, value in post_data.model_dump(exclude_unset=True).items():
        setattr(post, key, value)

    await db_session.commit()
    await db_session.refresh(post)
    return post


@posts_router.delete("/{post_id}", status_code=204)
async def delete_post(
    post_id: int,
    db_session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    post = await async_get_post(post_id, db_session)

    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only author can update")

    await delete_object(post, db_session)

    return None


async def async_get_post(post_id: int, db_session: AsyncSession) -> Post:
    query = select(Post).where(Post.id == post_id).options(selectinload(Post.author))
    result = await db_session.execute(query)
    post = result.scalars().first()

    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    return post
