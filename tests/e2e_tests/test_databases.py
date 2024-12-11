from unittest.mock import patch, AsyncMock
import json

from app.exceptions.databases import DatabaseNotConnected
from app.models.databases import Database
from app.models.users import User
from tests.tests_setup import BaseAPITestCase
from jose import JWTError


class TestDatabaseRoute(BaseAPITestCase):

    @patch("app.services.jwt_service.get_user", new_callable=AsyncMock)
    @patch("app.services.connect_database.ConnectedDatabase.verify_connection", new_callable=AsyncMock)
    async def test_create_database_with_all_fields(self, mocked_verify_connection, mocked_get_current_user) -> None:
        database_create_json_data = {
            "username": "test_user",
            "password": "test_password",
            "host": "127.0.0.1",
            "port": 5432
        }

        mocked_verify_connection.return_value = None
        mocked_get_current_user.return_value = User(id=1, username="mock_user")

        headers = {
            "Authorization": "Bearer valid_token"
        }

        response = await self.client.post("/database/", json=database_create_json_data, headers=headers)

        assert response.status_code == 201
        response_text = json.loads(response.text)
        database: Database | None = await self.db.get(Database, response_text["id"])

        assert database is not None

        assert database.password_digest is not None
        assert database.password_digest != database_create_json_data["password"]
        assert database.password == database_create_json_data["password"]

        assert database.host_digest is not None
        assert database.host_digest != database_create_json_data["host"]
        assert database.host == database_create_json_data["host"]

        assert database.port_digest is not None
        assert database.port_digest != database_create_json_data["port"]
        assert database.port == database_create_json_data["port"]

        assert database.username_digest is not None
        assert database.username_digest != database_create_json_data["username"]
        assert database.username == database_create_json_data["username"]

    @patch("app.services.jwt_service.get_user", new_callable=AsyncMock)
    @patch("app.services.connect_database.ConnectedDatabase.verify_connection", new_callable=AsyncMock)
    async def test_create_database_with_failed_connection(self, mocked_verify_connection, mocked_get_current_user) -> None:
        database_create_json_data = {
            "username": "test_user",
            "password": "test_password",
            "host": "127.0.0.1",
            "port": 5432
        }
        mocked_verify_connection.side_effect = DatabaseNotConnected()
        mocked_get_current_user.return_value = User(id=1, username="mock_user")
        headers = {
            "Authorization": "Bearer valid_token"
        }
        response = await self.client.post("/database/", json=database_create_json_data, headers=headers)
        assert response.status_code == 400
        response_text = json.loads(response.text)
        assert response_text['error_message'] == "Error connecting to database"

    @patch("app.services.jwt_service.get_user", new_callable=AsyncMock)
    async def test_create_database_with_invalid_token(self, mocked_get_current_user) -> None:
        database_create_json_data = {
            "username": "test_user",
            "password": "test_password",
            "host": "127.0.0.1",
            "port": 5432
        }
        mocked_get_current_user.side_effect = JWTError()
        headers = {
            "Authorization": "Bearer invalid_token"
        }
        response = await self.client.post("/database/", json=database_create_json_data, headers=headers)
        assert response.status_code == 401
        response_text = json.loads(response.text)
        assert response_text['error_message'] == "Could not validate credentials"

    async def test_create_database_without_token(self) -> None:
        database_create_json_data = {
            "username": "test_user",
            "password": "test_password",
            "host": "127.0.0.1",
            "port": 5432
        }

        response = await self.client.post("/database/", json=database_create_json_data)
        assert response.status_code == 401
        response_text = json.loads(response.text)
        assert response_text['error_message'] == "Could not validate credentials"