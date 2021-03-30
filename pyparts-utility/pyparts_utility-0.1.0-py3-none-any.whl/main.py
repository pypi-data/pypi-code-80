import ast
import collections
import click
import os
import inspect
from pyparts_utility.formating import *
from click.termui import get_terminal_size

# from typing_extensions import TypeAlias

# collections.


# string = 'print("hello")'
# print(dir(x))


class Line:
    def __init__(self, content: str) -> None:
        self.content = content

    def add(self, content: str):

        self.content += content


# print(x.body)
class Input:
    """
    Determine and collect the sum of the content that will be fed to the
    main proccess
    """

    def __init__(self) -> None:

        self.files = []
        self.content = []

        for x, _, z in os.walk(os.getcwd()):

            for i in z:
                j = os.path.join(x, i)
                j = os.path.relpath(j)

                if os.path.splitext(j)[1] == ".py":
                    self.files.append(os.path.relpath(j))

                    with open(j, "r") as f:
                        self.content.append(f.read())


class NodeInfo:
    def __init__(self, obj, depth) -> None:
        self.obj = obj
        self.depth = depth
        self.bases = self.get_attr_ifexists(obj, "bases")

        if type(self.bases) is list and len(self.bases) > 0:
            self.basenames = [self.get_attr_ifexists(base, "id") for base in self.bases]
        else:
            self.basenames = None

        # print(self.basenames)

        # print(self.bases)

    def get_attr_ifexists(self, obj, attr: str):

        if hasattr(obj, attr):
            return getattr(obj, attr)
        else:
            return None


class Formatter:
    """
    Recurses through an ast and formats the output
    """

    def __init__(self, top_lvl, file_path: str) -> None:
        self.objects = []
        self.file_path = file_path
        self._recurse_body(top_lvl)
        self.indent_char = "\t"

    def _recieve_obj(self, obj, depth):

        self.objects.append(NodeInfo(obj, depth))
        pass

    def _recurse_body(self, body, depth=0):

        for item in body:
            self._recieve_obj(item, depth)

            if hasattr(item, "body"):
                self._recurse_body(item.body, depth + 1)

    def _indent(self, incrementer: int):
        return self.indent_char * incrementer

    def _run(self, method):

        method = getattr(self, method)
        click.secho(self.file_path, dim=True)
        for info_obj in self.objects:
            method(info_obj)

    def class_tree(self, info):

        (obj, depth) = info.obj, info.depth

        self.indent_char = "\t"
        if info.basenames is not None:
            indent = self._indent(len(info.basenames))
        else:
            indent = self._indent(0)

        line = Line("")
        values = list(obj.__dict__.values())
        type_name = type(obj).__name__

        if type_name != "ClassDef":
            return

        if info.basenames is not None:

            line.add(str(values[0]))
            line.add("(")
            for i, base in enumerate(info.basenames):
                if i == len(info.basenames) - 1:
                    line.add(click.style(base, dim=True))
                else:
                    line.add(click.style(base + ", ", dim=True))
            line.add(")")
        else:
            line.add(click.style(indent + str(values[0]), bold=True))

        print_inside(line.content)


def main():

    formatters = []
    i = Input()

    for file, lines in zip(i.files, i.content):

        x = ast.parse(source=lines)
        formatters.append(Formatter(x.body, file))

    for f in formatters:
        f._run("class_tree")


# print(ast.dump(x, indent=4))
# print(type(out))

# compile('print("hello")')