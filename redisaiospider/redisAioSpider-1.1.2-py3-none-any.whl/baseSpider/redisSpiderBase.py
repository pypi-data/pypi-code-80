# -*- coding: utf-8 -*-
# @Time : 2021/3/17
# @Author : NotOne
# @Email : lvsongke@tianyancha.com
import asyncio

from redisAioSpider.config import redis_config

from redisAioSpider.utils.aioRedisConncet import getAioRedis
from redisAioSpider.baseSpider.normalSpiderBase import NormalSpiderBaseHandler


class RedisSpiderBaseHandler(NormalSpiderBaseHandler):
    name = "redisSpider"

    def __init__(self):
        super(RedisSpiderBaseHandler, self).__init__()
        ## 任务发布队列
        self.redisQueue = 'project_keys:accept_keys'
        ## 并发任务数
        self.tasks = 1

        self.redisConfig = redis_config
        self.timeSleep = 0

    def start(self):
        self.logger.info('[ Task ] {} 开始启动...'.format(self.name))
        self.loop.run_until_complete(self.init())
        self.logger.info("Initialize Success")
        self.logger.info("Starting...")
        self.loop.run_until_complete(self.__start())

    async def init(self):
        if not hasattr(self, 'redis'):
            self.redis = await getAioRedis(self.redisConfig, loop=self.loop)

    async def __start(self):
        while True:
            while await self.redis.conn.exists(self.redisQueue):
                ## 这里无法利用异步的特性，对于start这个函数来说 while循环是阻塞的
                if self.tasks <= 0:
                    await asyncio.sleep(0.5)
                    # self.logger.info("并行协程已满，等待中")
                    continue
                self.tasks -= 1
                event = await self.redis.conn.lpop(self.redisQueue)
                if event:
                    event = event.decode()
                else:
                    continue

                ### 将执行futune丢给子线程去执行，不阻塞主线程
                async def coroutine():
                    return self.loop.create_task(self.__scheduler(event))

                asyncio.run_coroutine_threadsafe(coroutine(), loop=self.loop)
                ### 将协程 或者 futune 聚合在一个loop event 中进行调度
            await asyncio.sleep(2)

    async def __scheduler(self, *args):
        try:
            await self.scheduler(*args)
        finally:
            await self.releaseFutune()

    async def releaseFutune(self):
        try:
            await asyncio.sleep(self.timeSleep)
        ## 通过一个全局变量来控制协程并发数 协程并发控制
        finally:
            self.tasks += 1

    async def scheduler(self, *args):
        pass
