"""`error.py` @ pyckage.pyckagelib

STATUS: COMPLETE
"""


class PyckageError(Exception):
    """"""


class PyckageExit(Exception):
    """"""

    def __init__(self, code: int = 0, *args: tuple, **kwargs: dict):
        Exception.__init__(self, *args, **kwargs)
        self.code = code