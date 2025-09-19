class StoresDuplicateException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class StoresNotFoundException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)