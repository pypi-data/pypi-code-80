# -*- coding: UTF-8 -*-

import os
import sys
import redis
import platform
import logging
from enum import IntEnum
from .realDistrabutedLock import RealDLock


class RealLogLevel(IntEnum):
    TRACE   = 1
    DEBUG   = 2
    INFO    = 3
    WARNING = 4
    ERROR   = 5
    FATAL   = 6
    OFF     = 7


class RealLog(object):
    __srv_name = 'Real_Logger_Srv'
    __data_channel = __srv_name + '_data_channel'

    def __init__(self,
                 level: RealLogLevel = RealLogLevel.WARNING,
                 path: (str, type(None)) = None,
                 host: str = 'localhost',
                 port: int = 6379,
                 db: int = 0,
                 password: (str, type(None)) = None):
        super(RealLog, self).__init__()
        self.__level = level
        self.__path = path
        self.__host = host
        self.__port = port
        self.__db = db
        self.__password = password
        self.__conn = redis.StrictRedis(host=host,
                                        port=port,
                                        db=db,
                                        password=password,
                                        charset="utf-8",
                                        decode_responses=True)

    @staticmethod
    def __srv_init():
        return

    @staticmethod
    def __change_to_daemon():
        """
        将运行这个函数的进程变为Daemon进程
        :return:
            0   我是子进程
            >0  我是父进程
        """
        if platform.system().lower() != 'linux':
            raise EnvironmentError('SinaAgencyCa can only execute in linux.')
        # do the UNIX double-fork magic, see Stevens' "Advanced
        # Programming in the UNIX Environment" for details (ISBN 0201563177)
        try:
            pid = os.fork()
            if pid > 0:
                # tell the process func 'you are parent'
                return pid
        except OSError as e:
            raise RuntimeError(f'fork #1 failed: {e}\n')
        # decouple from parent environment
        os.chdir("/")
        os.setsid()
        os.umask(0)
        # do second fork
        try:
            pid = os.fork()
            if pid > 0:
                # tell the process func 'you are parent'
                return pid
        except OSError as e:
            raise RuntimeError(f'fork #2 failed: {e}\n')
        # 能执行到这里的，就是最终要得到的守护进程了
        # 重定向标准输入流、标准输出流、标准错误
        sys.stdout.flush()
        sys.stderr.flush()
        si = open("/dev/null", 'r')
        so = open("/dev/null", 'a+')
        se = open("/dev/null", 'ab+', 0)
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())
        return 0

    @staticmethod
    def __log_srv_proc(host: str, port: int, db: int, password: (str, type(None)), level: int, path: str):
        # 检查logger服务是否已经存在
        daemon_lock = RealDLock(lock_name=RealLog.__srv_name,
                                host=host,
                                port=port,
                                db=db,
                                password=password,
                                use_in_folk=True)
        if not daemon_lock.acquire_lock():
            # 服务已经启动
            sys.exit(0)
        # 将日志服务转换为守护进程
        fork_stat = RealLog.__change_to_daemon()
        if fork_stat != 0:
            # 结束fork出子进程的父进程
            sys.exit(0)
        # 转换守护进程成功，监控日志通道，最终写入日志文件
        conn = redis.StrictRedis(host=host, port=port, db=db, password=password, charset="utf-8", decode_responses=True)
        while True:
            data = conn.blpop(RealLog.__data_channel)
            # 指令处理
            if '----> stop srv' == data:
                conn.delete(RealLog.__data_channel)
                sys.exit(0)
            # 日志数据处理
            # todo: 停在这里
        return

    def init_logger(self) -> bool:
        return True
