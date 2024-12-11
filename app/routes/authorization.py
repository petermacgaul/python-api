from typing import NoReturn

from fastapi import APIRouter, Depends, HTTPException
from fastapi import status as http_status

from ..repositories.users import UserRepository
from ..services.jwt_service import JWTService
from ..util.jwt_serializer import UserLogin, JWTtoken

router = APIRouter(prefix="/login", tags=["Authorization"])


def _not_found(user_id: str) -> NoReturn:
    raise HTTPException(
        status_code=http_status.HTTP_404_NOT_FOUND,
        detail=f"User with id {user_id} not found",
    )


@router.post("", status_code=http_status.HTTP_200_OK)
async def login(
    data: UserLogin,
    jwt_service: JWTService = Depends(JWTService),
    repo: UserRepository = Depends(UserRepository)
) -> JWTtoken:
    user = await repo.get_by_username(data.username)

    if not user:
        _not_found(data.username)

    if not user.password_match(data.password):
        raise HTTPException(
            status_code=http_status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
        )

    token = jwt_service.encode({"user_id": str(user.id), "username": user.username})
    return JWTtoken(access_token=token)
