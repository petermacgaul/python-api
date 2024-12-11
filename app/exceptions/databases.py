class DatabaseNotConnected(Exception):
    def __init__(self) -> None:
        self.message = "Error connecting to database"
        super().__init__(self.message)
