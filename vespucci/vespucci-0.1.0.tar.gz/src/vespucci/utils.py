import asyncio
from typing import Mapping, Hashable


async def switch(queues: Mapping[Hashable, asyncio.Queue]):
    if not queues:
        return

    def wrap(tag, queue):
        async def fn():
            x = await queue.get()
            return (tag, x)

        return asyncio.create_task(fn())

    aws = set(wrap(t, q) for (t, q) in queues.items())
    done, pending = await asyncio.wait(aws, return_when=asyncio.FIRST_COMPLETED)
    gather = asyncio.gather(*pending)
    gather.cancel()
    try:
        await gather
    except asyncio.CancelledError:
        pass
    for t in done:
        yield t.result()
