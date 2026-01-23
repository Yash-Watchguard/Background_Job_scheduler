class AppException(Exception):
    def __init__(self, status_code:int, message:str, error_code:int):
        self.status_code = status_code
        self.message = message
        self.error_code = error_code