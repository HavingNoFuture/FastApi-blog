from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

from app.config import settings


engine = create_async_engine(settings.DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
Base = declarative_base()

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
