#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/1/26 9:28
# @Author: SHAW
# @QQ:838705177
# -----------------------

'''
    dtmanager manage partterns
'''
import asyncio
import logging
import traceback
from socket import socket, AF_INET, SOCK_STREAM

from tornado.iostream import StreamClosedError

from tools import TcpDataTrans

logger = logging.getLogger(__name__)

class DTParserManager(object):

    def __init__(self,eofmethod="read_bytes",*eofargs,**eofkwargs):
        self.EOFARGS = eofargs
        self.EOFKWARGS = eofkwargs
        self.EOFMETHOD = eofmethod
        self._partterns = list()
        self._callback = None

    async def run(self,stream,address):
        try:
            while True:
                data = await getattr(stream,self.EOFMETHOD)(*self.EOFARGS,**self.EOFKWARGS)
                if asyncio.iscoroutinefunction(self._pre_callback):
                    data = await self._pre_callback(data)
                elif callable(self._pre_callback):
                    data = self._pre_callback(data)
                parseddata = self.data_parse(data,stream)
                if parseddata:
                    if asyncio.iscoroutinefunction(self._callback):
                        await self._callback(parseddata)
                    elif callable(self._callback):
                        self._callback(parseddata)
                else:
                    logger.warning("There is no dtee_script to parse the data")
        except StreamClosedError:
            logger.warning("Lost client at host %s", address)
        except Exception as e:
            traceback.print_exc()
            logger.warning("Exception Occur:%s", e)

    def add_parttern(self,dataparttern):
        self._partterns.append(dataparttern)

    def data_parse(self,data,stream):
        for parttern in self._partterns:
            parseddata = parttern.parse_data(data)
            if parseddata and stream:
                try:
                    return parttern.data_callback(parseddata,stream)
                except AttributeError:
                    return parseddata
        return False

    def add_callback(self,callback = None):
        if callback:self._callback = callback

    def add_pre_callback(self,callback = None):
        if callback:self._pre_callback = callback

    def _pre_callback(self,data):
        return data