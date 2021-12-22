from enum import Enum


class NetworkErrorCodes(Enum):
    CLIENT_DISCONNECTED = 'CLIENT_DISCONNECTED'


class NetworkError(BaseException):
    def __init__(self, code: NetworkErrorCodes, data: any = None):
        self.code = code
        self.data = data
