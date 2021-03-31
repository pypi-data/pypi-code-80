#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/3/28 11:23
# @Author  : kiway
# @Software: PyCharm


import threading

import pymysql
# from DBUtils.PooledDB import PooledDB
from dbutils.pooled_db import PooledDB
import json
import os
from sqlalchemy import create_engine


class DbPool1(object):
    _instance_lock = threading.Lock()
    # _pool = None

    def __init__(self, dbname="mytest"):
        if not hasattr(self, f"_pool"):
            self.dbname = dbname
            self.mysql_pool(dbname)
        else:
            pass

    def config(self):
        with open(r"C:\Program Files\.configJson", "r") as f:
            configure = json.load(f)
        self.configure:dict = configure

        if self.configure.__contains__("maxsize"):
            self.maxsize = self.configure["maxsize"]
        else:
            self.maxsize = 15

        if self.configure.__contains__("host"):
            self.host = self.configure["host"]
        else:
            self.host = "127.0.0.1"

        if self.configure.__contains__("port"):
            self.port = self.configure["port"]
        else:
            self.port = 3306

        self.user = self.configure["user"]
        self.password = self.configure["password"]


    @classmethod
    def firsttime_setconfig(cls, configure:dict):
        """设置配置文件
        param : configure dict(
                            maxsize=10,         最大连接数
                            host='127.0.0.1',   主机名
                            port=3306,          端口
                            user='root',        用户名       该字段为必须
                            password='5218',    用户密码     该字段为必须
                            )
        """
        if not configure.__contains__("user"):
            raise ValueError("配置文件必须包含 ‘user’")

        if not configure.__contains__("password"):
            raise ValueError("配置文件必须包含 ‘password’")

        if not os.path.exists(r"C:\Program Files"):
            os.mkdir(r"C:\Program Files")

        with open(r"C:\Program Files\.configJson", "w") as f:
            json.dump(configure, f)
            print("配置文件设置成功")


    def __new__(cls, *args, **kwargs):
        if not hasattr(DbPool1, "_instance"):
            with DbPool1._instance_lock:
                if not hasattr(DbPool1, "_instance"):
                    DbPool1._instance = object.__new__(cls)
        return DbPool1._instance


    def mysql_pool(self, dbname):
        self.config()
        self._pool = PooledDB(
            creator=pymysql,  # 使用链接数据库的模块
            mincached=2,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
            maxcached=6,  # 链接池中最多闲置的链接，0和None不限制
            maxshared=3,
            # 链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，因为pymysql和MySQLdb等模块的 threadsafety都为1，所有值无论设置为多少，_maxcached永远为0，所以永远是所有链接都共享。
            maxconnections=self.maxsize,  # 连接池允许的最大连接数，0和None表示不限制连接数
            blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
            maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
            setsession=None,  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
            # ping MySQL服务端，检查是否服务可用。# 如：0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is created, 4 = when a query is executed, 7 = always
            host=self.host,
            port=self.port,
            user=self.user,
            passwd=self.password,
            db=dbname,       # TODO 需要动态修改
            use_unicode=True,
            charset='utf8'
        )

    def get_store_con(self):
        self.config()
        return create_engine(f"mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}")

    def get_con(self):

        return self._pool.connection()


class DbPool2(DbPool1):
    pass




