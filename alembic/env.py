import asyncio
import logging
from logging.config import fileConfig

from alembic import context
from asyncpg import Connection
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config, create_async_engine

from app.config import settings
from app.db import Base

from app.models import *  # noqa

config = context.config

# Логирование Alembic
if config.config_file_name:
    fileConfig(config.config_file_name)
logger = logging.getLogger("alembic")

target_metadata = Base.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode.
    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.
    Calls to context.execute() here emit the given string to the
    script output.
    """
    context.configure(
        url=settings.DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Run migrations in 'online' mode.
    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    # configuration = config.get_section(config.config_ini_section)
    # configuration["sqlalchemy.url"] = settings.DATABASE_URL
    # connectable = async_engine_from_config(
    #     configuration,
    #     prefix="sqlalchemy.",
    #     poolclass=pool.NullPool,
    # )

    connectable = create_async_engine(settings.DATABASE_URL, poolclass=pool.NullPool)

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
