from abc import ABC

from backend.common.network.session.base import ISession


class TransportProviderFactory(ABC):
    def create(self, t: type) -> ISession:
        return t()
