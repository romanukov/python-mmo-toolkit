from abc import ABC, abstractmethod

from backend.common.network.models import MessageObject


class ISession(ABC):
    player_id: int = None
    connected: bool = False
    
    @staticmethod
    def serve(handler: callable, host: str, port: int, on_serve: callable): ...
    
    @abstractmethod
    def set_socket(self, socket: any): ...
    
    @abstractmethod
    def set_player_id(self, player_id: int): ...
    
    @abstractmethod
    async def get_message(self) -> dict: ...
    
    @abstractmethod
    async def send_message(self, message: dict | list) -> None: ...
    
    @abstractmethod
    async def handle_method_call(self) -> MessageObject: ...
