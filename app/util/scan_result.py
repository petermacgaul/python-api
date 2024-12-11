from app.util.scan_table_result import Table


class ScanResult:
    def __init__(self, schema: list):
        self.table_results = {}
        self.schema = [list(item) for item in schema]

    def add_result(self, table: str, result: Table) -> None:
        self.table_results[table] = result

    def json(self) -> dict:
        return {
            "schema": self.schema,
            "tables": {table: result.json() for table, result in self.table_results.items()},
        }
