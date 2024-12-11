import unittest

from app.services.scanners.ip_address_scanner import IPAddressScanner


class TestIPAddressScanner(unittest.TestCase):

    def setUp(self):
        self.scanner = IPAddressScanner()

    def test_information_type(self):
        self.assertEqual(self.scanner.type, 'IP_ADDRESS')

    def test_is_column_from_type_true(self):
        columns_to_test = [
            'ip_address',
            'ipaddress',
            'ip_address',
            'ipaddress',
            'ip',
            'ip address'
        ]
        for column in columns_to_test:
            with self.subTest(column=column):
                self.assertTrue(self.scanner.is_column_from_type(column))

    def test_is_column_from_type_false(self):
        columns_to_test = [
            'hostname',
            'username',
            'location',
            'postal_code'
        ]
        for column in columns_to_test:
            with self.subTest(column=column):
                self.assertFalse(self.scanner.is_column_from_type(column))

    def test_sample_is_compromised_true(self):
        ip_samples = [
            '192.168.1.1',
            '10.0.0.1',
            '172.16.254.1',
            '8.8.8.8'
        ]
        for ip in ip_samples:
            with self.subTest(ip=ip):
                self.assertTrue(self.scanner.sample_is_compromised(ip))

    def test_sample_is_compromised_false(self):
        non_ip_samples = [
            '999.999.999',
            '256.256',
            '123',
            '192.168.1.',
            'hello world',
            'string.with.dots'
        ]
        for sample in non_ip_samples:
            with self.subTest(sample=sample):
                self.assertFalse(self.scanner.sample_is_compromised(sample))