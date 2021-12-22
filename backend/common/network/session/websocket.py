import websockets.server
from websockets.exceptions import ConnectionClosedError

from backend.common.network.errors import NetworkErrorCodes, NetworkError
from backend.common.network.session.base import BaseSession


class WebsocketSession(BaseSession):
    _socket: websockets.WebSocketServerProtocol
    connected: bool = False

    @staticmethod
    async def serve(handler: callable, host: str, port: int, on_serve: callable) -> None:
        async with websockets.serve(lambda socket: handler(socket), host, port):
            await on_serve()

    def set_socket(self, socket: websockets.WebSocketServerProtocol):
        self._socket = socket
        self.connected = True

    def set_player_id(self, player_id: int):
        self.player_id = player_id

    async def get_message(self) -> dict:
        try:
            message_string = await self._socket.recv()
        except ConnectionClosedError:
            self.connected = False
            raise NetworkError(NetworkErrorCodes.CLIENT_DISCONNECTED)
        return self._crypter.decode(message_string)

    async def send_message(self, message: object) -> None:
        await self._send_string_message(self._crypter.encode_dataclass(message))

    async def _send_string_message(self, message: str) -> None:
        await self._socket.send(message)
