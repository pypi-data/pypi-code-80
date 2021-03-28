import time


def execution_time(method, repeat_count=1):
    def timed(*args, **kwargs):
        for i in range(repeat_count):
            ts = time.time()
            result = method(*args, **kwargs)
            te = time.time()
            print('>>> function %r executed in %2.2f ms <<<' % (method.__name__, (te - ts) * 1000))

    return timed