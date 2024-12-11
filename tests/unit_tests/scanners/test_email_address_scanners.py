import unittest

from app.services.scanners.email_address_scanner import EmailAddressScanner


class TestEmailAddressScanner(unittest.TestCase):

    def setUp(self):
        self.scanner = EmailAddressScanner()

    def test_information_type(self):
        self.assertEqual(self.scanner.type, 'EMAIL_ADDRESS')

    def test_is_column_from_type_true(self):
        columns_to_test = [
            'email',
            'email_address',
            'e-mail',
            'e_mail',
            'e mail',
            'e mail address',
            'e-mail address',
            'emailaddress'
        ]
        for column in columns_to_test:
            with self.subTest(column=column):
                self.assertTrue(self.scanner.is_column_from_type(column))

    def test_is_column_from_type_false(self):
        columns_to_test = [
            'username',
            'user_id',
            'contact_number',
            'address'
        ]
        for column in columns_to_test:
            with self.subTest(column=column):
                self.assertFalse(self.scanner.is_column_from_type(column))

    def test_sample_is_compromised_always_false(self):
        samples_to_test = [
            'this should not be compromised',
            'even actual@example.com should return false',
            '12345',
            'random-string'
        ]
        for sample in samples_to_test:
            with self.subTest(sample=sample):
                self.assertFalse(self.scanner.sample_is_compromised(sample))