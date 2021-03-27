#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/3/27 14:41
# @Author: SHAW
# @QQ:838705177
# -----------------------
import traceback
from socket import socket, AF_INET, SOCK_STREAM

'''工具插件'''

def TcpDataTrans(data,ADDR):
    '''
        TCP数据包转发工具
        :param data Bytes,字节码数据,举例：b'##123MN=111222NP=222&&C33\r\n'
        :param ADDR tuple,socket元组，举例：('127.0.0.1',2000)
    '''
    try:
        tcpsocket = socket(AF_INET, SOCK_STREAM)
        tcpsocket.connect(ADDR)
        tcpsocket.sendall(data)
    except Exception as e:
        traceback.print_exc()
    finally:
        tcpsocket.close()