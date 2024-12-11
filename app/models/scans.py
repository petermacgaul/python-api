import json
from typing import Dict, Any

from sqlmodel import Field, SQLModel

from .util import UUIDModel, TimestampModel, Id


class ScanDatabaseBase(SQLModel):
    pass


class ScanDatabaseRead(ScanDatabaseBase, UUIDModel):
    pass


class ScanDatabase(ScanDatabaseRead, TimestampModel, table=True):
    __tablename__ = "scans"

    database_id: Id = Field(foreign_key="databases.id")
    scan: str


class ScanDatabaseCreate(ScanDatabaseBase):
    database_id: Id
    scan: Dict[str, Any]

    @property
    def scan(self) -> str:
        return json.dumps(self.scan)


class ScanDatabaseSerializer(ScanDatabaseBase):
    scan: Dict[str, Any]
