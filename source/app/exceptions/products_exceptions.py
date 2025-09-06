class ProductDuplicateNameException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class ProductCreationException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class ProductsNotFoundException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class ProductNotFoundException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
