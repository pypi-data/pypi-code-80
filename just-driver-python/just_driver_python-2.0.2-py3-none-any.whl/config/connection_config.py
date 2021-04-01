from just_driver.api import DataError
from just_driver.config.connection_sync_config import ConnectionSyncConfig
from just_driver.constant.builtin_config_enum import BuiltInConfig
from just_driver.util.str_util import StrUtil


class ConnectionConfig:

    def __init__(self, prop: dict):
        self._prop = prop
        self._user = prop[BuiltInConfig.USER.value.name]
        self._private_key = prop[BuiltInConfig.PRIVATE_KEY.value.name]
        self._urls = prop["urls"]
        self._connection_id = prop.get(BuiltInConfig.CONNECTION_ID.value.name,
                                       BuiltInConfig.CONNECTION_ID.value.default_value)
        self._db = prop.get(BuiltInConfig.DB.value.name, BuiltInConfig.DB.value.default_value)
        self.page_size: int = int(
            prop.get(BuiltInConfig.PAGE_SIZE.value.name, BuiltInConfig.PAGE_SIZE.value.default_value))
        self.current_uri = None

    @property
    def connection_id(self):
        return self._connection_id

    @property
    def db(self):
        return self._db

    @db.setter
    def db(self, item):
        self._db = item
        self._prop[BuiltInConfig.DB.value.name] = item

    @property
    def urls(self):
        return [_ if _.startswith("http://") else "http://" + _
                for _ in self._urls.replace(" ", "").split(",")]

    @property
    def max_retries(self):
        return int(self._prop.get(BuiltInConfig.MAX_RETRIES.value.name, BuiltInConfig.MAX_RETRIES.value.default_value))

    @property
    def user(self):
        return self._user

    @property
    def private_key(self):
        return self._private_key

    def sync_config(self):
        return ConnectionSyncConfig(self._db, True)

    def all_config(self):
        # TODO
        return self._prop

    @staticmethod
    def check_config():
        for _, c in BuiltInConfig.__members__.items():
            if c.required and StrUtil.isblank(c.name):
                raise DataError("Config [{}] required.".format(c.name))
