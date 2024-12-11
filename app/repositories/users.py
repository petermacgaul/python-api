from fastapi import Depends
from sqlalchemy import select
from sqlmodel.ext.asyncio.session import AsyncSession

from ..db import get_db
from ..models.users import User, UserCreate

from .base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession = Depends(get_db)):
        super().__init__(User, session)

    async def create(self, data: UserCreate) -> User:
        new_user = User(
            username=data.username
        )
        new_user.password = data.password
        return await self.save(new_user)

    async def get_by_username(self, username) -> User | None:
        query = select(User).where(self.cls.username == username).limit(1)
        result = await self.db.exec(query)
        user = result.first()
        return user[0] if user else None