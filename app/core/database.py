from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine , AsyncEngine
from app.core.configs import settings
from typing import Generator

engine: AsyncEngine = create_async_engine(settings.DB_URL)

Session: AsyncSession = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
    bind=engine
)
async def get_session()-> Generator:
    session: AsyncSession = Session()
    try:
        yield session
    finally:
        await session.close()
