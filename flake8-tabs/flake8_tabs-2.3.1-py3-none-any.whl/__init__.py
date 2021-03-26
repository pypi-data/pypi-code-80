"""
Tab (or Spaces) indentation style checker for flake8
"""
import typing as ty

from . import blanklineck
from . import config
from . import indentationck
from . import misc


__version__: ty.Final[str] = misc.__version__

Config             = config.Config
BlankLinesChecker  = blanklineck.Checker
IndentationChecker = indentationck.Checker