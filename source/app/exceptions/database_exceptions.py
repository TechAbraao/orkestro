class DatabaseUnavailableException(Exception):
    def __init__(self, details="Database is unavailable."):
        self.details = details
        super().__init__(self.details)