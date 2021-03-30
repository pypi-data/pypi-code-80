import functools
from .. import logger, logger_b


def logger_wraps(*, entry=True, exit=True, level="TRACE"):
    def wrapper(func):
        name = func.__name__
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            logger_ = logger_b.opt(depth=1)
            if entry:
                logger_.log(level, "Entering '{}' (kwargs={})", name, kwargs)
            result = func(*args, **kwargs)
            if exit:
                logger_.log(level, "Exiting '{}' (result={})", name, result)
            return result
        return wrapped
    return wrapper

