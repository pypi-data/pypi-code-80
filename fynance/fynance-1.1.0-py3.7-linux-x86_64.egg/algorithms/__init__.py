#!/usr/bin/env python3
# coding: utf-8
# @Author: ArthurBernard
# @Email: arthur.bernard.92@gmail.com
# @Date: 2019-09-12 17:54:50
# @Last modified by: ArthurBernard
# @Last modified time: 2020-09-25 19:31:40

"""

.. currentmodule:: fynance.algorithms

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   algorithms.allocation

"""

# Built-in packages

# Third party packages

# Local packages
from .allocation import *
from .browsers import *
from .browsers_cy import *

__all__ = allocation.__all__
__all__ += browsers.__all__
__all__ += browsers_cy.__all__
