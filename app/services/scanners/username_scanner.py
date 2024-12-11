from app.services.scanners.scanner import Scanner

import re


class UsernameScanner(Scanner):
    INFORMATION_TYPE = 'USERNAME'

    def __init__(self) -> None:
        super().__init__()
        self.type = self.INFORMATION_TYPE

    def is_column_from_type(self, column_name: str) -> bool:
        """
        Check if the column name is a username
        """
        pattern = re.compile(r'(?i)(username|user_name|user name)') # posible username names

        if pattern.search(column_name):
            return True

        return False

    def sample_is_compromised(self, sample: str) -> bool:
        """
        Isn't a sensitive information
        """
        return False
