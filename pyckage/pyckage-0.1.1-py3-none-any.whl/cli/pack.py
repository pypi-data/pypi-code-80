import os
import json
import argparse

from ..pyckage import Pyckage, _PYCKAGE_DATA as package_data
from ..pyckagelib.error import PyckageError


def pack(args: argparse.Namespace):
    """"""
    pyckage = Pyckage.pack(args)
    pyckage.save()