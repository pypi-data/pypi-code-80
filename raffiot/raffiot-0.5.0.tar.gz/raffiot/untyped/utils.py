from collections import abc
from dataclasses import dataclass
from enum import IntEnum
from collections import abc

__all__ = [
    "MatchError",
    "MultipleExceptions",
    "ComputationStatus",
    "seq",
    "DomainErrors",
]


@dataclass(frozen=True)
class MatchError(Exception):
    """
    Exception for pattern matching errors (used internally, should NEVER happen).
    """

    __slots__ = ["message"]

    message: None


@dataclass(frozen=True)
class MultipleExceptions(Exception):
    """
    Represents
    """

    exceptions: None
    """
    The list exceptions encountered
    """

    errors: None
    """
    The list of errors encountered
    """

    @classmethod
    def merge(cls, *exceptions, errors=None):
        """
        Merge some exceptions, retuning the exceptions if there is only one
        or a  `MultipleExceptions` otherwise.

        :param exceptions:
        :param errors:
        :return:
        """
        stack = [exn for exn in exceptions]
        base_exceptions = []
        errs = [x for x in errors] if errors else []

        while stack:
            item = stack.pop()
            if isinstance(item, MultipleExceptions):
                stack.extend(item.exceptions)
                errs.extend(item.errors)
                continue
            if isinstance(item, abc.Iterable) and not isinstance(item, str):
                stack.extend(item)
                continue
            base_exceptions.append(item)

        if len(base_exceptions) == 1:
            return base_exceptions[0]
        base_exceptions.reverse()
        return MultipleExceptions(base_exceptions, [])


@dataclass(frozen=True)
class DomainErrors(Exception):
    """
    Errors from the business domain
    """

    errors: None


class ComputationStatus(IntEnum):
    FAILED = 0
    SUCCEEDED = 1


def seq(*a):
    """
    The result is the result of the last argument.

    Accepts a single list or multiple arguments.
    :param a:
    :return:
    """
    if len(a) == 1 and isinstance(a[0], abc.Iterable):
        return a[0][-1]
    return a[-1]
