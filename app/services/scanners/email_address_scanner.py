from app.services.scanners.scanner import Scanner

import re


class EmailAddressScanner(Scanner):
    INFORMATION_TYPE = 'EMAIL_ADDRESS'

    def __init__(self):
        super().__init__()
        self.type = self.INFORMATION_TYPE

    def is_column_from_type(self, column_name: str) -> bool:
        """
        Check if the column name is related to Email Address
        """
        pattern = re.compile(
            r'(?i)(email|email_address|e-mail|e_mail|e mail|e mail address|e-mail address|emailaddress|emailaddress)') # posible email address names

        if pattern.search(column_name):
            return True

        return False

    def sample_is_compromised(self, sample: str) -> bool:
        """
        Isn't a sensitive information
        """
        return False
