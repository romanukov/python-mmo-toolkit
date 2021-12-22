from abc import ABC

from backend.common.logic.service import IService
from backend.common.logic.session import ISession
from backend.ioc import depends
from backend.common.network.crypto.base import ICrypter
from backend.common.network.enums import MessageTypes
from backend.common.network.models import MessageObject, MethodCall, ErrorResult
from backend.common.network.rpc.local import methods
from backend.common.network.session.hooks import IConnectionHooks
from backend.logic.errors import GameError



class BaseSession(ISession, ABC):
    _service: IService = depends(IService)
    _crypter: ICrypter = depends(ICrypter)
    _hooks: IConnectionHooks = depends(IConnectionHooks)

    async def handle_method_call(self) -> MessageObject:
        message = await self.get_message()
        message = MethodCall(**message)

        self._hooks.on_method_call()

        rpc_method = methods[message.method_name]
        argument = rpc_method.argument_model(**message.data) if rpc_method.argument_model else None
        
        args = []
        if argument:
            args = [argument]
    
        try:
            response = rpc_method.func(self._service, *args)
            response_message = MessageObject(
                type=MessageTypes.METHOD_RESPONSE,
                success=True,
                message_id=message.message_id,
                result=response,
            )
            await self.send_message(response_message)
            return response_message
        except GameError as error:
            error_message = MessageObject(
                type=MessageTypes.METHOD_RESPONSE,
                success=False,
                message_id=message.message_id,
                result=ErrorResult(
                    code=error.code,
                    data=error.data
                ),
            )
            await self.send_message(error_message)
            return error_message
