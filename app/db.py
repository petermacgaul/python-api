from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from .config import settings

engine = create_async_engine(
    settings.DB_URL, connect_args=settings.DB_ARGUMENTS, pool_pre_ping=True
)


SessionLocal = sessionmaker(  # type: ignore
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    db: AsyncSession = SessionLocal()
    try:
        yield db
        await db.commit()
    except Exception:
        await db.rollback()
        raise
    finally:
        await db.close()
