#!/usr/bin/env python3
#
#  __init__.py
"""
Checker for pointless statements.
"""
#
#  Copyright © 2020-2021 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#  Based on pylint
#  See notebook2script/pointless.py for full copyright information
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License version 2
#  as published by the Free Software Foundation.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

# 3rd party
from pylint.checkers.base_checker import BaseChecker, BaseTokenChecker  # type: ignore
from pylint.utils import register_plugins  # type: ignore


def initialize(linter):
	"""
	Initialize linter with checkers in this package.
	"""

	register_plugins(linter, __path__[0])  # type: ignore


__all__ = ("BaseChecker", "BaseTokenChecker", "initialize")
