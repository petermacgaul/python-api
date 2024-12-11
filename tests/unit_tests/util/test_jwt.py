import unittest
from unittest.mock import patch, AsyncMock
from fastapi import Request, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from jose import JWTError

from app.config import settings
from app.models.users import User
from app.repositories.users import UserRepository
from app.services.jwt_service import validate_user, UNAUTHORIZED, JWTService


class TestJWTService(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.request = AsyncMock(Request)
        self.user_repo = AsyncMock(UserRepository)
        self.valid_token = "valid.token.here"
        self.user_id = "12345"
        self.mock_user = User(id=self.user_id, username="testuser")

    @patch("app.services.jwt_service.JWTService.get_id_from_token", return_value="12345")
    async def test_get_current_user_valid_token(self, mock_get_id):
        self.user_repo.get_by_id.return_value = self.mock_user

        user = await validate_user(
            self.request,
            HTTPAuthorizationCredentials(scheme="Bearer", credentials=self.valid_token),
            self.user_repo,
        )

        self.assertEqual(user, self.mock_user)
        self.user_repo.get_by_id.assert_awaited_once_with("12345")
        self.assertEqual(self.request.state.user, self.mock_user)

    @patch("app.services.jwt_service.JWTService.get_id_from_token", side_effect=JWTError("Invalid token"))
    async def test_get_current_user_invalid_token(self, mock_get_id):
        with self.assertRaises(HTTPException) as exc:
            await validate_user(
                self.request,
                HTTPAuthorizationCredentials(scheme="Bearer", credentials="invalid.token"),
                self.user_repo,
            )
        self.assertEqual(exc.exception.status_code, UNAUTHORIZED.status_code)

    async def test_get_current_user_missing_credentials(self):
        with self.assertRaises(HTTPException) as exc:
            await validate_user(self.request, None, self.user_repo)

        self.assertEqual(exc.exception.status_code, UNAUTHORIZED.status_code)


    @patch("jwt.decode", return_value={"user_id": "12345"})
    def test_get_id_from_token_valid(self, mock_decode):
        token = "valid.token.here"
        user_id = JWTService.get_id_from_token(token)
        self.assertEqual(user_id, "12345")
        mock_decode.assert_called_once_with(token, settings.JWT_KEY, algorithms=["HS256"])

    @patch("jwt.decode", side_effect=JWTError("Invalid token"))
    def test_get_id_from_token_invalid(self, mock_decode):
        token = "invalid.token.here"
        with self.assertRaises(JWTError):
            JWTService.get_id_from_token(token)