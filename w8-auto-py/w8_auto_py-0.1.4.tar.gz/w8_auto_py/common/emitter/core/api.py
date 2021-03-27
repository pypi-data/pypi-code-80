# @Time     : 2021/3/26
# @Project  : w8_auto_utils
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
import enum
import functools

from w8_auto_py.typings import ArgsType, Function, NumberTypes, KwargsType
from w8_auto_py.global_vars import TimeUnit
from w8_auto_py.common.emitter import AbstractEmitter, EmitterReturnType, Emitter, EmitterGroup, EmitterQueue, EmitterCollection
from w8_auto_py.common.runner import create_arunner, run


class Emitters(enum.Enum):
    EMITTER = Emitter
    EMITTER_GROUP = EmitterGroup
    EMITTER_COLLECTION = EmitterCollection


class EmitterFactory:

    @classmethod
    def create_task(cls, max_num: int) -> EmitterQueue:
        return EmitterQueue(max_len=max_num)

    @classmethod
    def _factory(cls,
                 emitters: Emitters,
                 delay: NumberTypes = 500,
                 date_unit: TimeUnit = TimeUnit.MS,
                 **kwargs) -> AbstractEmitter:
        if not isinstance(emitters, Emitters):
            raise TypeError("results must be EmitterResults Enum")

        f = functools.partial(
            emitters.value,
            delay=delay,
            date_unit=date_unit
        )
        return f(**kwargs)

    @classmethod
    def create(cls,
               emitters: Emitters,
               delay: NumberTypes = 500,
               date_unit: TimeUnit = TimeUnit.MS,
               max_num: int = None,
               **kwargs) -> AbstractEmitter:
        task = cls.create_task(max_num)
        return cls._factory(
            emitters=emitters,
            task=task,
            delay=delay,
            date_unit=date_unit,
            **kwargs
        )


def create_emitter(coro_func: Function,
                   args: ArgsType = None,
                   kwargs: KwargsType = None,
                   max_num: int = None,
                   delay: NumberTypes = 500,
                   date_unit: TimeUnit = TimeUnit.MS) -> Emitter:
    """
    创建 并发器
    Args:
        coro_func:
        args:
        kwargs:
        max_num:
        delay:
        date_unit:
    Returns:

    """
    return EmitterFactory.create(
        emitters=Emitters.EMITTER,
        coro_func=coro_func,
        delay=delay,
        date_unit=date_unit,
        max_num=max_num,
        args=args,
        kwargs=kwargs,
    )


def emitter_decorator(max_num: int = None,
                      delay: NumberTypes = 500,
                      date_unit: TimeUnit = TimeUnit.MS) -> Emitter:
    """
    并发包装器
    Args:
        max_num:
        delay:
        date_unit:

    Returns:

    """

    def _decorate(func: Function):
        @functools.wraps(func)
        def _wrapper(*args, **kwargs) -> Emitter:
            return create_emitter(
                coro_func=func,
                delay=delay,
                date_unit=date_unit,
                max_num=max_num,
                args=args,
                kwargs=kwargs
            )

        return _wrapper

    return _decorate


def create_emitter_group(max_num: int = None,
                         delay: NumberTypes = 500,
                         date_unit: TimeUnit = TimeUnit.MS) -> EmitterGroup:
    """
    创建 并发组
    Args:
        max_num:
        delay:
        date_unit:

    Returns:

    """

    return EmitterFactory.create(
        emitters=Emitters.EMITTER_GROUP,
        delay=delay,
        date_unit=date_unit
    )


def create_emitter_collection(max_num: int = None,
                              delay: NumberTypes = 500,
                              date_unit: TimeUnit = TimeUnit.MS) -> EmitterCollection:
    """
    创建 并发集合
    Args:
        max_num:
        delay:
        date_unit:

    Returns:

    """
    return EmitterFactory.create(
        emitters=Emitters.EMITTER_COLLECTION,
        delay=delay,
        date_unit=date_unit
    )


def start(emitter: AbstractEmitter) -> EmitterReturnType:
    """
    运行并发器
    Args:
        emitter:

    Returns:

    """
    runner = create_arunner(emitter.start())
    return run(runner)
