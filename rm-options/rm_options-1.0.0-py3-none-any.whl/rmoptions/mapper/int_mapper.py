from .base_mapper import BaseMapper

'''
IntMapper

Mapper to parse string values to integers.
'''


class IntMapper(BaseMapper):

    def __init__(self):
        BaseMapper.__init__(self)

    def get_target_type_name(self):
        return "int"

    def map(self, value):
        if value.isnumeric():
            return int(value)
        return None
