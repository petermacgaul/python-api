from fastapi import Depends
from sqlalchemy import select
from sqlmodel.ext.asyncio.session import AsyncSession

from ..db import get_db
from ..models.scans import ScanDatabase

from .base_repository import BaseRepository


class ScanDatabaseRepository(BaseRepository[ScanDatabase]):
    def __init__(self, session: AsyncSession = Depends(get_db)):
        super().__init__(ScanDatabase, session)

    async def create(self, new_database: ScanDatabase) -> ScanDatabase:
        return await self.save(new_database)

    async def get_by_database_id(self, database_id: str) -> ScanDatabase:
        query = (select(ScanDatabase.id, ScanDatabase.scan)
                 .where(self.cls.database_id == database_id).limit(1))
        result = await self.db.exec(query)
        return result.first()
