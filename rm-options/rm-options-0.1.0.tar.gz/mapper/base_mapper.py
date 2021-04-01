"""
BaseMapper class

it's a default class for the mapper.
Override this class to create a new mapper.
"""


class BaseMapper(object):

    def __init__(self):
        pass

    # is needed for error messages
    # it's the name of the target type (for example 'int', 'AnyClass')
    def get_target_type_name(self):
        raise NotImplementedError

    # this is the mapping method.
    # you should return the mapped object, or a non object when something wents wrong.
    def map(self, option):
        raise NotImplementedError
