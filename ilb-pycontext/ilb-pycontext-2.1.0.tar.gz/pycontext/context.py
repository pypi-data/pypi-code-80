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

import logging
from typing import List, Any, Optional

from pycontext import ContextVariable
from pycontext.reader import ContextReader

logger = logging.getLogger(__name__)


class AppContext:
    """
    Holds and manages application context from specified context sources.
    """

    @staticmethod
    def from_readers(readers: List[ContextReader]) -> "AppContext":
        """
        Fills app context by list of context readers.
        Merges same variables in order of context readers.
        :param readers: context readers which provide context variables
        :return: filled app context
        """
        context: List[ContextVariable] = []

        # Reverse readers list to support source prioritization.
        # Variables from first by order source has the highest priority.
        readers.reverse()

        for reader in readers:
            try:
                new_variables = reader.read_all()
                for new_variable in new_variables:
                    exist_variable = next((var for var in context if var.name == new_variable.name), None)
                    if exist_variable is not None:
                        if not exist_variable.locked:
                            context.remove(exist_variable)
                            context.append(new_variable)
                    else:
                        context.append(new_variable)
            except Exception as e:
                raise ContextBuildError(str(e))

        return AppContext(context=context)

    def __init__(self, context: List[ContextVariable]) -> None:
        """
        Generic constructor.
        :param context: list of context variables
        """
        self._context = context

    def get(self, key: str) -> Optional[Any]:
        """
        Returns variable from context by it's name.
        :param key: variable name
        :raises KeyError when variable doesn't exist in context
        :return: variable
        """
        try:
            variable = next(var for var in self._context if var.name == key)
            if variable.expired:
                updated_variable: Optional[ContextVariable] = self._update_variable(variable)
                return updated_variable.value if updated_variable is not None else None
        except StopIteration:
            logger.warning(f"'{key}' doesn't exist in app context")
            return None

        return variable.value

    def _update_variable(self, expired_variable: ContextVariable) -> Optional[ContextVariable]:
        try:
            upd_variable = expired_variable.source.read(expired_variable.name)
            self._context.remove(expired_variable)
            self._context.append(upd_variable)
            return upd_variable
        except ValueError:
            self._context.remove(expired_variable)
            logger.warning(
                f"'{expired_variable.name}' doesn't exist in app context. "
                f"That variable has expired and there was an attempt to update, "
                f"but it's gone from the original source - {str(expired_variable.source)}"
            )
            return None


class ContextBuildError(Exception):
    message = "Error when building application context"

    def __init__(self, description) -> None:
        self._description = description

    def __str__(self) -> str:
        return f"{self.message}: {self._description}"
