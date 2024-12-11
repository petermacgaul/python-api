import unittest

from app.util.encryptor import Encryptor


class TestEncryptor(unittest.TestCase):

    def test_encrypt_and_decrypt(self):
        original_text = "texto no encriptado"

        encrypted_text = Encryptor.encrypt(original_text)
        decrypted_text = Encryptor.decrypt(encrypted_text)

        # Assertions
        self.assertNotEqual(original_text, encrypted_text,
                            "The encrypted text should not be equal to the original text")
        self.assertEqual(original_text,
                         decrypted_text,
                         "The decrypted text should match the original text")
