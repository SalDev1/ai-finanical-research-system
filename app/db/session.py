from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    create_async_engine,
    async_sessionmaker,
    AsyncSession
) 
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings

# Creates an asynchronous database engine.
engine = create_async_engine(
    settings.database_url,
    echo=True,  # print SQL queries in your terminal, which is useful for debugging.
    pool_pre_ping=True   # Helps detect stale database connections.
)

# Creates an asynchronous database sessions.
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)
class Base(AsyncAttrs, DeclarativeBase):
    pass

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session