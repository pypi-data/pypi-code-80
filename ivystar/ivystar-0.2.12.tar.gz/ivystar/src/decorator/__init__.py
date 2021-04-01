#!encoding=utf-8
import time, functools
import multiprocessing
import schedule, functools, time
import schedule

global l
l = multiprocessing.Lock()

''' 装饰器 '''

def timer(func):
    '''
    打印函数耗时
    '''
    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        print('excute in {:.2f} 秒'.format(time.time() - start))
        return res
    return wrapper

def prilog(func):
    '''
    打印函数名及耗时
    '''
    @functools.wraps(func)
    def wrapper(*args, **kw):
        start=time.time()
        r=func(*args, **kw)
        print('%s excute in %s ms' %(func.__name__, 1000*(time.time()-start)))
        return r
    return wrapper

def safethread(func):
    '''
    确保方法线程安全，未充分测试
    '''
    @functools.wraps(func)
    def wrapper(*args, **kw):
        global l
        start=time.time()
        l.acquire()
        r=func(*args, **kw)
        print('%s excute in %s ms and lock.acquire()' %(func.__name__, 1000*(time.time()-start)))
        l.release()
        return r
    return wrapper

'''
定时任务装饰器
使用schedule类定时运行task任务
'''
def run_task(task, freq=1, time_unit='minute'):
    '''定时执行任务'''
    if time_unit == 'second':
        schedule.every(freq).seconds.do(task)
    elif time_unit == 'minute':
        schedule.every(freq).minutes.do(task)
    elif time_unit == 'hour':
        schedule.every(freq).hour.do(task)
    elif time_unit == 'day':
        schedule.every(freq).day.at("4:30").do(task)

    while True:
        schedule.run_pending()
        time.sleep(1)

'''
定时任务装饰器
调用run_task任务
'''
def run_every(freq=1, time_unit='minute'):
    '''定时任务装饰器'''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            try:
                run_task(func, freq, time_unit)
            except:
                pass
        return wrapper
    return decorator

'''
@log
def fast(x, y):
    return x*y

fast(3, 5)
'''
