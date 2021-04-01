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

import asyncio
import socket
from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Callable, List, Optional

import websockets

from rtt_sdk import logging

if TYPE_CHECKING:
    from rtt_sdk.client import RTTClient

from rtt_sdk.models import TicketInResponse


class WebsocketStream:
    def __init__(self, client: "RTTClient", ticket_url: str, websocket_url: Optional[str] = None):
        self._client = client
        self._ticket_url = ticket_url  # f"{self._tool}/tasks/feed"
        self._websocket_url = (
            websocket_url if websocket_url else ticket_url.replace("https://", "wss://").replace("http://", "ws://")
        )
        self._callbacks: List[Callable] = []
        self._ticket: Optional[TicketInResponse] = None
        self._reset_time: Optional[datetime] = None
        self._max_retries = 5
        self.cursor: str = ""

    def _refresh_ticket(self):
        self._ticket = TicketInResponse(**self._client.get(self._ticket_url))
        self._reset_time = datetime.now() + timedelta(minutes=self._ticket.expires_in - 1)

    def add_callback(self, callback: Callable) -> None:
        self._callbacks.append(callback)

    async def connect(self):
        while True:
            self._refresh_ticket()
            logging.debug("[STREAM] ticket refreshed.")
            try:
                cursor = self.cursor
                ws_url_with_ticket = f"{self._websocket_url}?ticket={self._ticket.ticket}"
                if cursor:
                    logging.debug("[STREAM] cursor: " + cursor)
                    ws_url_with_ticket += "&cursor=" + cursor
                else:
                    logging.debug("[STREAM] no cursor")
                async with websockets.connect(ws_url_with_ticket) as ws:
                    logging.debug("[STREAM] connected.")
                    while True:
                        try:
                            if cursor != self.cursor:
                                logging.debug("[STREAM] new cursor, reconnecting")
                                break
                            time_left = int((self._reset_time - datetime.now()).total_seconds())
                            ws_data = await asyncio.wait_for(ws.recv(), timeout=time_left)
                            for callback in self._callbacks[:]:
                                callback(ws_data)
                        except asyncio.TimeoutError:
                            break
                        except websockets.exceptions.ConnectionClosed:
                            try:
                                pong = await ws.ping()
                                await asyncio.wait_for(pong, timeout=5)
                                continue
                            except Exception:
                                break
            except socket.gaierror:
                continue
