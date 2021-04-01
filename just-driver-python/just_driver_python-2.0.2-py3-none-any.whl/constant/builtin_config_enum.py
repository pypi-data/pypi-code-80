import uuid
from collections import namedtuple
from enum import Enum

from just_driver.constant.type_enum import Type

PARAM = namedtuple("PARAM", ["name", "type", "default_value", "required"])


class BuiltInConfig(Enum):
    USER = PARAM(name="user", type=Type.STRING, default_value="", required=True)
    PRIVATE_KEY = PARAM(name="privateKey", type=Type.STRING, default_value="", required=True)
    DB = PARAM(name="db", type=Type.STRING, default_value="default", required=False)
    CONNECTION_ID = PARAM(name="connectionId", type=Type.STRING, default_value=uuid.uuid4().__str__(), required=False)
    PAGE_SIZE = PARAM(name="pagesize", type=Type.NUMBER, default_value="1000", required=False)
    MAX_RETRIES = PARAM(name="maxRetries", type=Type.NUMBER, default_value="3", required=False)
