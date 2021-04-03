from decimal import Decimal
from math import floor, log10

from numformat.operators.integer_operator import IntegerOperator


class DecimalOperator(IntegerOperator):

    def __init__(self, value: Decimal):
        if not isinstance(value, Decimal):
            raise ValueError('Expected Decimal object but received {} object.'.format(type(value)))
        self.value = value
        self.is_integer = False
        self.integer_operator: IntegerOperator = None

    def is_zero(self):
        if self.is_integer:
            return self.integer_operator.is_zero()
        return self.value.is_zero()

    def get_order(self):
        if self.is_zero():
            return 0
        return floor(log10(abs(self.value))) + 1

    def get_sigfigs(self):

        if self.is_integer:
            return self.integer_operator.get_sigfigs()

        value_str = str(abs(self.value))
        decimal_point_index = len(value_str.split('.')[0])
        for i in range(len(value_str)):
            if value_str[i].isdigit():
                if value_str[i] != '0':
                    return len(value_str) - i - (1 if i < decimal_point_index else 0)
        return 0

    def set_sigfigs(self, desired_sig_figs):

        if self.is_integer:
            return self.integer_operator.set_sigfigs(desired_sig_figs)

        if desired_sig_figs is not None:
            if desired_sig_figs < self.get_sigfigs():
                order = self.get_order()
                self.value = round(self.value, desired_sig_figs - order)
                if (self.value % 1) == 0:
                    self.value = int(self.value)
                    self.is_integer = True
                    super(DecimalOperator, self).__init__(self.value)
                    self.integer_operator = super(DecimalOperator, self)
                else:
                    self.is_integer = False
                    self.integer_operator = None

    def to_standard_notation(self):
        if self.is_integer:
            return self.integer_operator.to_standard_notation()
        return str(self.value)

    def to_scientific_notation(self):
        if self.is_integer:
            return self.integer_operator.to_scientific_notation()
        sn_format = '{{:.{}e}}'.format(max(self.get_sigfigs() - 1, 0))
        return sn_format.format(self.value)

    def to_engineering_notation(self):
        if self.is_integer:
            return self.integer_operator.to_engineering_notation()
        return self.value.normalize().to_eng_string()

    def __str__(self):
        return self.to_standard_notation()
