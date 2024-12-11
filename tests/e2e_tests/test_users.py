import json

from app.models.users import User
from tests.tests_setup import BaseAPITestCase


class TestUsersRoute(BaseAPITestCase):

    async def test_create_users_with_all_fields(self) -> None:
        user_create_json_data = {
            "username": "test_user",
            "password": "test_password",
        }

        response = await self.client.post("/users", json=user_create_json_data)

        assert response.status_code == 201
        response_text = json.loads(response.text)
        user: User | None = await self.db.get(User, response_text["id"])

        assert user is not None
        assert user.password is not None
        assert user.password != user_create_json_data["password"]
        assert response_text["id"] is not None
        del response_text["id"]
        del user_create_json_data["password"]
        assert response_text == user_create_json_data

        assert user.created_at is not None
        assert user.updated_at is not None