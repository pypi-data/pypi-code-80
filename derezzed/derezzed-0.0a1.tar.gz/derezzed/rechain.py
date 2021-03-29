"""Place strings into categories.

Classes:

    RegularExpressionChain
"""

import re
from typing import List
from typing import Tuple


class RegularExpressionChain:
    """
    Reduces the resolution of a string to a category using regular expressions.

    The category is found by testing the string using regular expressions in
    sequence until a match is found. This allows for more specific strings to
    be matched first, with less specific strings being matched only if the more
    specific string did not match.

    The regular expressions will be compiled when the class is initialised to
    make subsequent matching more efficient.

    :param patterns: ordered list of identifiers and regular expressions
    """

    _chain: List[Tuple[str, re.Pattern]]

    def __init__(self, patterns: List[Tuple[str, str]]):
        """Create a new RegularExpressionChain."""
        self._chain = [(r[0], re.compile(r[1])) for r in patterns]

    def match(self, string: str, case_insensitive: bool = False) -> str:
        """Returns an identifier for the first match of a regular expression.

        Each regular expression in the chain will be tested against the
        provided string in sequence until a match is found, and then the
        identifier will be returned. If no match is found, "other" is returned.

        :param string: string to match on
        """
        if case_insensitive:
            string = string.lower()
        for identifier, regex in self._chain:
            if regex.match(string):
                return identifier
        return "other"
