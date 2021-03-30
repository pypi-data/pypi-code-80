# -*- coding: utf-8 -*-
# @Time : 2021/3/29
# @Author : NotOne
# @Email : lvsongke@tianyancha.com

import os
import inspect

from redisAioSpider.baseSpider.base import BaseHandler

# dirPath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
relPath = os.path.abspath(os.path.join(os.getcwd(), "."))


def runByName(name=None):
    runObj = None

    for path in [relPath]:
        if not os.path.exists(path + '/spider'):
            continue

        fileList = os.listdir(path + '/spider')
        _importModule = 'spider.'
        if not name:
            raise ValueError('Error Spider Name')

        for file in fileList:
            if '.py' not in file or '__init__' in file:
                continue
            moduleStr = file.replace('.py', '')
            importModule = _importModule + moduleStr
            HandlerModule = __import__(importModule)
            module = getattr(HandlerModule, moduleStr)
            for obj in vars(module).values():
                if (
                        inspect.isclass(obj)
                        and issubclass(obj, BaseHandler)
                        and obj.__module__ == module.__name__
                        and getattr(obj, 'name', None)
                ):
                    if obj.name == name:
                        runObj = obj
                        break
            if runObj:
                break
        if runObj:
            break

    if not runObj:
        print("Not Found Project {}".format(name))
        return
    try:
        print("Project {} Is Running".format(name))
        runObj().start()
    finally:
        print("Project {} Is End".format(name))


if __name__ == '__main__':
    runByName('credit_bejing')
