#!/usr/bin/env python
# -*- coding:utf-8
from .libs import pyredis as pyredis
_redis=pyredis.PyRedis()

def Set(name, value,ex=None, px=None, nx=False, xx=False, keepttl=False):
    _redis.Set(name, value,ex, px, nx, xx, keepttl)

def Get(name):
    return _redis.Get(name)

def Delete(name):
    return _redis.Delete(name)

def Close():
    return _redis.Close()

def Client():
    _redis.Client()