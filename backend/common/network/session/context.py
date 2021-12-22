from backend.common.network.session.base import ISession
from backend.common.network.session.vars import current_session


class ClientConnectionContext:
    
    @property
    def session(self) -> ISession:
        return current_session.get()
    
    @session.setter
    def session(self, v):
        current_session.set(v)


context = ClientConnectionContext()
