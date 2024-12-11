# mypy: ignore-errors
from typing import Sequence, Type, TypeVar, Generic, Any
from abc import ABC

from sqlalchemy.sql.functions import count, func
from sqlmodel import select, delete, and_
from sqlmodel.sql.expression import SelectOfScalar
from sqlmodel.ext.asyncio.session import AsyncSession

from ..models.util import UUIDModel, Id

T = TypeVar("T", bound=UUIDModel)
PK = TypeVar("PK")  # Primary key type


class BaseRepository(Generic[T], ABC):
    def __init__(self, repository_class: Type[T], session: AsyncSession):
        self.db = session
        self.cls = repository_class

    def _where(self, **filters) -> list[bool | Any]:
        where_clauses = []
        for field, values in filters.items():
            if not hasattr(self.cls, field):
                raise ValueError(f"Invalid column name {field}")
            column = getattr(self.cls, field)
            if field == "name":
                where_clauses.append(func.lower(column).ilike(f"%{values.lower()}%"))
            elif isinstance(values, list):
                where_clauses.append(column.in_(values))
            else:
                where_clauses.append(column == values)

        return where_clauses

    def _add_filters(self, query, **filters) -> SelectOfScalar:
        where_clauses = self._where(**filters)

        if not where_clauses:
            return query

        initial, *rest = where_clauses
        return query.where(and_(initial, *rest))

    def _list_select(self, **filters) -> SelectOfScalar:
        query = select(self.cls)
        return self._add_filters(query, **filters)

    def _count_query(self, **filters) -> SelectOfScalar:
        query = select(count()).select_from(self.cls)
        return self._add_filters(query, **filters)

    def _count_select(self, **filters: Any) -> SelectOfScalar:
        # pylint: disable=not-callable
        query = select(func.count()).select_from(self.cls)
        return self._add_filters(query=query, **filters)

    async def get_all(self, skip: int = 0, limit: int | None = None, **filters) -> Sequence[T]:
        query = self._list_select(**filters).offset(skip).limit(limit).order_by(self.cls.created_at)
        result = await self.db.exec(query)
        return result.all()

    async def get_by_id(self, _id: Id | str) -> T | None:
        return await self.db.get(self.cls, _id)

    async def save(self, record: T) -> T:
        self.db.add(record)
        await self.db.flush()
        await self.db.refresh(record)
        return record

    async def delete(self, example_id: Id | str) -> None:
        query = delete(self.cls).where(self.cls.id == example_id)
        await self.db.exec(query)

    async def delete_all(self) -> None:
        await self.db.execute(delete(self.cls))

    async def count(self, **filters) -> int:
        query = self._count_query(**filters)
        result = await self.db.exec(query)
        return result.one()

    async def update(self, record_id: PK, new_data: dict[str, Any]) -> T:
        existing = await self.get_by_id(record_id)
        if not existing:
            raise ValueError(f"Record with id {record_id} does not exist")
        for key, value in new_data.items():
            if hasattr(existing, key) and key != "id":
                setattr(existing, key, value)
        return await self.save(existing)
