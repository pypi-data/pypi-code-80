# -*- coding: UTF-8 -*-

from functools import wraps
import time


def show_time_cost(func):
    """
    装饰器 @show_time_cost
    被装饰函数返回后将打印函数执行秒数
    """
    @wraps(func)
    def show_time_function(*args, **kwargs):
        print('\n-------------------------------\n{}：'.format(func.__name__))
        tp_s = time.time()
        func_rst = func(*args, **kwargs)
        tp_e = time.time()
        print('完成')
        print('耗时 {:.02f}'.format(tp_e - tp_s))
        return func_rst
    return show_time_function
