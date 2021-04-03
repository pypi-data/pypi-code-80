from decimal import Decimal
from math import floor, log10

from numformat.operators.operator import Operator


class IntegerOperator(Operator):

    def __init__(self, value: int):
        if not isinstance(value, int):
            raise ValueError('Expected int object but received {} object.'.format(type(value)))
        self.value = value

    def is_zero(self):
        return self.value == 0

    def get_order(self):
        if self.is_zero():
            return 0
        return floor(log10(abs(self.value))) + 1

    def get_sigfigs(self):
        return len(str(abs(self.value)).strip('0'))

    def set_sigfigs(self, desired_sig_figs):
        if desired_sig_figs is not None:
            if desired_sig_figs < self.get_sigfigs():
                order = self.get_order()
                self.value = round(self.value, desired_sig_figs - order)

    def to_standard_notation(self):
        return str(self.value)

    def to_scientific_notation(self):
        sn_format = '{{:.{}e}}'.format(max(self.get_sigfigs() - 1, 0))
        return sn_format.format(self.value)

    def to_engineering_notation(self):
        sci = self.to_scientific_notation()
        return Decimal(sci).to_eng_string()

    def __str__(self):
        return self.to_standard_notation()
