# @Time     : 2021/3/26
# @Project  : w8_auto_utils
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
import abc
import typing
from collections.abc import Awaitable

from w8_auto_py.typings import Interface, NumberTypes
from w8_auto_py.global_vars import TimeUnit

T = typing.TypeVar("T")
EmitterReturnType = typing.TypeVar("EmitterReturnType")


class AbstractEmitterTask(metaclass=abc.ABCMeta):
    """
    抽象并发器任务
    """

    @abc.abstractmethod
    def add_task(self, task: T, **kwargs) -> None:
        """
        添加
        :param task:
        :param kwargs:
        :return:
        """
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def length(self) -> int:
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def empty(self) -> bool:
        raise NotImplementedError()

    @abc.abstractmethod
    def __iter__(self) -> typing.Iterable[T]:
        raise NotImplementedError()


class AbstractEmitter(Awaitable, metaclass=abc.ABCMeta):

    def __init__(self,
                 task: AbstractEmitterTask,
                 delay: NumberTypes,
                 date_unit: TimeUnit):
        self.__task = task
        self.__delay = delay
        self.__date_unit = date_unit

    @property
    def task(self) -> AbstractEmitterTask:
        return self.__task

    @property
    def delay(self) -> NumberTypes:
        if not isinstance(self.__delay, int):
            self.__delay = 1

        if not isinstance(self.__date_unit, TimeUnit):
            self.__date_unit = TimeUnit.MS

        return self.__delay * self.__date_unit.value

    @abc.abstractmethod
    async def run(self, *args, **kwargs) -> T:
        raise NotImplementedError()

    async def start(self) -> T:
        return await self.run()

    def __await__(self):
        return self.start().__await__()


class IEmitterTask(Interface):
    """
    并发任务接口
    """

    def add(self, task: T, **kwargs) -> None:
        raise NotImplementedError()

    def __iter__(self) -> typing.Iterable[T]:
        raise NotImplementedError()


class IEmitter(Interface):
    """
    并发器接口
    """

    async def start(self) -> EmitterReturnType:
        raise NotImplementedError()
