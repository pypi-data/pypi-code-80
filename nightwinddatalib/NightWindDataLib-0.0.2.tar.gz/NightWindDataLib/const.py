class ConstantReassignedError(TypeError):
    """raise this exception when constant is reassigned"""
    pass


class ConstantTypeConvertedError(TypeError):
    """raise this exception when constant is converted to a new type"""
    pass


class _const(object):
    def __setattr__(self, key, value):
        if key in self.__dict__:
            if isinstance(value, type(self.__dict__[key])):
                raise ConstantReassignedError("Constant can't be reassigned")
            else:
                raise ConstantTypeConvertedError("Constant type can't be converted")

        self.__dict__[key] = value


if __name__ == '__main__':
    import sys
    sys.modules[__name__] = _const()
