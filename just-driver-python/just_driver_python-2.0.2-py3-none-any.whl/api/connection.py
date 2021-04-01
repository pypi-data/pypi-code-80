from just_driver.api.errors import JustConnectionError
from just_driver.config.connection_config import ConnectionConfig
from just_driver.constant.request_enum import RequestEnum
from just_driver.log import logger


class Connection(object):
    """
    创建访问JUST数据库的连接

    连接封装了客户端的很多cursor，请不要直接初始化Connection
    """

    def __init__(self, conn_config: ConnectionConfig):
        self._conn_config = conn_config
        self.is_closed = False
        from just_driver.api.service import Service
        self.service = Service(self)
        self.open_connection()

    def open_connection(self):
        body = {"request": RequestEnum.OPEN_CONNECTION.value,
                "connectionId": self._conn_config.connection_id,
                "info": self._conn_config.all_config()
                }
        # 最大尝试次数为用户自定义的最大尝试次数和URLS的数量的最大值
        max_retries = max(self._conn_config.max_retries, len(self._conn_config.urls))
        i = 0
        self._conn_config.current_uri = None
        for _ in range(max_retries):
            if self._conn_config.current_uri:
                break
            for url in self._conn_config.urls:
                try:
                    self._conn_config.current_uri = url
                    self.service.request(body)
                except JustConnectionError:
                    self._conn_config.current_uri = None
                    i += 1
                    logger.warning('connection lost, retry {}'.format(i))
                    if i > max_retries:
                        raise JustConnectionError("JUST已达最大尝试连接次数!")
                else:
                    self._conn_config.current_uri = url
                    logger.info("JUST已与``%s``成功建立连接！".format(self._conn_config.current_uri))
                    break

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def conn_config(self):
        return self._conn_config

    def close(self):
        # TODO close cursor
        close_connection_request = {
            "request": RequestEnum.CLOSE_CONNECTION.value,
            "connectionId": self._conn_config.connection_id
        }
        self.is_closed = True
        self.service.request(close_connection_request)
        logger.info("JUST已与``%s``成功断开连接！", self._conn_config.current_uri)

    def commit(self):
        """
        什么都不做，目前JUST不支持事务
        """
        pass

    def rollback(self):
        """
        什么都不做，目前JUST不支持事务
        """
        pass

    def cursor(self):
        """
        :return: 返回一个新的Cursor对象
        """
        from .cursor import Cursor
        if self.is_closed:
            raise Exception('connection already closed')

        # TODO 同步ConnectionSync
        return Cursor(self)

    def set_db(self, db_name: str):
        connection_sync_request = {
            "request": RequestEnum.CONNECTION_SYNC.value,
            "connectionId": self._conn_config.connection_id,
            "connProps": {
                "connProps": "connPropsImpl",
                "autoCommit": None,
                "readOnly": None,
                "transactionIsolation": None,
                "catalog": db_name,
                "schema": None,
                "dirty": None
            }
        }
        self.service.request(connection_sync_request)
        self._conn_config.db = db_name
        logger.info("JUST已成功切换为``%s``数据库！", db_name)
