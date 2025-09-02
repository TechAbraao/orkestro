class MenuFoundException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class MenuNotFoundException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
        
