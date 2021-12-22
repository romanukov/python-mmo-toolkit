from dataclasses import dataclass

from backend.common.network.enums import MessageTypes
from backend.logic.errors import ErrorCodes


@dataclass
class MethodCall:
    message_id: str
    method_name: str
    data: any


@dataclass
class MessageObject:
    success: bool
    message_id: str
    type: MessageTypes
    result: any


@dataclass
class ErrorResult:
    code: ErrorCodes
    data: any
