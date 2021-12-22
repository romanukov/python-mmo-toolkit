from abc import ABC, abstractmethod


class ICrypter(ABC):
    @abstractmethod
    def encode_dataclass(self, data) -> str: ...

    @abstractmethod
    def decode(self, string: str) -> dict: ...
