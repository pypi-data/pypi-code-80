import abc
import typing
from . import mention, package

class tools(abc.ABCMeta):
    def __init__(self, *args, **kwargs):
        raise RuntimeError("Incorrect usage")

    @property
    @abc.abstractmethod
    def assets(self):
        pass

    @property
    @abc.abstractmethod
    def values(self):
        pass

    @property
    @abc.abstractmethod
    def api(self):
        pass

    @property
    @abc.abstractmethod
    def http(self):
        pass

    @abc.abstractmethod
    def gen_random(self) -> int:
        pass

    @abc.abstractmethod
    def system_message(self, *args, write: typing.Optional[str] = None, module: str = "system", level:str = 'info') -> None:
        pass

    @abc.abstractmethod
    def getBotId(self) -> int:
        pass

    @abc.abstractmethod
    def getBotLink(self) -> str:
        pass

    @abc.abstractmethod
    def getBotDogMention(self) -> mention:
        """
        Get Mention as testcanarybot.objects.mention
        To get mention at format [id|string] use repr(tools.getBotDogMention())
        """
        pass

    @abc.abstractmethod
    def getBotMentions(self) -> list:
        """
        get all mentions that you set as bot mentions at commands
        """
        pass


    @abc.abstractmethod
    def wait_check(self, package) -> bool:
        pass


    @abc.abstractmethod
    async def wait_reply(self, package: package) -> package:
        pass

    @abc.abstractmethod
    async def getMention(self, page_id: int, name_case = "nom") -> str:
        pass


    @abc.abstractmethod
    async def getManagers(self, group_id = None) -> list:
        pass


    @abc.abstractmethod
    async def isManager(self, from_id: int, group_id = None) -> bool:
        pass


    @abc.abstractmethod
    async def getChatManagers(self, peer_id: int) -> list:
        pass
        

    @abc.abstractmethod
    def isChatManager(self, from_id, peer_id: int) -> bool:
        pass


    @abc.abstractmethod
    async def getMembers(self, peer_id: int) -> list:
        pass


    @abc.abstractmethod
    async def isMember(self, from_id: int, peer_id: int) -> bool:
        pass