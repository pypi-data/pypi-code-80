"""
Copyright 2021-2021 The jdh99 Authors. All rights reserved.
knocky包用于通信时帧头和帧正文处理解耦
帧正文处理函数注册成knock包的服务,帧头处理调用服务,调用knock服务获取响应数据
Authors: jdh99 <jdh821@163.com>
"""

_services = dict()


def call(protocol: int, cmd: int, req: bytearray, *args) -> (bytearray, bool):
    """Call 同步调用.返回值是应答字节流和是否需要应答标志"""
    global _services

    rid = cmd + (protocol << 16)
    if rid not in _services:
        return bytearray(), False
    resp, result = _services[rid](req, *args)
    if resp is None:
        return bytearray(), False
    else:
        return resp, result


def register(protocol: int, cmd: int, callback):
    """
    注册服务回调函数
    callback是回调函数,格式:func(req: bytearray, *args) -> (bytearray, bool)
    回调函数的返回值是应答数据和应答标志.应答标志为false表示不需要应答
    """
    global _services

    rid = cmd + (protocol << 16)
    _services[rid] = callback
