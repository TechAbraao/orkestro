class CategoryDuplicateNameException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class CategoryCreationException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class CategoryNotFoundException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
