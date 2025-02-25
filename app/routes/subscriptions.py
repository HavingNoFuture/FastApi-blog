import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import exists, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.db import get_async_session
from app.models import Subscription, User
from app.schemas.subscriptions import SubscriptionCreateScheme, SubscriptionListScheme, SubscriptionReadScheme
from app.services.users import get_current_user
from app.services.utils import create_object
from app.urls import USERS_URL

subscriptions_router = APIRouter(
    prefix=USERS_URL,
    tags=["subscriptions"],
)


@subscriptions_router.post("/current_user/subscriptions", response_model=SubscriptionReadScheme)
async def create_subscription(
    subscription_data: SubscriptionCreateScheme,
    db_session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    query = select(
        exists().where(Subscription.user == current_user, Subscription.author_id == subscription_data.author_id)
    )
    result = await db_session.execute(query)
    is_subscribed = result.scalars()

    if is_subscribed:
        raise HTTPException(status_code=400, detail="User is already subscribed to the author")

    obj = Subscription(user=current_user, author_id=subscription_data.author_id)
    return await create_object(obj, db_session)


@subscriptions_router.get("/{user_id}/subscriptions", response_model=SubscriptionListScheme)
async def get_subscriptions(
    user_id: uuid.UUID,
    db_session: AsyncSession = Depends(get_async_session),
):
    query = (
        select(Subscription)
        .where(Subscription.user_id == user_id)
        .order_by(Subscription.created_at.desc())
        .options(joinedload(Subscription.author))
    )
    result = await db_session.execute(query)
    subscriptions = result.scalars().all()

    query = select(func.count()).where(Subscription.user_id == user_id)
    total_count = await db_session.scalar(query)

    return {'total_count': total_count, 'subscriptions': subscriptions}


@subscriptions_router.delete("/current_user/subscriptions/{subscription_id}", status_code=204)
async def delete_subscription(
    subscription_id: int,
    db_session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    query = select(Subscription).where(Subscription.id == subscription_id, Subscription.user == current_user)
    result = await db_session.execute(query)
    subscription = result.scalars().first()

    if subscription is None:
        raise HTTPException(status_code=404, detail="Subscription not found")

    await db_session.delete(subscription)
    await db_session.commit()

    return None
