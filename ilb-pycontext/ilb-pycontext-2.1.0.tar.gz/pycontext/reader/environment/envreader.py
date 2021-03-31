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

import os
from typing import List

from pycontext import ContextVariable
from pycontext.reader.reader import ContextReader


class EnvironmentReader(ContextReader):
    """
    Reads reader.environment variables to list of reader.descriptor variables.
    """

    def __init__(self, produced_ttl: float = None):
        """
        Generic constructor
        :param produced_ttl: unique produced reader.descriptor element time to life
        """
        self._produced_ttl = produced_ttl

    def read_all(self) -> List[ContextVariable]:
        """
        Reads all reader.environment variables to list of the context variables.
        :return: list of context variables
        """
        values = []
        for key in os.environ:
            values.append(
                ContextVariable(
                    name=key,
                    source=self,
                    value=os.environ.get(key),
                    expires=self._produced_ttl,
                )
            )
        return values

    def read(self, key: str) -> "ContextVariable":
        """
        Reads reader.environment variable to context variable by key.
        :param key: variable key
        :return: context variable
        """
        if key in os.environ:
            return ContextVariable(
                name=key,
                source=self,
                value=os.environ.get(key),
                expires=self._produced_ttl,
            )
        else:
            raise ValueError(f"'key' variable not found in reader.environment")

    def __str__(self):
        return f"{type(self).__module__}.{type(self).__name__}]"
