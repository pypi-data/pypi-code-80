"""tree.py @ pyckage.pyckagelib
"""
import os
import abc
import pathlib

from .data import PackageData
from .tracker import FileTracker
from .template import FileTemplate


class FileTree(object, metaclass=abc.ABCMeta):

    DIR = "DIR"
    FILE = "FILE"

    FILE_TYPES = {FILE, DIR, None}

    __datum__ = {}

    @classmethod
    def set(self, **kwargs):
        self.__datum__.update(kwargs)

    @classmethod
    def get(self, key: str):
        return self.__datum__[key]

    def __init__(
        self,
        type_: str,
        head: str = None,
        tail: list = None,
        *,
        cond: bool = True,
        template: FileTemplate = None,
    ):
        """"""
        self.type = type_
        self.head = head
        self.cond = cond

        if tail is None:
            self.tail = []
        else:
            self.tail = [subtree for subtree in tail if subtree.cond]

        self.template = template

    def __repr__(self, level: int = 0) -> str:
        """"""
        if self.tail:
            return (
                f"FileTree({self.type}, {self.head!r}, ["
                + "\n"
                + ",\n".join(
                    (
                        "\t" * (level + 1)
                        + f"{item.__repr__(level+1) if type(item) is type(self) else repr(item)}"
                        for item in self.tail
                    )
                )
                + "\n"
                + "\t" * level
            )
        else:
            return f"FileTree({self.type}, {self.head!r})"

    @classmethod
    def root(cls, tail: list):
        """"""
        return cls(None, None, tail)

    def grow(self, root_path: pathlib.Path, *, tracker: FileTracker = None):
        """"""
        if tracker is None:
            raise ValueError("`tracker` is None.")

        if self.type is not None:
            if not self.cond:
                return

            path = root_path.joinpath(self.head)

            tracker.create(self.type, path, template=self.template)
        else:
            path = root_path

        if self.tail is not None:
            for subtree in self.tail:
                subtree.grow(path, tracker=tracker)