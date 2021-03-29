import functools
from .core import db


# def getattribute(self, *args, **kwargs):
#     print('__getattribute__ %r' % args)
#
#     attr = args[0]
#
#     if isinstance(attr, str) and not (attr.startswith('__') or attr in ['setup', 'teardown']):
#         # self.setup()
#         result = super(self.__class__, self).__getattribute__(attr)
#         # self.teardown()
#         return result
#
#     return super(self.__class__, self).__getattribute__(attr)


def rpc(cls):
    origin_init = cls.__init__
    origin_getattribute = cls.__getattribute__

    @functools.wraps(origin_init)
    def initialize(self, *args, **kwargs):
        origin_init(self, *args, **kwargs)
        self.db = db

    @functools.wraps(cls)
    def getattribute(self, *args, **kwargs):
        print('__getattribute__ %r' % args)

        attr = args[0]

        if isinstance(attr, str) and not (attr.startswith('__') or attr in ['setup', 'teardown']):
            # self.setup()
            result = super(cls, self).__getattribute__(attr)
            # self.teardown()
            return result

        return super(cls, self).__getattribute__(attr)

    # def setup(self):
    #     print('setup...')
    #
    # def teardown(self):
    #     # noinspection PyBroadException
    #     try:
    #         db.remove()
    #     except Exception:
    #         pass

    cls.__init__ = initialize
    cls.__getattribute__ = getattribute

    # added setup & teardown
    # cls.setup = setup
    # cls.teardown = teardown

    return cls
