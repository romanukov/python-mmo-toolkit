from abc import ABC, abstractmethod


class IAuth(ABC):

    @abstractmethod
    def authenticate(self, token): ...

    @abstractmethod
    def authorize(self, player_name, password): ...
