from app.services.scanners.scanner import Scanner

import re


class IPAddressScanner(Scanner):
    INFORMATION_TYPE = 'IP_ADDRESS'

    def __init__(self) -> None:
        super().__init__()
        self.type = self.INFORMATION_TYPE

    def is_column_from_type(self, column_name: str) -> bool:
        """
        Check if the column name is related to IP Address
        """
        pattern = re.compile(r'(?i)(ip_address|ipaddress|ip_address|ipaddress|ip|ip address)')

        if pattern.search(column_name):
            return True

        return False

    def sample_is_compromised(self, sample: str) -> bool:
        """
        Check if the sample is a valid IP address
        """
        pattern = re.compile(r'(?i)(\b(?:\d{1,3}\.){3}\d{1,3}\b)')

        if pattern.search(sample):
            return True

        return False
