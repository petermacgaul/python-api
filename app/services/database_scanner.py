import logging

from app.services.connect_database import ConnectedDatabase
from app.services.scanners.credit_card_scanner import CreditCardScanner
from app.services.scanners.username_scanner import UsernameScanner
from app.services.scanners.email_address_scanner import EmailAddressScanner
from app.services.scanners.ip_address_scanner import IPAddressScanner
from app.util.scan_result import ScanResult
from app.util.scan_table_result import Table


class DatabaseScanner:
    def __init__(self, database: ConnectedDatabase):
        self.scanners = [
            CreditCardScanner(),
            UsernameScanner(),
            EmailAddressScanner(),
            IPAddressScanner()
        ]
        self.database = database

    async def scan(self) -> ScanResult:
        logging.info("Scanning database")
        logging.info("Getting schema")
        schema = await self.database.get_schema()
        logging.debug(f"Schema: {schema}")

        logging.info("Getting tables")
        tables = await self.database.get_tables()
        logging.debug(f"Tables: {tables}")

        scan_result = ScanResult(schema)

        for table in tables:
            table_result = await self._scan_table(table)
            scan_result.add_result(table, table_result)

        return scan_result

    async def _scan_table(self, table_name: str) -> Table:
        logging.debug(f"Scanning table: {table_name}")
        columns = await self.database.get_columns(table_name)
        samples = await self._get_samples(table_name, columns)

        logging.debug(f"Scanning columns: {columns}")
        table = Table(columns)

        for scanner in self.scanners:
            scanner.scan_columns(columns, table)
            scanner.scan_samples(samples, table)

        return table

    async def _get_samples(self, table_name: str, columns: list) -> dict:
        logging.debug(f"Getting samples from: {table_name}")

        samples = {}
        for column in columns:
            logging.debug(f"Getting samples from: {table_name} on column: {column}")
            sample = await self.database.get_sample(table_name, column)
            samples[column] = sample

        return samples
