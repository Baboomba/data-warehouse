


class SizeException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
    
    def merge_error(self):
        pass


class MyCustomError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)    