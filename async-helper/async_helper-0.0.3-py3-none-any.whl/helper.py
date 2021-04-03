#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import asyncio

__all__ = ['first_sequential_result', 'first_parallel_result']


def first_sequential_result(functions, satisfied=lambda _: True):
    """
    Runs a list of functions sequentially and returns
    the result of the function which terminated first
    without an `Exception`.
    Optionally skips a result if the `satisfied`
    callable returns `False`.
    """
    for function in functions:
        result = first_parallel_result([function],
                                       satisfied=satisfied)
        if result:
            return result

def first_parallel_result(functions, satisfied=lambda _: True):
    """
    Runs a list of functions in parallel and returns
    the result of the function which terminated first
    without an `Exception`.
    Optionally skips a result if the `satisfied`
    callable returns `False`.
    """

    # Get a valid envent loop
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    # Canceller
    def cancel(pending):
        for task in pending:
            task : asyncio.Task
            task.cancel()

    # The actual worker
    async def run_parallel():
        pending = {(asyncio.create_task(async_function(*fn))) for fn in functions}
        while pending:
            done, pending = await asyncio.wait(pending, 
                                               return_when=asyncio.FIRST_COMPLETED)
            for d in done:
                e = d.exception()
                if e:
                    continue
                result = d.result()
                if satisfied(result):
                    cancel(pending)
                    return d.result()

    # Wrapper for synchronous functions with
    # optional lag as the first parameter
    async def async_function(*args, **kwargs):
        args = list(args)
        a = args.pop(0)
        if callable(a):
            function, lag = a, 0
        else:
            function, lag = args.pop(0), a
        if lag:
            await asyncio.sleep(lag)
        res = await loop.run_in_executor(None, function, *args, **kwargs)
        return res

    # Do the work and connect to the async world
    return loop.run_until_complete(run_parallel())
