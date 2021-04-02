import asyncio
import logging
from asyncio.queues import LifoQueue, Queue  # pylint: disable=ungrouped-imports
from contextlib import AsyncExitStack
from typing import AsyncGenerator, Callable, Generic, Tuple, TypeVar

from vespucci.base import Edge

log = logging.getLogger(__name__)


N = TypeVar("N")


class Oracle(Generic[N]):

    _in_process: int
    _seeds: Queue
    _revealed: Queue

    def __init__(self, fn: Callable[[N], Edge[N]], capacity: int = 100):
        self._fn = fn
        self._capacity = capacity
        self._seeds = LifoQueue(maxsize=self._capacity)
        self._revealed = Queue(maxsize=self._capacity)
        self._fn_calls = 0
        self._process_task = None

    async def enter(self, stack: AsyncExitStack):
        return await stack.enter_async_context(self)

    async def seed(self, node: N, rank: int):
        self._seeds.put_nowait((node, rank))

    async def reveal(self) -> AsyncGenerator[Tuple[Edge[N], int], None]:
        while True:
            (edge, rank) = await self._revealed.get()
            yield (edge, rank)

    def in_process(self) -> int:
        return self._seeds.qsize() + self._revealed.qsize() + self._fn_calls

    async def _process(self):
        while True:
            (node, rank) = await self._seeds.get()
            # TODO: Deal with self._fn(node) raising exceptions
            self._fn_calls += 1
            edges = [e for e in await self._fn(node) if e.src != e.dst]
            if edges:
                for edge in edges:
                    await self._revealed.put((edge, rank))
            else:
                # Pass control to a client waiting on a next edge to reveal
                await self._revealed.put((Edge(node, None), rank))
            self._fn_calls -= 1

    async def __aenter__(self):
        self._process_task = asyncio.create_task(self._process())
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if hasattr(self._process_task, "cancel"):
            self._process_task.cancel()
