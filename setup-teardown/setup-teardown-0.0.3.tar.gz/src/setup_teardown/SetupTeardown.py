import time
from functools import wraps


class ContextDecorator:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __enter__(self):
        return self

    def __exit__(self, typ, val, traceback):
        pass

    def __call__(self, f):
        @wraps(f)
        def wrapper(*args, **kw):
            with self:
                return f(*args, **kw)

        return wrapper


class SetupTeardown(ContextDecorator):
    def __enter__(self):
        self.setup(self)
        return self

    def __exit__(self, typ, val, traceback):
        self.teardown(self)

    def setup(self):
        print("setup")

    def teardown(self):
        print("teardown")
