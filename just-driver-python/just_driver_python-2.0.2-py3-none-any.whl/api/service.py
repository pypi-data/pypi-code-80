import json

import requests

from just_driver.api import OperationalError, InternalError, ProgrammingError
from just_driver.api.connection import Connection
from just_driver.api.errors import JustConnectionError
from just_driver.log import logger


class Service:

    def __init__(self, conn: Connection):
        self._conn = conn

    def request(self, req_json):
        header = self._conn.conn_config.all_config()
        try:
            res = requests.post(self._conn.conn_config.current_uri, json=req_json, headers=header)
        except requests.exceptions.ConnectionError as e:
            logger.warning('connection lost', e)
            raise JustConnectionError('connection lost')
        res.encoding = "utf-8"
        if res.status_code == 200:
            return json.loads(res.text)
        elif res.status_code == 401:
            raise OperationalError('authentication failed, check your username or secret key')
        elif res.status_code == 500:
            logger.error('just db error: {}'.format(res.text))
            raise InternalError('just database internal error')
        elif res.status_code == 403:
            raise OperationalError('authority failed, check your permission')
        raise ProgrammingError('unknown error happend')
