import jwt
from fastapi import Depends, Request

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from fastapi import HTTPException
from fastapi import status as http_status
from jose import JWTError

from app.config import settings
from app.models.users import User
from app.repositories.users import UserRepository

UNAUTHORIZED = HTTPException(
    status_code=http_status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials"
)

oauth2_scheme = HTTPBearer(auto_error=False)


async def get_user(token: str, user_repo: UserRepository) -> User | None:
    user_id = JWTService.get_id_from_token(token)
    if user_id is None:
        raise UNAUTHORIZED

    user = await user_repo.get_by_id(user_id)
    if user is None:
        raise UNAUTHORIZED

    return user

async def validate_user(
        req: Request,
        auth: HTTPAuthorizationCredentials | None = Depends(oauth2_scheme),
        user_repo: UserRepository = Depends(UserRepository),
) -> User | None:

    if auth is None:
        raise UNAUTHORIZED

    try:
        user = await get_user(auth.credentials, user_repo)
        setattr(req.state, "user", user)
        return user
    except JWTError as exc:
        raise UNAUTHORIZED from exc


class JWTService:
    @staticmethod
    def encode(data: dict, algorithm: str = "HS256") -> str:
        return jwt.encode(data, settings.JWT_KEY, algorithm=algorithm)

    @staticmethod
    def decode(token: str, algorithm: str = "HS256") -> dict:
        return jwt.decode(token, settings.JWT_KEY, algorithms=[algorithm])

    @staticmethod
    def get_id_from_token(token: str) -> str:
        payload = JWTService.decode(token)
        return payload.get("user_id")
