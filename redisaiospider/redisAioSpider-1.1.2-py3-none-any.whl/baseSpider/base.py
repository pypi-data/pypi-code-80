# -*- coding: utf-8 -*-
# @Time : 2021/3/17
# @Author : NotOne
# @Email : lvsongke@tianyancha.com


"""
解析基类
"""
import asyncio
from redisAioSpider.logger.logger import Logger


class BaseHandler():
    name = "base"

    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
            'USE-RULE': 'true'
        }
        self.logger = Logger().get_logger(self.name, False)

    def start(self):
        self.logger.info('[ Task ] {} 开始启动...'.format(self.name))
        self.loop.run_until_complete(self.init())
        self.logger.info("Initialize Success")
        self.logger.info("Starting...")
        self.loop.run_until_complete(self.__start())

    async def init(self):
        pass

    async def __start(self):
        await self.__scheduler()

    async def __scheduler(self):
        # try:
        await self.scheduler()
        # finally:
        #     await self.releaseFutune()

    async def scheduler(self):
        pass
