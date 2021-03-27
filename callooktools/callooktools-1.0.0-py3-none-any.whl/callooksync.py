"""
callooktools: synchronous editon
---
Copyright 2021 classabbyamp, 0x5c
Released under the terms of the BSD 3-Clause license.
"""


from typing import Dict

import requests

from .callooktools import CallookAbc, CallookCallsignData, CallookError, URL


class CallookSync(CallookAbc):
    """The synchronous callook API object

    :param session: A requests session to use for requests
    :type session: requests.Session
    """
    def __init__(self, session: requests.Session = requests.Session()):
        self._session = session
        super().__init__()

    @property
    def session(self) -> requests.Session:
        """
        :getter: gets the requests session
        :rtype: requests.Session

        :setter: sets the requests session
        :type: requests.Session
        """
        return self._session

    @session.setter
    def session(self, val: requests.Session) -> None:
        self._session = val

    def get_callsign(self, callsign: str) -> CallookCallsignData:
        if not callsign.isalnum():
            raise CallookError("Invalid Callsign")
        resp_data = self._do_query(callsign)
        return self._process_callsign(resp_data)

    def _do_query(self, query: str) -> Dict:
        url = URL.format(callsign=query)
        with self._session.get(url) as resp:
            if resp.status_code != 200:
                raise CallookError(f"Unable to connect to callook.info (HTTP Error {resp.status_code})")
            return dict(resp.json())
