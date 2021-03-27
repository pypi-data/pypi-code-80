#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2020//24 16:04
# @Author: SHAW
# @QQ:838705177
# -----------------------
import json
from datetime import datetime
from urllib.parse import urlencode

from tornado.httpclient import HTTPRequest, AsyncHTTPClient
from tornado.options import options
from tornado.ioloop import IOLoop
import logging

from addon import TcpDataTrans
from server import DTCloudTcpServer
from config import *
from tools import init_logging
from dtee_script.dtee_main import dtparsermanager


async def pre_parse(data):
    '''数据接收到之后，解析之前，处理方式'''
    TcpDataTrans(data,('127.0.0.1',8076))  # 数据转发
    return data

dtparsermanager.add_pre_callback(pre_parse)

async def handle_data(data):
    '''manager callback'''
    print("handle_data data:",data)

dtparsermanager.add_callback(handle_data)

def main():
    init_logging()
    logging.info("Start listening，port:%s", options.port)
    server = DTCloudTcpServer(dtparsermanager)
    server.listen(options.port)
    server.start()
    IOLoop.current().start()

if __name__ == '__main__':
    main()

