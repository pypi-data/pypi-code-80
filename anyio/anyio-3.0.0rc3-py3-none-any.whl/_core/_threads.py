from builtins import DeprecationWarning
from typing import Callable, Optional, TypeVar
from warnings import warn

from ..abc import CapacityLimiter
from ._eventloop import get_asynclib

T_Retval = TypeVar('T_Retval')


async def run_sync_in_worker_thread(
        func: Callable[..., T_Retval], *args, cancellable: bool = False,
        limiter: Optional[CapacityLimiter] = None) -> T_Retval:
    """
    Call the given function with the given arguments in a worker thread.

    If the ``cancellable`` option is enabled and the task waiting for its completion is cancelled,
    the thread will still run its course but its return value (or any raised exception) will be
    ignored.

    :param func: a callable
    :param args: positional arguments for the callable
    :param cancellable: ``True`` to allow cancellation of the operation
    :param limiter: capacity limiter to use to limit the total amount of threads running
        (if omitted, the default limiter is used)
    :return: an awaitable that yields the return value of the function.

    """
    warn('run_sync_in_worker_thread() is deprecated - use anyio.to_thread.run_sync() instead',
         DeprecationWarning)
    return await get_asynclib().run_sync_in_worker_thread(func, *args, cancellable=cancellable,
                                                          limiter=limiter)
