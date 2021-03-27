# @Time     : 2021/3/26
# @Project  : w8_auto_utils
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
import abc
import asyncio
import typing

from w8_auto_py.typings import ArgsType, Function, NumberTypes, KwargsType
from w8_auto_py.global_vars import TimeUnit
from w8_auto_py.common.emitter import AbstractEmitter, IEmitterTask
from w8_auto_py.common.validator import is_coroutine_function


class Emitter(AbstractEmitter):
    """
    并发器
    """

    def __init__(self,
                 coro_func: Function,
                 task: IEmitterTask,
                 max_num: typing.Union[int, None] = None,
                 delay: NumberTypes = 500,
                 date_unit: TimeUnit = TimeUnit.MS,
                 args: ArgsType = None,
                 kwargs: KwargsType = None):
        """

        Args:
            coro_func:          协程函数 或 任意可调用对象返回协程函数
            max_num:            最大并发数，when None, is 2 ** 31
            delay:              延迟创建时间，默认 500 毫秒
            date_unit:          延迟创建时间单位
            args:               位置参数
            kwargs:             关键字参数
        """
        super().__init__(task, delay, date_unit)
        if not is_coroutine_function(coro_func):
            raise ValueError("coro_func must be coro function, callable return coro function")

        self.__coro_or_func = coro_func
        self.__max_num = max_num
        self.__args = () if not isinstance(args, tuple) else args
        self.__kwargs = {} if not isinstance(kwargs, dict) else kwargs

    @property
    def coro_func(self) -> Function:
        return self.__coro_or_func

    @property
    def max_num(self) -> int:
        if not isinstance(self.__max_num, int):
            return 2 ** 31
        return abs(self.__max_num)

    @property
    def args(self) -> ArgsType:
        return self.__args

    @property
    def kwargs(self) -> KwargsType:
        return self.__kwargs

    async def _impl_run(self):
        for index, item in enumerate(range(self.max_num)):
            t = asyncio.create_task(
                self.coro_func(*self.args, **self.kwargs),
                name=index
            )
            self.task.add_task(t)
            await asyncio.sleep(self.delay)

        for task in asyncio.as_completed(self.task):
            await task

    async def run(self):
        return await self._impl_run()

    def __str__(self):
        return f"{self.coro_func.__name__} + {self.delay} + {self.args}"


class EmitterMaster(AbstractEmitter):
    """
    并发器管理组
    """

    def __init__(self,
                 task: IEmitterTask,
                 delay: NumberTypes = 500,
                 date_unit: TimeUnit = TimeUnit.MS):
        super().__init__(task, delay, date_unit)

    @abc.abstractmethod
    def add(self, emitter: AbstractEmitter) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def extends(self, *emitters) -> None:
        raise NotImplementedError()

    async def run(self):
        return await self._impl_run()

    async def _impl_run(self):
        for emitter in self:
            self.task.add_task(asyncio.create_task(emitter.start()))
            await asyncio.sleep(self.delay)

        for task in asyncio.as_completed(self.task):
            await task

    @abc.abstractmethod
    def __iter__(self) -> typing.Iterable[AbstractEmitter]:
        raise NotImplementedError()


class EmitterGroup(EmitterMaster):
    """
    并发组
    """

    def __init__(self,
                 task: IEmitterTask,
                 delay: NumberTypes,
                 date_unit: TimeUnit = TimeUnit.MS):
        super().__init__(task, delay, date_unit)
        self.__emitters: typing.List[Emitter] = []

    @property
    def count(self) -> int:
        return len(self.emitters)

    @property
    def emitters(self) -> typing.List[Emitter]:
        return self.__emitters

    def add(self, emitter: Emitter) -> None:
        """
        单个添加并发器
        Args:
            emitter:

        Returns:

        """
        if not self._is_emitter(emitter):
            raise TypeError(f"emitter 必须是一个并发对象")
        self.emitters.append(emitter)

    def extends(self, *emitters) -> None:
        """
        批量添加并发器
        Args:
            *emitters:

        Returns:

        """
        if not emitters:
            return

        self.emitters.extend((emitter for emitter in emitters if self._is_emitter(emitter)))

    def _is_emitter(self, emitter: Emitter) -> bool:
        return isinstance(emitter, Emitter)

    def __iter__(self) -> typing.Iterable[Emitter]:
        for _, item in enumerate(range(self.count)):
            yield self._pop_head()

    def _pop_head(self) -> Emitter:
        return self.emitters.pop(0)


class EmitterCollection(EmitterMaster):
    """
    并发集合
    """

    def __init__(self,
                 task: IEmitterTask,
                 delay: NumberTypes = 500,
                 date_unit: TimeUnit = TimeUnit.MS):
        """
        并发管理器
        Args:
            delay:      延迟创建并发器任务时间
            date_unit:  时间单位
        """
        super().__init__(task, 2 ** 0, date_unit)
        self.__emitters: typing.Set[typing.Union[Emitter, EmitterGroup]] = set()

    @property
    def count(self) -> int:
        return len(self.emitters)

    @property
    def emitters(self) -> typing.Set[typing.Union[Emitter, EmitterGroup]]:
        return self.__emitters

    def add(self, emitter: typing.Union[Emitter, EmitterGroup]) -> None:
        """
        单个添加
        Args:
            emitter:

        Returns:

        """
        if not self._is_emitter(emitter):
            raise TypeError("emitter 必须是并发对象或并发组")

        self.emitters.add(emitter)

    def extends(self, *emitters) -> None:
        """
        批量添加并发器、并发组
        Args:
            *emitters:

        Returns:

        """
        self.emitters.update({emitter for emitter in emitters if self._is_emitter(emitter)})

    def _is_emitter(self, emitter: typing.Union[Emitter, EmitterGroup]) -> bool:
        return isinstance(emitter, (Emitter, EmitterGroup))

    def __iter__(self) -> typing.Iterable[typing.Union[Emitter, EmitterGroup]]:
        for _ in enumerate(range(self.count)):
            yield self.emitters.pop()
