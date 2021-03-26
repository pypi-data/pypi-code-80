from abc import abstractmethod, ABC

from bottle import Bottle


class BaseApp(ABC):
    """every new app must inherit from  BaseApp"""

    @staticmethod
    @abstractmethod
    def call_router(core):
        pass


class PluginApp(ABC):
    @staticmethod
    @abstractmethod
    def install(core: Bottle):
        pass
