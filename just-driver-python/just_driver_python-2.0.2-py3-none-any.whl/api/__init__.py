from .errors import (
    Warning, Error, DataError, DatabaseError, ProgrammingError, IntegrityError,
    InterfaceError, InternalError, NotSupportedError, OperationalError
)
from .connection import Connection
from ..config.connection_config import ConnectionConfig
from ..constant.builtin_config_enum import BuiltInConfig

apilevel = '2.0'

paramstyle = 'pyformat'


def connect(user, private_key, urls,
            db=BuiltInConfig.DB.value.default_value,
            page_size=BuiltInConfig.PAGE_SIZE.value.default_value,
            max_reties=BuiltInConfig.MAX_RETRIES.value.default_value, **kwargs):
    """
    创建一个新的连接
    :return: 返回新的连接
    """
    max_reties = max(max_reties, BuiltInConfig.MAX_RETRIES.value.default_value)
    conn_config = ConnectionConfig(dict({
        BuiltInConfig.USER.value.name: user,
        BuiltInConfig.PRIVATE_KEY.value.name: private_key,
        'urls': urls,
        BuiltInConfig.DB.value.name: db,
        BuiltInConfig.PAGE_SIZE.value.name: page_size,
        BuiltInConfig.MAX_RETRIES.value.name: max_reties
    }, **kwargs))
    return Connection(conn_config)


__all__ = [
    'connect',
    'Warning', 'Error', 'DataError', 'DatabaseError', 'ProgrammingError',
    'IntegrityError', 'InterfaceError', 'InternalError', 'NotSupportedError',
    'OperationalError'
]
