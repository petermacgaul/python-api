import unittest

from app.services.scanners.username_scanner import UsernameScanner


class TestUsernameScanner(unittest.TestCase):

    def setUp(self):
        self.scanner = UsernameScanner()

    def test_information_type(self):
        self.assertEqual(self.scanner.type, 'USERNAME')

    def test_is_column_from_type_true(self):
        columns_to_test = [
            'username',
            'user_name',
            'user name'
        ]
        for column in columns_to_test:
            with self.subTest(column=column):
                self.assertTrue(self.scanner.is_column_from_type(column))

    def test_is_column_from_type_false(self):
        columns_to_test = [
            'first_name',
            'surname',
            'email_address',
            'contact_number'
        ]
        for column in columns_to_test:
            with self.subTest(column=column):
                self.assertFalse(self.scanner.is_column_from_type(column))

    def test_sample_is_compromised_always_false(self):
        samples_to_test = [
            'admin',
            'johndoe',
            'user123',
            'guest_user',
            'another_sample'
        ]
        for sample in samples_to_test:
            with self.subTest(sample=sample):
                self.assertFalse(self.scanner.sample_is_compromised(sample))