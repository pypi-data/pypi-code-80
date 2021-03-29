"""Provide custom function decoration for common logging requirements."""

import logging
import functools
import inspect
import itertools
import warnings


class LogFuncArgs(object):
    """Log arguments of a function using a supplied logger object."""

    def __init__(self, logger, level='DEBUG'):
        """Setup the logging decorator.

        :param logger: logging object used to emit logs
        :param level: log level of message to be emitted
        """
        self.logger = logger
        self.logger_level = logging.getLevelName(level)

    def __call__(self, func):
        """Execute function args logging on function call."""
        def merge_dicts(*dict_args):
            """Merge dicts and return single dict.

            Given any number of dicts, shallow copy and merge into a
            new dict, precedence goes to key value pairs in latter dicts.

            :param dict_args: dictionaries to be merged
            :type dict_args: dict
            :return: merged dict
            :rtype dict
            """
            result = {}
            for dictionary in dict_args:
                result.update(dictionary)
            return result

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """Log the entry, args and kwargs of a wrapped function."""
            # Log entry to the function
            self.logger.log(self.logger_level,
                            'Entering function {}'
                            .format(func.__name__))

            # Log the args and kwargs of the function
            args_dict = dict(zip(inspect.getargspec(func)[0], args))
            full_args_dict = merge_dicts(args_dict, kwargs)

            for k, v in full_args_dict.items():
                self.logger.log(self.logger_level,
                                "arg '{}' set to value '{}' on function '{}'"
                                .format(k, v, func.__name__))

            # Execute the original wrapped function
            func_result = func(*args, **kwargs)

            # Log leaving the function
            self.logger.log(self.logger_level,
                            'Exiting function {}'
                            .format(func.__name__))

            return func_result
        return wrapper


def deprecated(func):
    """Mark function as being deprecated and raise warning.

    This will result in a warning being emitted
    when the function is used.
    """
    @functools.wraps(func)
    def new_func(*args, **kwargs):
        """Emit warning for wrapped function marked as deprecated."""
        warnings.warn_explicit(
            "Call to deprecated function {}.".format(func.__name__),
            category=DeprecationWarning,
            filename=func.__code__.co_filename,
            lineno=func.__code__.co_firstlineno + 1
        )
        return func(*args, **kwargs)
    return new_func
