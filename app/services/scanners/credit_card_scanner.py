from app.services.scanners.scanner import Scanner

import re


class CreditCardScanner(Scanner):
    INFORMATION_TYPE = 'CREDIT_CARD_NUMBER'

    def __init__(self) -> None:
        super().__init__()
        self.type = self.INFORMATION_TYPE

    def is_column_from_type(self, column_name: str) -> bool:
        """
        Check if the column name is a credit card number
        """
        pattern = re.compile(
            r'(?i)(credit_card_number|credit_card|ccn|card_number|creditcardnumber)' # posible credit card number names
        )

        if pattern.search(column_name):
            return True

        return False

    def sample_is_compromised(self, sample: str) -> bool:
        """
        Check if the sample is a credit card number
        """
        pattern = re.compile(r'\b(?:\d[ -]*?){13,16}\b') # 13 to 16 digits

        if pattern.search(sample):
            return True

        return False
