import os


class _assets:
    def __init__(self):
        self.__path = os.getcwd() + '\\assets\\'


    def __call__(self, *args, **kwargs):
        args = list(args)
        if len(args) > 0:
            args[0] = self.__path + args[0]
        
        elif 'file' in kwargs:
            kwargs['file'] = self.__path + kwargs['file']
        
        return open(*args, **kwargs)


    def __exit__(self, exc_type, exc_value, traceback):
        pass

assets = _assets()