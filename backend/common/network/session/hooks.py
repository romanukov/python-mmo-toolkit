from abc import abstractmethod, ABC


class IConnectionHooks(ABC):
    
    @abstractmethod
    def on_server_start(self): ...
    
    @abstractmethod
    def on_server_exit(self): ...
    
    @abstractmethod
    def on_connect(self): ...
    
    @abstractmethod
    def on_authorize(self): ...
    
    @abstractmethod
    def on_method_call(self): ...
    
    @abstractmethod
    def on_disconnect(self): ...
