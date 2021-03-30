# Copyright (c) 2021 Alex Jamieson-Binnie
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import annotations

from typing import Any, TypeVar, Generic, Set, Union, Iterable, overload, AbstractSet

from typing_extensions import Protocol, runtime_checkable

TItem = TypeVar('TItem')
TItem2 = TypeVar("TItem2")

EmptySet = Set


@runtime_checkable
class InfiniteSet(Protocol[TItem]):
    """Protocol describing an infinite set, which can perform both membership queries and set operations, whilst
    not defining a length or being iterable."""

    def __contains__(self, item: TItem) -> bool:
        ...

    def __eq__(self, other: Any) -> bool:
        ...

    def __ne__(self, other: Any) -> bool:
        ...

    def __le__(self, other: Any) -> bool:
        ...

    def __lt__(self, other: Any) -> bool:
        ...

    def __ge__(self, other: Any) -> bool:
        ...

    def __gt__(self, other: Any) -> bool:
        ...

    def __and__(self, other: Any) -> 'InfiniteSet[Any]':
        ...

    def __or__(self, other: Any) -> 'InfiniteSet[Any]':
        ...

    def __sub__(self, other: Any) -> 'InfiniteSet[TItem]':
        ...

    def __xor__(self, other: Any) -> 'InfiniteSet[TItem]':
        ...

    def __repr__(self):
        return "everything()"


@runtime_checkable
class SupportsComplement(Protocol[TItem]):
    """Protocol for an object that can provide a set complement using complement()."""

    def __complement__(self) -> 'InfiniteSet[TItem]':
        ...


class UniversalSet(InfiniteSet[Any]):
    """Singleton representing the universal set of all objects."""

    def __contains__(self, item: Any) -> bool:
        return True

    def __eq__(self, other: Any) -> bool:
        # Univeral set is singleton, and only equal to itself.
        return other is self

    def __ne__(self, other: Any) -> bool:
        # Univeral set is singleton, and only equal to itself.
        return other is not self

    def __le__(self, other: Any) -> bool:
        # Universal set is only a subset of itself.
        return other is self

    def __lt__(self, other: Any) -> bool:
        # Universal set is not a strict subset of anything.
        return False

    def __ge__(self, other: Any) -> bool:
        # Univeral set is superset of everything.
        return True

    def __gt__(self, other: Any) -> bool:
        # Universal set is superset of all but itself.
        return other is not self

    def __or__(self, other: Any) -> 'UniversalSet':
        # Union with universal set is always universal set.
        return self

    def __ror__(self, other: Any) -> 'UniversalSet':
        return self

    def __and__(self, other: InfiniteSet[TItem]) -> InfiniteSet[TItem]:
        # Intersection with universal set is the set in question.
        return other

    def __rand__(self, other: InfiniteSet[TItem]) -> InfiniteSet[TItem]:
        return self & other

    def __sub__(self, other: InfiniteSet[TItem]) -> 'InfiniteSet[TItem]':
        # Complement of set defined as universal set - that set.
        return complement(other)

    def __rsub__(self, other: InfiniteSet[TItem]) -> EmptySet:
        return set()

    def __xor__(self, other: InfiniteSet[TItem]) -> 'InfiniteSet[TItem]':
        return self - other

    def __rxor__(self, other: InfiniteSet[TItem]) -> 'InfiniteSet[TItem]':
        return self ^ other

    def __complement__(self) -> Set:
        return set()


