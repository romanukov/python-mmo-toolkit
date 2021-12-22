from enum import Enum


class ErrorCodes(Enum):
    BAD_CREDENTIALS = 'BAD_CREDENTIALS'


class GameError(BaseException):
    def __init__(self, code: ErrorCodes, data = None):
        self.code = code
        self.data = data
