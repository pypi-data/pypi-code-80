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

from abc import ABC, abstractmethod
from typing import Any


class TypeParser(ABC):
    """
    Casts some values to Python objects by specific source types.
    """

    @abstractmethod
    def to_type(self, value: Any, val_type: str) -> Any:
        """
        Casts value to type from some source.
        :param value: value to cast
        :param val_type: type to cast
        :return: python obj
        """
        pass


class JavaTypeParser(TypeParser):
    """
    Casts Java primitives and it's object wrappers to python objects.
    """

    def to_type(self, value: Any, val_type: str) -> Any:
        """
        Casts value to type from reader.descriptor.
        :param value: value to cast
        :param val_type: Java type
        :raises ValueCastingError when cast is not possible
        :raises ValueError when type is not supported
        :return: python object
        """
        val_type = val_type.strip().lower()
        if value is None:
            return None
        elif val_type == "java.lang.string" or val_type == "javax.jms.queue":
            try:
                return str(value)
            except ValueError:
                raise ValueCastingError(value, str)
        elif val_type in ["java.lang.int", "java.lang.integer"]:
            try:
                return int(value)
            except ValueError:
                raise ValueCastingError(value, int)
        elif val_type == "java.lang.float":
            try:
                return float(value)
            except ValueError:
                raise ValueCastingError(value, float)
        elif val_type == "java.lang.boolean":
            if value == "true":
                return True
            elif value == "false":
                return False
            else:
                raise ValueCastingError(value, bool)
        else:
            raise ValueError(f"'{val_type}' type is not supported by {str(self)}")

    def __str__(self) -> str:
        return f"{type(self).__module__}.{type(self).__name__}"


class ValueCastingError(Exception):
    """
    Exception raises when some error occurs when casting value to Python object.
    """

    message = "Can't parse value to type"

    def __init__(self, value, val_type) -> None:
        self._value = value
        self._type = val_type

    def __str__(self) -> str:
        return f"{self.message}: '{self._value}' -> '{self._type}'"
