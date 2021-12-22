from typing import Union

from inject import Binder

from backend.common.logic.auth import IAuth
from backend.common.logic.service import IService
from backend.common.network.crypto.base import ICrypter
from backend.common.network.crypto.json import JSONCrypter
from backend.common.network.session.base import ISession
from backend.common.network.session.factory import TransportProviderFactory
from backend.common.network.session.hooks import IConnectionHooks
from backend.common.network.session.websocket import WebsocketSession
from backend.logic.auth import LogicAuth
from backend.logic.hooks import LogicHooks
from backend.logic.service import LogicService, ILogicService


def container(binder: Binder):
    binder.bind(Union[callable, ISession], WebsocketSession)
    binder.bind(TransportProviderFactory, TransportProviderFactory())
    binder.bind(IService, LogicService())
    binder.bind(ILogicService, LogicService())
    binder.bind(ICrypter, JSONCrypter())
    binder.bind(IConnectionHooks, LogicHooks())
    binder.bind(IAuth, LogicAuth())
