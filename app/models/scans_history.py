from sqlmodel import Field, SQLModel

from .util import UUIDModel, TimestampModel, Id


class ScanDatabaseHistoryBase(SQLModel):
    pass


class ScanDatabaseHistoryRead(ScanDatabaseHistoryBase, UUIDModel):
    pass


class ScanDatabaseHistory(ScanDatabaseHistoryRead, TimestampModel, table=True):
    __tablename__ = "scans_history"

    database_id: Id = Field(foreign_key="databases.id")
    scan: str
