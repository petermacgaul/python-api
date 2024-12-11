import unittest

from app.services.scanners.credit_card_scanner import CreditCardScanner


class TestCreditCardScanner(unittest.TestCase):

    def setUp(self):
        self.scanner = CreditCardScanner()

    def test_information_type(self):
        self.assertEqual(self.scanner.type, 'CREDIT_CARD_NUMBER')

    def test_is_column_from_type_true(self):
        columns_to_test = [
            'credit_card_number',
            'credit_card',
            'ccn',
            'card_number',
            'creditcardnumber'
        ]
        for column in columns_to_test:
            with self.subTest(column=column):
                self.assertTrue(self.scanner.is_column_from_type(column))

    def test_is_column_from_type_false(self):
        columns_to_test = [
            'account_number',
            'phone_number',
            'email_address',
            'user_id'
        ]
        for column in columns_to_test:
            with self.subTest(column=column):
                self.assertFalse(self.scanner.is_column_from_type(column))

    def test_sample_is_compromised_true(self):
        compromised_samples = [
            '1234 5678 9012 3456',
            '1234-5678-9012-3456',
            '1234567890123456',
            '1234 5678 9012345'
        ]
        for sample in compromised_samples:
            with self.subTest(sample=sample):
                self.assertTrue(self.scanner.sample_is_compromised(sample))

    def test_sample_is_compromised_false(self):
        non_compromised_samples = [
            '1234',
            'not a credit card number',
            '1234-5678',
            'abcd efgh ijkl mnop'
        ]
        for sample in non_compromised_samples:
            with self.subTest(sample=sample):
                self.assertFalse(self.scanner.sample_is_compromised(sample))