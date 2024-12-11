from fastapi import Depends
from sqlalchemy import func, select
from sqlmodel.ext.asyncio.session import AsyncSession

from ..db import get_db
from ..models.databases import Database

from .base_repository import BaseRepository


class DatabaseRepository(BaseRepository[Database]):
    def __init__(self, session: AsyncSession = Depends(get_db)):
        super().__init__(Database, session)

    async def create(self, data: Database) -> Database:
        return await self.save(Database.model_validate(data))

    async def count_database_created(self) -> int:
        query = select(func.count(Database.id))

        result = await self.db.exec(query)
        return result.scalar()
