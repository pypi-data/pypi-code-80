# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 NetSPI <rtt.support@netspi.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
from typing import Optional


def log(message: str, context: Optional[str] = None):
    if context:
        print(f"[RTT:{context}] {message}")
    else:
        print(f"[RTT] {message}")


def warn(message: str):
    log(message, "-")


def error(message: str):
    log(message, "!")


def success(message: str):
    log(message, "+")


def debug(message: str):
    if os.environ.get('DEBUG', False):
        log(message, "=")
