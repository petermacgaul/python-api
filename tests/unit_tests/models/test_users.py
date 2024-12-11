import unittest
from unittest.mock import patch

from app.models.users import User


class TestUser(unittest.TestCase):

    def setUp(self):
        self.user = User(username='test_user')
        self.plain_password = 'plain_password'
        self.user.password = self.plain_password

    def test_password_encryption(self):
        self.assertNotEqual(self.user.password, self.plain_password)

    def test_password_match(self):
        self.assertTrue(self.user.password_match(self.plain_password))
