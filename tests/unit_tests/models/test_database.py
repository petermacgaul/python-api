import unittest

from app.models.databases import Database
from app.util.encryptor import Encryptor

class TestDatabase(unittest.TestCase):

    def test_database_properties_encryption_and_decryption(self):
        # Given
        original_data = {
            'host': 'localhost',
            'port': 5432,
            'username': 'user1',
            'password': 'securepassword'
        }

        database = Database()

        database.host = original_data['host']
        database.port = original_data['port']
        database.username = original_data['username']
        database.password = original_data['password']

        # When
        for attr in original_data.keys():
            encrypted_value = getattr(database, f"{attr}_digest")

            self.assertNotEqual(encrypted_value, original_data[attr])
            decrypted_value = Encryptor.decrypt(encrypted_value)
            self.assertEqual(decrypted_value, str(original_data[attr]))

        # Then
        self.assertEqual(database.host, original_data['host'])
        self.assertEqual(database.port, original_data['port'])
        self.assertEqual(database.username, original_data['username'])
        self.assertEqual(database.password, original_data['password'])
