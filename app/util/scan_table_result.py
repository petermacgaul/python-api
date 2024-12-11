from app.util.scan_column_result import Column


class Table:
    def __init__(self, columns: list) -> None:
        self.column_results = {}

        for column in columns:
            self.column_results[column] = Column(name=column)

    def add_result(self, column: str, result: Column) -> None:
        self.column_results[column] = result

    def json(self) -> dict:
        return {column: result.json() for column, result in self.column_results.items()}

    def has_result(self, column: str) -> bool:
        column_result = self.column_results.get(column, None)
        if not column:
            return False

        return column_result.has_type()

    def column_unsecured(self, column: str) -> None:
        self.column_results[column].compromised_column()
