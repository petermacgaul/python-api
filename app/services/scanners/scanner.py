import logging
from typing import List

from app.util.scan_column_result import Column
from app.util.scan_table_result import Table


class Scanner:

    def __init__(self):
        self.column_patterns = []
        self.sample_patterns = []
        self.type = ""

    def scan_columns(self, columns: List, table: Table) -> None:
        logging.debug(f"Analizing columns with scanner: {self.type}")
        for column in columns:
            result = self.scan_column(column)
            table.add_result(column, result)

            if table.has_result(column):
                logging.debug(f"Result added on column: {column}")
                columns.remove(column)

    def scan_column(self, column_name: str) -> Column:
        column = Column(name=column_name)
        is_from_type = self.is_column_from_type(column_name)

        if is_from_type:
            column.set_type(self.type)

        return column

    def scan_samples(self, samples: dict, table: Table) -> None:
        logging.debug(f"Analizing samples with scanner: {self.type}")
        for column, sample in samples.items():
            unsecured_data = self.sample_is_compromised(str(sample))
            if unsecured_data: table.column_unsecured(column)

    def is_column_from_type(self, column_name: str) -> bool:
        raise NotImplementedError


    def sample_is_compromised(self, sample: str) -> bool:
        raise NotImplementedError
