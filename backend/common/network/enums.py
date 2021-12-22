from enum import Enum


class TransportProtocols(Enum):
    WEBSOCKET = 'WEBSOCKET'
    TCP = 'TCP'
    UDP = 'UDP'
    HTTP = 'HTTP'


class MessageTypes(Enum):
    METHOD_CALL = 'METHOD_CALL'
    METHOD_RESPONSE = 'METHOD_RESPONSE'
    EVENT = 'EVENT'
