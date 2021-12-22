import asyncio
from asyncio import sleep, create_task
from typing import Union

from backend.common.logic.auth import IAuth
from backend.ioc import depends
from backend.common.network.enums import MessageTypes
from backend.common.network.errors import NetworkError
from backend.common.network.models import MessageObject
from backend.common.network.session.base import ISession
from backend.common.network.session.factory import TransportProviderFactory
from backend.common.network.session.hooks import IConnectionHooks
from backend.common.network.session.context import context
from backend.logic.events import events_queue


SessionType = Union[callable, ISession]


class Server:
    session_type: SessionType = depends(SessionType) # обозначил так класс, имплементирующий сессию
    session_factory: TransportProviderFactory = depends(TransportProviderFactory)
    _hooks: IConnectionHooks = depends(IConnectionHooks)
    _auth: IAuth = depends(IAuth)

    async def run(self, host: str, port: int):
        
        async def on_run():
            print(f'Websocket server listening on {host}:{port}')
            self._hooks.on_server_start()
            await asyncio.Future()
        
        await self.session_type.serve(self._handle_client_connection, host, port, on_run)
    
    async def _handle_client_connection(self, *args, **kwargs):
        session = self.session_factory.create(self.session_type)
        context.session = session
        session.set_socket(*args, **kwargs)
        self._hooks.on_connect()
        await self._handle_client_session(session)

    async def _handle_client_session(self, session: ISession):
        auth_message = await session.handle_method_call()
        auth_token = auth_message.result['token']
        player_id = self._auth.authenticate(auth_token)
        session.set_player_id(player_id)
        self._hooks.on_authorize()
        create_task(self._wait_for_events(session))
        working = True
        while working:
            working = await self._handle_network_error(session.handle_method_call(), session)
        
    async def _wait_for_events(self, session: ISession):
        while True:
            await sleep(0)
            if session.player_id not in events_queue:
                continue
            
            user_events = events_queue[session.player_id]
            for event_name, payloads in user_events.items():
                for payload in payloads:
                    message = MessageObject(
                        success=True,
                        message_id='',
                        type=MessageTypes.EVENT,
                        result=dict(
                            event_name=event_name,
                            payload=payload,
                        ),
                    )
                    success = await self._handle_network_error(session.send_message(message), session)
                    if not success:
                        return
                    
                user_events[event_name] = []
    
    async def _handle_network_error(self, coroutine, session: ISession) -> bool:
        if not session.connected:
            coroutine.close()
            return False
        try:
            await coroutine
            return True
        except NetworkError as err:
            if session.player_id in events_queue:
                del events_queue[session.player_id]
            self._hooks.on_disconnect()
            return False
        except BaseException as err:
            print('Raised error:', err)
            if session.player_id in events_queue:
                del events_queue[session.player_id]
            self._hooks.on_disconnect()
            raise err
