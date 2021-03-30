# -*- coding: utf-8 -*-
# @Time : 2021/3/18
# @Author : NotOne
# @Email : lvsongke@tianyancha.com

"""
统一处理各地方抓取数据
将汇总数据写入到mysql
"""

"""
统一调用此方法入库
"""
from redisAioSpider.baseSpider.base import BaseHandler
from redisAioSpider.utils.aioMysqlConnet import getAioMysql

import datetime


class MysqlSaveHandler(BaseHandler):

    def __init__(self, config, spiderName=None):
        super(MysqlSaveHandler, self).__init__()
        self.name = spiderName
        self.mysqlConfig = config
        self._init()

    async def init(self):
        if not hasattr(self, 'conn'):
            ## 连接交付库，重构库
            self.conn = await getAioMysql(self.mysqlConfig, self.loop)

    def _init(self):
        self.loop.run_until_complete(self.init())

    def formatUpdateSql(self, tableName, keys, values, sqlId=None):
        if not isinstance(keys, list):
            keys = list(keys)
        if not isinstance(values, list):
            values = list(values)
        for i, v in enumerate(values):
            if isinstance(v, datetime.datetime):
                values[i] = v.__str__()
        ## 执行更新命令
        kvList = []
        for i in range(len(keys)):
            k = str(keys[i])
            if isinstance(values[i], str):
                v = r"'{}'".format(str(values[i]))
            elif isinstance(values[i], datetime.datetime):
                v = r"'{}'".format(str(values[i]))
            elif isinstance(values[i], datetime.date):
                v = r"'{}'".format(str(values[i]))
            else:
                v = str(values[i])
            kvList.append('='.join([k, v]))
        updateField = ', '.join(kvList)
        if not updateField:
            raise ValueError('Update Field Is None')
        if not sqlId:
            raise ValueError('Must Have Primary Id')
        UPDATE_SQL = "UPDATE %s SET %s WHERE id=%s;" % (
            tableName, updateField, sqlId)
        UPDATE_SQL = UPDATE_SQL.replace(r"'None'", "NULL").replace("None", "NULL")
        return UPDATE_SQL

    def formatInsertSql(self, tableName, keys, values):
        if not tableName or not keys or not values:
            raise ValueError("The Lack Of Parameter")
        if not isinstance(keys, list):
            keys = list(keys)
        if not isinstance(values, list):
            values = list(values)
        for i, v in enumerate(values):
            if isinstance(v, datetime.datetime):
                values[i] = v.__str__()
        INSERT_SQL = """INSERT INTO `%s` %s VALUES %s""" % (tableName, tuple(keys), tuple(values))
        replaceSql = INSERT_SQL.split('VALUES')
        insertSql = replaceSql[0].replace(r"'", '').replace(r'\"', '')
        INSERT_SQL = 'VALUES'.join([insertSql, replaceSql[1]])
        INSERT_SQL = INSERT_SQL.replace(r"'None'", 'NULL').replace('None', 'NULL')
        return INSERT_SQL

    async def insert(self, tableName, keys, values):
        if not tableName or not keys or not values:
            raise ValueError("The Lack Of Parameter")
        _sql = self.formatInsertSql(tableName, keys, values)
        await self.conn.execute(_sql)


    async def update(self, tableName, keys, values, primeId):
        if not tableName or not keys or not values:
            raise ValueError("The Lack Of Parameter")
        if not primeId:
            raise ValueError('Must Have Primary Id')
        _sql = self.formatUpdateSql(tableName, keys, values, primeId)
        await self.conn.execute(_sql)
