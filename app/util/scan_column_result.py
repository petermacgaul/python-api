from typing import Any

from app.const import NO_TYPE


class Column:
    def __init__(self, name: str) -> None:
        self.name = name
        self.type = NO_TYPE
        self.compromised = False

    def set_type(self, result: str) -> None:
        if result == NO_TYPE:
            return

        self.type = result

    def has_type(self) -> bool:
        return self.type != NO_TYPE

    def __eq__(self, other: Any) -> bool:
        return self.name == other.name and self.type == other.type

    def json(self) -> dict:
        return {
            "name": self.name,
            "type": self.type,
            "compromised": self.compromised
        }

    def compromised_column(self) -> None:
        self.compromised = True
