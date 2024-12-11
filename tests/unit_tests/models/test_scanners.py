import unittest
from unittest.mock import AsyncMock
from app.services.connect_database import ConnectedDatabase
from app.services.database_scanner import DatabaseScanner
from app.util.scan_result import ScanResult


class TestScanner(unittest.IsolatedAsyncioTestCase):

    async def test_scan(self):
        # Given
        mock_database = AsyncMock(spec=ConnectedDatabase)
        mock_database.get_schema.return_value = 'mock_schema'
        mock_database.get_tables.return_value = ['users', 'orders']
        mock_database.get_columns.return_value = ['credit_card_number', 'username']

        scanner = DatabaseScanner(mock_database)

        # When
        result = await scanner.scan()

        # Then
        mock_database.get_schema.assert_awaited_once()
        mock_database.get_tables.assert_awaited_once()
        mock_database.get_columns.assert_awaited()

        self.assertIsInstance(result, ScanResult)
