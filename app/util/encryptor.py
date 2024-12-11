from cryptography.fernet import Fernet

from app.config import settings

cipher_suite = Fernet(settings.ENCRYPT_KEY)


class Encryptor:
    @staticmethod
    def encrypt(value: str) -> str:
        return cipher_suite.encrypt(value.encode()).decode()

    @staticmethod
    def decrypt(value: str) -> str:
        return cipher_suite.decrypt(value.encode()).decode()
