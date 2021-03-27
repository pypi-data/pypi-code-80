"""template.py @ pyckage.pyckagelib

This utility allows for file template generation, applying changes from a given dictionary.
"""
from pathlib import Path


class FileFormatter(dict):
    """"""

    def __getitem__(self, key):
        value = dict.__getitem__(self, key)
        return f"{{{key}}}" if value is None else value

    def __missing__(self, key):
        return f"{{{key}}}"


class FileTemplate:
    """"""

    FILE = "FILE"

    __hooks__ = {}
    __datum__ = {}

    def __init__(self, source: Path, *, key: str = None, info: dict = None):
        self.source = source
        self.info = info
        self.key = key

    @classmethod
    def set(self, **kwargs):
        self.__datum__.update(kwargs)

    @classmethod
    def get(self, key: str):
        return self.__datum__[key]

    @classmethod
    def template(cls, key: str):
        """Registers new template hook. A template hook is a bound method.

        Every hook is recorded under a key. Calling a template's make function with the `template` keyword argument will use `template` as key for loading the hook. Just as said, using the `args` and `kwargs` keyword arguments will tell what to pass for the hook.

        hook's return is a string telling from which file to read the template, i.e., overrides `from_` normal behavior. Thus, a regular use case would be to create a new template file from the usual one and use it right away. This allows for advanced template building. You might want to make use of the `tempfile` module.

        Parameters
        ----------
        key: str
            hook registry key
        """

        def decor(callback):
            cls.__hooks__[key] = callback
            return callback

        return decor

    def __default_hook(self, from_: Path, to_: Path) -> (str, str):
        """Default behavior is to look at the package data folder."""
        return (from_, to_)

    def make(self, path: Path):
        """"""
        ## Retrieve path information
        if self.key in self.__hooks__:
            source_path, dest_path = self.__hooks__[self.key](self, self.source, path)
        else:
            source_path, dest_path = self.__default_hook(self.source, path)

        ## Read template file
        with open(source_path, mode="r") as r_file:
            content = r_file.read()

        with open(dest_path, "w") as w_file:
            if self.info is None:
                w_file.write(content)
            else:
                w_file.write(content.format_map(FileFormatter(self.info)))


__all__ = ["FileTemplate"]