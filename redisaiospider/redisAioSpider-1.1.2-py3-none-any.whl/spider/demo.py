# -*- coding: utf-8 -*-
# @Time : 2021/3/29
# @Author : NotOne
# @Email : lvsongke@tianyancha.com
import json

import redisAioSpider.config.sql_config

from redisAioSpider.baseSpider.redisSpiderBase import RedisSpiderBaseHandler
from redisAioSpider.components.saveToMysql import MysqlSaveHandler


class DemoRedisSpider(RedisSpiderBaseHandler):
    """
    信用
    """
    name = "demo"

    def __init__(self):
        super(DemoRedisSpider, self).__init__()

        ## 分布式接收任务种子队列名称
        self.redisQueue = 'redis_queue_name'

        ## 并发数
        self.tasks = 15

        ## mysqlHandler
        self.mysqlHandler = MysqlSaveHandler(redisAioSpider.config.sql_config)

    async def scheduler(self, event):
        """
        :return:
        """
        if isinstance(event, bytes):
            event = event.decode()
        if isinstance(event, str):
            event = json.loads(event)
        await self.getIndex(event)

    async def getIndex(self, event):
        """
        获取协程任务
        :param event:
        :return:
        """
        url = event.get('url')

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
        }
        ## 发起一个请求
        response = await self.RetryRequest(url=url, headers=headers, method="GET", verify=False)
        if not response:
            print("达到重试上限，放弃...")
            return

        if response.status_code == 404 or response.status_code >= 500:
            ### 处理响应异常数据
            print("出现异常响应状态码")
            print("处理这条字段标记")
            return
        ## 判断内容
        if "text1" in response.text:
            ### do something
            print("出现异常字段")
            print("处理这条字段标记")
            return

        pass

    async def parse(self, response):
        """
        解析数据
        :param data:
        :return:
        """
        pass


if __name__ == '__main__':
    DemoRedisSpider().start()
