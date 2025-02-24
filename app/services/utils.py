from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import Base


async def create_object(obj: Base, db_session: AsyncSession):
    db_session.add(obj)

    try:
        await db_session.commit()
        await db_session.refresh(obj)
    except IntegrityError as exc:
        await db_session.rollback()
        raise HTTPException(status_code=400, detail=f"Error while creating {str(obj)}") from exc

    return obj
