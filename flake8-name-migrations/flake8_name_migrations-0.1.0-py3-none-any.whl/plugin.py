import re
import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ast import Module
    from typing import Generator

if sys.version_info >= (3, 8):
    from importlib.metadata import version
else:
    # noinspection PyUnresolvedReferences
    from importlib_metadata import version

migration_pattern = re.compile(r'[0-9]{4}_auto\w+.py')


class Plugin:
    """Flake8 plugin."""

    name = 'flake8-name-migrations'
    version = version('flake8-name-migrations')

    __slots__ = ('filename',)

    def __init__(self, tree: 'Module', filename: str) -> None:
        self.filename = filename

    def run(self) -> 'Generator':
        """Yield errors in flake8-specified format."""
        if migration_pattern.search(self.filename):
            yield 1, 0, f'NMI001: Rename {self.filename} to something human readable', None
