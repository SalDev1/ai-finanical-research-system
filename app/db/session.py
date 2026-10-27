"""Database session configuration."""
# This piece of code helps in connecting Python to PostgresDB by creating a session with the database.
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings

engine = create_async_engine(
    settings.database_url,
    pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)

#  Assigning a Shared Base for all models.
class Base(AsyncAttrs, DeclarativeBase):
    pass
