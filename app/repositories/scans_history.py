from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from ..db import get_db
from ..models.scans import ScanDatabase
from ..models.scans_history import ScanDatabaseHistory

from .base_repository import BaseRepository


class ScanDatabaseHistoryRepository(BaseRepository[ScanDatabaseHistory]):
    def __init__(self, session: AsyncSession = Depends(get_db)):
        super().__init__(ScanDatabaseHistory, session)

    async def create(self, data: ScanDatabase) -> ScanDatabaseHistory:
        return await self.save(ScanDatabaseHistory.model_validate(data))
