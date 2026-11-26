from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from app.core.configs import settings

db_url = settings.DB_URL
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql+asyncpg://", 1)
elif db_url.startswith("postgresql://") and "+asyncpg" not in db_url:
    db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)

connect_args = {"check_same_thread": False} if db_url.startswith("sqlite") else {}

engine: AsyncEngine = create_async_engine(db_url, connect_args=connect_args)

SessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
    bind=engine,
)


async def get_session():
    session: AsyncSession = SessionLocal()
    try:
        yield session
    finally:
        await session.close()