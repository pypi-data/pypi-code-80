import asyncio
import logging
from contextlib import AsyncExitStack
from typing import Generic, Set, TypeVar

from vespucci.oracle import Oracle
from vespucci.store import Store

log = logging.getLogger(__name__)


N = TypeVar("N")


class Crawler(Generic[N]):
    _visited: Set[N]
    _LOG_FREQUENCY = 100

    def __init__(self, oracle: Oracle[N], store: Store[N]):
        self._oracle = oracle
        self._store = store
        self._process_task = None
        self._visited = set()

    async def seed(self, node: N, rank: int):
        await self._oracle.seed(node, rank)
        self._visited.add(node)

    async def _process(self):
        n_edges = 0
        async for (edge, rank) in self._oracle.reveal():
            log.debug("Crawler found edge %s of rank %d", edge, rank)
            await self._store.save(edge)
            if edge.dst is not None:
                n_edges += 1
                if n_edges % self._LOG_FREQUENCY == 0:
                    log.info("Crawler traversed %d edges", n_edges)

            if rank > 1 and edge.dst is not None and edge.dst not in self._visited:
                dsts = await self._store.load(edge.dst)
                if dsts:
                    # The neighborhood of edge.dst was already in the graph store
                    for dst in dsts:
                        await self.seed(dst, rank - 1)
                else:
                    await self.seed(edge.dst, rank - 1)
            else:
                in_process = self._oracle.in_process()
                log.debug("Crawler has %d nodes in process", in_process)
                if in_process <= 0:
                    log.info("Crawler traversed %d edges", n_edges)
                    return

    def run(self):
        return self._process_task

    async def __aenter__(self):
        self._process_task = asyncio.create_task(self._process())
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if not self._process_task.done():
            self._process_task.cancel()

    async def enter(self, stack: AsyncExitStack):
        return await stack.enter_async_context(self)
