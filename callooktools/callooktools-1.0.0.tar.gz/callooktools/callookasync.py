"""
callooktools: asynchronous editon
---
Copyright 2021 classabbyamp, 0x5c
Released under the terms of the BSD 3-Clause license.
"""


from typing import Dict, Optional

import aiohttp

from .callooktools import CallookAbc, CallookCallsignData, CallookError, URL


class CallookAsync(CallookAbc):
    """The asynchronous callook API object

    :param session: An aiohttp session to use for requests
    :type session: Optional[aiohttp.ClientSession]
    """
    def __init__(self, session: Optional[aiohttp.ClientSession] = None):
        self._session = session
        super().__init__()

    @property
    def session(self) -> aiohttp.ClientSession:
        """
        :getter: gets the aiohttp session
        :rtype: aiohttp.ClientSession

        :setter: sets the aiohttp session
        :type: aiohttp.ClientSession
        """
        return self._session

    @session.setter
    def session(self, val: aiohttp.ClientSession) -> None:
        self._session = val

    async def start_session(self) -> None:
        """Creates a new ``aiohttp.ClientSession`` object for the :class:`CallookAsync` object"""
        self._session = aiohttp.ClientSession()

    async def close_session(self) -> None:
        """Closes a ``aiohttp.ClientSession`` session for the :class:`CallookAsync` object"""
        await self._session.close()

    async def get_callsign(self, callsign: str) -> CallookCallsignData:
        if not callsign.isalnum():
            raise CallookError("Invalid Callsign")
        resp_data = await self._do_query(callsign)
        return self._process_callsign(resp_data)

    async def _do_query(self, query: str) -> Dict:
        url = URL.format(callsign=query)
        async with self._session.get(url) as resp:
            if resp.status != 200:
                raise CallookError(f"Unable to connect to callook.info (HTTP Error {resp.status})")
            return dict(resp.json())
