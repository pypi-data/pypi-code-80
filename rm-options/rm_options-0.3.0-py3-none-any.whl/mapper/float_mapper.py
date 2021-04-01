from .base_mapper import BaseMapper

'''
FloatMapper

Mapper to parse string values to floats.
'''


class FloatMapper(BaseMapper):

    def __init__(self):
        BaseMapper.__init__(self)

    def get_target_type_name(self):
        return "float"

    def map(self, value):
        try:
            return float(value)
        except ValueError:
            return None
