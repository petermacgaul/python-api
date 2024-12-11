import json

from tests.tests_setup import BaseAPITestCase


class TestUsersRoute(BaseAPITestCase):

    async def test_login_success(self) -> None:
        user_create_json_data = {
            "username": "test_user",
            "password": "test_password",
        }
        response = await self.client.post("/users", json=user_create_json_data)
        assert response.status_code == 201

        response = await self.client.post("/login", json=user_create_json_data)
        assert response.status_code == 200

        response_text = json.loads(response.text)
        assert response_text["access_token"] is not None

    async def test_user_registration_missing_fields(self) -> None:
        incomplete_user_data = {
            "username": "test_user"
        }
        response = await self.client.post("/users", json=incomplete_user_data)
        assert response.status_code == 400

    async def test_login_incorrect_credentials(self) -> None:
        incorrect_user_data = {
            "username": "test_user_non_existent",
            "password": "test_password",
        }
        response = await self.client.post("/login", json=incorrect_user_data)
        assert response.status_code == 404


    async def test_login_incorrect_password(self) -> None:
        user_create_json_data = {
            "username": "test_user",
            "password": "test_password",
        }
        response = await self.client.post("/users", json=user_create_json_data)
        assert response.status_code == 201
        incorrect_user_data = {
            "username": "test_user",
            "password": "wrong_password",
        }
        response = await self.client.post("/login", json=incorrect_user_data)
        assert response.status_code == 401

