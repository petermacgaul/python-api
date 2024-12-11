from typing import NoReturn
from fastapi import APIRouter, Depends, HTTPException
from fastapi import status as http_status

from ..models.users import UserCreate, UserRead
from ..repositories.users import UserRepository

router = APIRouter(prefix="/users", tags=["Users"])


def _not_found(user_id: str) -> NoReturn:
    raise HTTPException(
        status_code=http_status.HTTP_404_NOT_FOUND,
        detail=f"User with id {user_id} not found",
    )


@router.post("", status_code=http_status.HTTP_201_CREATED)
async def create_user(
    data: UserCreate, repo: UserRepository = Depends(UserRepository)
) -> UserRead:
    user = await repo.create(data)
    return user
