import argparse
from ..pyckage import Pyckage, PyckageValidate


def clear(args: argparse.Namespace):
    """"""
    path = PyckageValidate.path(args.path)

    pyckage = Pyckage.load(path)
    pyckage.clear()