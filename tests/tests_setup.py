from unittest import IsolatedAsyncioTestCase

from sqlmodel import SQLModel, text
from sqlmodel.ext.asyncio.session import AsyncSession
from httpx import AsyncClient

from app.db import engine
from app.main import app


class BaseDbTestCase(IsolatedAsyncioTestCase):
    db: AsyncSession

    def setUp(self) -> None:
        self.db = AsyncSession(bind=engine)

    async def asyncSetUp(self) -> None:
        async with engine.begin() as conn:
            await conn.execute(text("PRAGMA foreign_keys=ON"))
            await conn.run_sync(SQLModel.metadata.create_all)

    async def asyncTearDown(self) -> None:
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.drop_all)
        await self.db.close()


class BaseAPITestCase(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.client = AsyncClient(app=app, base_url="http://test")
        self.db = AsyncSession(bind=engine)

    async def asyncSetUp(self) -> None:
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

    async def asyncTearDown(self) -> None:
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.drop_all)
        await self.db.close()
        await self.client.aclose()