class SetComplement(Generic[TItem], InfiniteSet[TItem]):
    """Represents the set complement of a set A, consisting of everything that is not in A."""

    def __init__(self, except_set: Iterable[TItem]):
        self._except = set(except_set)

    def __contains__(self, item: Any) -> bool:
        return item not in self._except

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, self.__class__):
            return other._except == self._except
        return False

    def __ne__(self, other: Any) -> bool:
        return not (self == other)

    def __le__(self, other: Any) -> bool:
        if isinstance(other, self.__class__):
            return self._except >= other._except
        if other == everything():
            return True
        if isinstance(other, AbstractSet):
            return False
        return NotImplemented

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, self.__class__):
            return self._except > other._except
        if other == everything():
            return True
        if isinstance(other, AbstractSet):
            return False
        return NotImplemented

    def __ge__(self, other: Any) -> bool:
        if isinstance(other, self.__class__):
            return self._except <= other._except
        if other == everything():
            return False
        if isinstance(other, AbstractSet):
            return (self._except & other) == set()
        return NotImplemented

    def __gt__(self, other: Any) -> bool:
        if isinstance(other, self.__class__):
            return self._except < other._except
        if other == everything():
            return False
        if isinstance(other, AbstractSet):
            return (self._except & other) == set()
        return NotImplemented

    def __or__(self, other: InfiniteSet[TItem2]) -> InfiniteSet[Union[TItem, TItem2]]:
        if isinstance(other, self.__class__):
            return complement(self._except & other._except)  # type: ignore
        if other == everything():
            return everything()
        if isinstance(other, AbstractSet):
            return complement(self._except - other)
        return NotImplemented

    def __ror__(self, other: InfiniteSet[TItem2]) -> InfiniteSet[Union[TItem, TItem2]]:
        return self.__or__(other)  # type: ignore

    def __and__(self, other: InfiniteSet[TItem]) -> InfiniteSet[TItem]:
        if isinstance(other, self.__class__):
            return complement(self._except | other._except)
        if other == everything():
            return self.copy()
        if isinstance(other, AbstractSet):
            return other - self._except
        return NotImplemented

    def __rand__(self, other: InfiniteSet[TItem]) -> InfiniteSet[Union[TItem, TItem2]]:
        return self.__and__(other)  # type: ignore

    def __sub__(self, other: InfiniteSet[TItem]) -> InfiniteSet[TItem]:
        if isinstance(other, self.__class__):
            return other._except - self._except
        if other == everything():
            return set()
        if isinstance(other, AbstractSet):
            return complement(self._except | other)
        return NotImplemented

    def __rsub__(self, other: InfiniteSet[TItem]) -> InfiniteSet[TItem]:
        if isinstance(other, self.__class__):
            return self._except - other._except
        if other == everything():
            return everything()
        if isinstance(other, AbstractSet):
            return self._except & other
        return NotImplemented

    def __xor__(self, other: InfiniteSet[TItem]) -> InfiniteSet[TItem]:
        if isinstance(other, self.__class__):
            return self._except ^ other._except
        if other == everything():
            return self._except
        if isinstance(other, AbstractSet):
            return complement(self._except ^ other)
        return NotImplemented

    def __rxor__(self, other: InfiniteSet[TItem]) -> InfiniteSet[TItem]:
        return self.__xor__(other)

    def copy(self) -> 'SetComplement[TItem]':
        return complement(self._except.copy())  # type: ignore

    def __complement__(self) -> Set:
        return self._except.copy()

    def __repr__(self) -> str:
        return f"complement({self._except})"


UNIVERSAL_SET = UniversalSet()


def everything() -> UniversalSet:
    """The universal set of everything.

    This is an infinite set which contains everything, but cannot be iterated. It supports all set operations."""
    return UNIVERSAL_SET


@overload
def complement(other: UniversalSet) -> Set[Any]:
    ...


@overload
def complement(other: InfiniteSet[TItem]) -> InfiniteSet[TItem]:
    ...


def complement(other: InfiniteSet[TItem]) -> InfiniteSet[TItem]:
    """Return the set complement of a given set, which can be finite or infinite."""
    if isinstance(other, SupportsComplement):
        return other.__complement__()
    if isinstance(other, AbstractSet):
        if len(other) == 0:
            return everything()
        else:
            return SetComplement(other)
    raise ValueError(f"Cannot take set complement of {other}")


__all__ = ['complement', 'everything', 'InfiniteSet']
