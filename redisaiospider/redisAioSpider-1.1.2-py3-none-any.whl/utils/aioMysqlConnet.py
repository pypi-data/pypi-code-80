# -*- coding: utf-8 -*-
# @Time : 2021/1/8
# @Author : NotOne
# @Email : lvsongke@tianyancha.com

import aiomysql


class AioMysql(object):
    """
        MYSQL数据库对象，负责产生数据库连接 , 此类中的连接采用连接池实现
        获取连接对象：conn = Mysql.getConn()
        释放连接对象;conn.close()或del conn
    """

    # 连接池对象
    # __pool = None

    def __init__(self, sql_config):
        """
        数据库构造函数，从连接池中取出连接，并生成操作游标
        """
        self.coon = None
        self.pool = None
        self.sql_config = sql_config

    # @staticmethod
    async def initPool(self, loop=None):
        """
        @summary: 静态方法，从连接池中取出连接
        @return MySQLdb.connection
        """
        # if self.pool is None:
        # try:
        __pool = await aiomysql.create_pool(host=self.sql_config.DBHOST, port=self.sql_config.DBPORT,
                                            user=self.sql_config.DBUSER,
                                            password=self.sql_config.DBPWD,
                                            db=self.sql_config.DBNAME, minsize=5, maxsize=15, autocommit=True,
                                            loop=loop)
        return __pool
        # except:
        #     print('连接失败')

    async def getCurosr(self):
        conn = await self.pool.acquire()
        cur = await conn.cursor(aiomysql.DictCursor)
        return conn, cur

    async def query(self, query, param=None):
        """
        查询操作 返回一条数据
        :param query: sql语句
        :param param: 参数
        :return:
        """
        conn, cur = await self.getCurosr()
        try:
            await cur.execute(query, param)
            return await cur.fetchone()
        except Exception as err:
            print('出现错误:', err)
            print('出错sql:', query, param)
        finally:
            if cur:
                await cur.close()
            # 释放掉conn,将连接放回到连接池中
            await self.pool.release(conn)

    async def queryAll(self, query, param=None):
        """
        查询操作返回多条数据
        :param query: sql语句
        :param param: 参数
        :return:
        """
        conn, cur = await self.getCurosr()
        try:
            await cur.execute(query, param)
            return await cur.fetchall()
        except Exception as err:
            print('出现错误:', err)
            print('出错sql:', query, param)
        finally:
            if cur:
                await cur.close()
            # 释放掉conn,将连接放回到连接池中
            await self.pool.release(conn)

    async def execute(self, query, param=None):
        """
        增删改 操作
        :param query: sql语句
        :param param: 参数
        :return:
        """
        conn, cur = await self.getCurosr()
        try:
            await cur.execute(query, param)
            if cur.rowcount == 0:
                return False
            else:
                return True
        except Exception as err:
            print('出现错误:', err)
            print('出错sql:', query, param)
            return False
            # print(err)
        finally:
            if cur:
                await cur.close()
            # 释放掉conn,将连接放回到连接池中
            await self.pool.release(conn)

    async def beginQuery(self, queryList):
        """
        开启事务
        :return:
        """
        conn, cur = await self.getCurosr()
        if not isinstance(queryList, list):
            raise ValueError('Argument must be list')
        counter = 0

        ## 记录事务开启时的sqlList索引，如果回滚时收集失败的sql
        beginStart = 0
        await conn.begin()
        try:
            for query in queryList:
                await cur.execute(query)
                counter += 1
                # if counter % 100 == 0:
                #     ## 避免一次命令太多，导致事务超时
                #     await conn.commit()
                #     await conn.begin()
                #     beginStart = counter - 1
            res = cur.rowcount
            await conn.commit()
            return True, res
        except Exception as err:
            print('出现错误:', err)
            print('开始回滚')
            await conn.rollback()
            self.saveErrorSql(queryList[beginStart:])
            return False, err
        finally:
            if cur:
                await cur.close()
            # 释放掉conn,将连接放回到连接池中
            await self.pool.release(conn)

    def saveErrorSql(self, saveList):
        if not saveList:
            return
        import json
        with open('./errorGather/errorSqlList.json', 'a') as fs:
            fs.write(json.dumps(saveList) + '\n')


async def getAioMysql(sql_config, loop=None):
    mysqlobj = AioMysql(sql_config)
    pool = await mysqlobj.initPool(loop)
    mysqlobj.pool = pool
    return mysqlobj


if __name__ == '__main__':
    from redisAioSpider import config
    import asyncio

    loop = asyncio.get_event_loop()
    mysqlobj = loop.run_until_complete(getAioMysql(config.reset_sql_config))
    sqlList = []
    import json

    with open('../redisAioSpider/spider/save.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            sql = json.loads(line)
            sql = sql.replace(', 0,', ', 271611,')
            sqlList.append(sql)
    res = loop.run_until_complete(
        mysqlobj.beginQuery(
            sqlList))
    print(res)
