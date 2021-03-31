#  Copyright (c) 2020 Bystrobank
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

__author__ = "Denis Borodulin, Maxim Kuznetsov"
__copyright__ = "Copyright 2020, Bystrobank"
__license__ = "MIT"
__version__ = "2.1.0"
__email__ = "borodulin@bystrobank.ru, kuznetsov_me@bystrobank.ru"
__status__ = "Development"

import time
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from pycontext.reader import ContextReader


class ContextVariable:
    """
    Context variable holder.
    """

    def __init__(
        self,
        name: str,
        source: "ContextReader",
        value: Any = None,
        locked: bool = False,
        expires: float = None,
    ) -> None:
        """
        Generic constructor.
        :param name: variable name
        :param source: variable source
        :param value: variable content
        :param locked: is variable locked for replace
        :param expires: time of the variable expiration
        """
        self._name = name
        self._source = source
        self._value = value
        self._locked = locked
        self._expires = expires
        self._creation_time = time.time()

    @property
    def name(self) -> str:
        return self._name

    @property
    def value(self) -> Any:
        return self._value

    @property
    def locked(self) -> bool:
        return self._locked

    @property
    def expired(self) -> bool:
        return False if self._expires is None else time.time() - self._creation_time > self._expires

    @property
    def source(self) -> "ContextReader":
        return self._source
