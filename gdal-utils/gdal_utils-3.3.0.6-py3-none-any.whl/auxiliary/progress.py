#!/usr/bin/env python3
###############################################################################
# $Id$
#
# Project:  GDAL
# Purpose:  Handles progress callback functions
# Author:   Idan Miara <idan@miara.com>
#
###############################################################################
# Copyright (c) 2020, Idan Miara <idan@miara.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
###############################################################################

from numbers import Real
from typing import Optional, Union, Callable

ProgressCallback = Optional[Callable[[Real], None]]
ProgressCallbackOrDefault = Union[type(...), ProgressCallback]


def simple_print_progres(r1: Real):
    print(str(round(r1*100)) + '%', end=" ")


def print_progress_from_to(r0: Real, r1: Real):
    """ prints the progress from r0 to r1 """
    i0 = 0 if (r0 is None) or (r0 > r1) else round(r0 * 100) + 1
    i1 = round(r1 * 100) + 1
    for i in range(i0, i1):
        print(str(i) if i % 5 == 0 else ".", end="", flush=True)
    if r1 >= 1:
        print("% done!")


def get_progress_callback(callback: ProgressCallbackOrDefault) -> ProgressCallback:
    """ returns the default progress callback (input is Ellipsis) or the given callback (otherwise) """
    if callback is None:
        return None
    elif callback is ...:
        last = None

        def print_progress(prog, *_):
            nonlocal last

            r0 = last
            r1 = prog
            print_progress_from_to(r0, r1)
            last = prog
        return print_progress

    return callback
