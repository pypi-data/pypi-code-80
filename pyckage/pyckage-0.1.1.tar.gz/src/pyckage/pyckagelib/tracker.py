"""tracker.py @ pyckage.pyckagelib

"""
import os
import sys
from pathlib import Path

from .template import FileTemplate


class FileTracker:
    """"""

    DIR = "DIR"
    FILE = "FILE"

    FILE_TYPES = {DIR, FILE}

    def __init__(self, pathlog: list = None):
        self.pathlog = (
            [(type_, Path(path)) for type_, path in pathlog]
            if pathlog is not None
            else []
        )

    @staticmethod
    def touch(path: str):
        """"""
        with open(path, "a"):
            pass

    def clear(self):
        """"""
        while self.pathlog:
            type_, path = self.pathlog.pop()
            try:
                if type_ == self.FILE:
                    os.remove(path)
                    print(f"Remove FILE `{path}`.")
                elif type_ == self.DIR:
                    os.rmdir(path)
                    print(f"Remove DIR `{path}`.")
                else:
                    raise TypeError
            except:
                raise EnvironmentError(
                    "Fatal Error: run `pyckage fix` or try fixing package contents manually."
                )

    def create(self, type_: str, path: Path, template: FileTemplate = None):
        """"""
        if path.exists():
            raise FileExistsError(f"`{path}` already exists.")
        elif type_ in self.FILE_TYPES:
            if type_ == self.DIR:
                print(f"Create FILE `{path}`.")
                os.mkdir(path)
                self.pathlog.append((type_, path))

            elif type_ == self.FILE:
                print(f"Create DIR `{path}`.")
                if template is None:
                    self.touch(path)
                else:
                    template.make(path=path)
                self.pathlog.append((type_, path))

            else:
                raise TypeError(f"Invalid type {type_}.")
        else:
            raise TypeError(f"Invalid type {type_}.")


__all__ = ["FileTracker"]