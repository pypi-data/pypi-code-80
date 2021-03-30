# -*- coding: utf-8 -*-
# @Time : 2021/3/17
# @Author : NotOne
# @Email : lvsongke@tianyancha.com

import re
import asyncio
import requests

from functools import partial

from redisAioSpider.logger.logger import Logger
from redisAioSpider.utils.tools import parseSetCookie
from redisAioSpider.baseSpider.base import BaseHandler

requests.packages.urllib3.disable_warnings()


class NormalSpiderBaseHandler(BaseHandler):
    name = "normalBase"

    def __init__(self):
        super(NormalSpiderBaseHandler, self).__init__()
        self.loop = asyncio.get_event_loop()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
            'USE-RULE': 'true'
        }
        self.logger = Logger().get_logger(self.name, False)
        self.proxies = None

        self.delayTime = 0

    def checkResponse(self, resp):
        if resp.status_code in [500, 206]:
            self.logger.error('[ Error ] Url: {}, Status: {}'.format(resp.url, resp.status_code))
            return None
        # elif resp.status_code in [500, 206]:
        #     self.logger.error('[ warning ] Url: {}, Status: {}'.format(resp.url, resp.status_code))
        #     return None
        return resp

    async def RetryRequest(self, **kwargs):
        if "retryMaxNum" not in kwargs:
            retryMaxNum = 3
        else:
            retryMaxNum = kwargs.get("retryMaxNum")
            del kwargs['retryMaxNum']

        if "proxies" not in kwargs and self.proxies:
            kwargs["proxies"] = {"http": "http://" + self.proxies, "https": "http://" + self.proxies}
        if 'http' not in kwargs["proxies"]:
            kwargs["proxies"] = {"http": "http://" + kwargs["proxies"], "https": "http://" + kwargs["proxies"]}
        headers = kwargs.get('headers', self.headers)

        retry = 0
        resp = None
        while retry < retryMaxNum:
            retry += 1
            try:
                await asyncio.sleep(self.delayTime)
                resp = await aioRequest(**kwargs)
                resp = self.checkResponse(resp)
                if not resp:
                    if "Cookie" in headers:
                        subCookie = re.sub(r"proxyBase=[A-Za-z0-9=]{20,28};*", "", headers["Cookie"])
                        headers["Cookie"] = subCookie
                    continue
                if "Cookie" in headers:
                    newProxy = parseSetCookie(resp.headers["Set-Cookie"], cookieType="dict").get("proxyBase")
                    headers["Cookie"] = re.sub(r"proxyBase=[A-Za-z0-9=]{20,28};*", "proxyBase={}".format(newProxy),
                                               headers["Cookie"])
                return resp
            except Exception as err:
                self.logger.error(" [ Retry Error ] Error: {}".format(err))
                if "Cookie" in headers:
                    subCookie = re.sub(r"proxyBase=[A-Za-z0-9=]{20,28};*", "", headers["Cookie"])
                    headers["Cookie"] = subCookie
                resp = None
                continue
        return resp


def aioRequest(**kwargs):
    url = kwargs.get('url', None)
    if not url:
        raise ValueError('Missing URL parameter')
    del kwargs['url']

    method = kwargs.get('method', "GET").upper()
    loop = kwargs.get('loop', asyncio.get_event_loop())

    if 'method' in kwargs:
        del kwargs['method']
    if 'loop' in kwargs:
        del kwargs['loop']

    return loop.run_in_executor(None, partial(requests.request,
                                              method=method,
                                              url=url,
                                              **kwargs))
