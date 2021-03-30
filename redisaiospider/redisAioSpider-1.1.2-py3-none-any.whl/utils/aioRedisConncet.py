# -*- coding: utf-8 -*-
# @Time : 2021/1/27
# @Author : NotOne
# @Email : lvsongke@tianyancha.com

import aioredis
import asyncio


class AioRedisConn():

    def __init__(self, redis_config, loop=None):
        """
        数据库构造函数，从连接池中取出连接，并生成操作游标
        """
        self.conn = None
        self.pool = None
        self.redis_config = redis_config
        if loop is None:
            loop = asyncio.get_event_loop()
        self.loop = loop

    # @staticmethod
    async def initPool(self):
        """
        @summary: 静态方法，从连接池中取出连接
        @return MySQLdb.connection
        """
        __pool = await aioredis.create_redis_pool(
            address='redis://' + ':'.join([self.redis_config.REDIS_HOST, str(self.redis_config.REDIS_PORT)]),
            password=self.redis_config.REDIS_PASSWORD,
            db=self.redis_config.DB_NAME, minsize=1, maxsize=15, loop=self.loop)
        return __pool


async def getAioRedis(redis_config, loop=None):
    _aioRedis = AioRedisConn(redis_config, loop)
    conn = await _aioRedis.initPool()
    _aioRedis.conn = conn
    return _aioRedis


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    # redis = loop.run_until_complete(test())
    # AioRedisConn().loop
    # loop.run_until_complete(redis.pool.hget('hset', '128282'))
