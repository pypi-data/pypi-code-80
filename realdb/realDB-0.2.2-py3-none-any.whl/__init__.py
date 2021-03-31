# -*- coding: UTF-8 -*-

from .sqlite import RealDB as Sqlite
from .postgres import RealDB as Postgres


def ver():
    return '0.2.2'
