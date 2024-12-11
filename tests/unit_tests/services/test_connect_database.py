import unittest
from typing import ClassVar
from unittest.mock import AsyncMock, patch
from app.exceptions.databases import DatabaseNotConnected
from app.models.databases import DatabaseBase
from app.services.connect_database import ConnectedDatabase


class MockDatabase(DatabaseBase):
    def url(self) -> str:
        return "sqlite+aiosqlite:///:memory:"

    db_name: ClassVar[str] = "test_db"


class TestConnectedDatabase(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.database = MockDatabase()
        self.connected_database = ConnectedDatabase(self.database)

    @patch.object(ConnectedDatabase, '_execute_query', new_callable=AsyncMock)
    async def test_verify_connection(self, mock_execute_query):
        mock_execute_query.return_value = None

        await self.connected_database.verify_connection()
        assert True

    @patch.object(ConnectedDatabase, '_execute_query', new_callable=AsyncMock)
    async def test_verify_connection_failure(self, mock_execute_query):
        mock_execute_query.side_effect = Exception("Database connection error")

        with self.assertRaises(DatabaseNotConnected):
            await self.connected_database.verify_connection()