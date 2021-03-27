# @Time     : 2021/3/26
# @Project  : w8_auto_utils
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
import asyncio
import typing
from collections import deque

from w8_auto_py.common.validator import is_async_task
from w8_auto_py.common.emitter import AbstractEmitterTask

ATask = asyncio.Task
ATaskDeque = typing.Deque[ATask]
ATaskIterable = typing.Iterable[ATask]


class EmitterQueue(AbstractEmitterTask):
    """
    使用队列实现
    """

    def __init__(self, max_len: int = None):
        self.__max_len = max_len
        self.__queue = deque(maxlen=max_len)

    @property
    def count(self):
        return len(self.queue)

    @property
    def empty(self) -> bool:
        return len(self.count) <= 0

    @property
    def max_len(self) -> int:
        if not isinstance(self.__max_len, int):
            self.__max_len = 2 ** 31
        return abs(self.__max_len)

    @property
    def queue(self) -> ATaskDeque:
        return self.__queue

    def add_task(self, task: ATask, **kwargs) -> None:
        """
        单次添加
        Args:
            task:
            **kwargs:

        Returns:

        """
        if not is_async_task(task):
            raise TypeError(f"task must be asyncio.Task, use asyncio.create_task()")

        self.queue.append(task)

    def __iter__(self) -> ATaskIterable:
        for _ in enumerate(range(self.count)):
            yield self.popleft()

    def popleft(self) -> ATask:
        if self.count:
            return self.queue.popleft()
