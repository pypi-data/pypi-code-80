from decimal import Decimal

from numformat.operators.decimal_operator import DecimalOperator
from numformat.operators.integer_operator import IntegerOperator
from numformat.utils import to_decimal, to_int


class OperatorFactory:

    @staticmethod
    def get_operator(value):
        if isinstance(value, int):
            return IntegerOperator(value)
        elif isinstance(value, float):
            return DecimalOperator(to_decimal(repr(value)))
        elif isinstance(value, Decimal):
            return DecimalOperator(value)
        elif isinstance(value, str):
            if '.' not in value:
                return IntegerOperator(to_int(value))
            return DecimalOperator(to_decimal(value))
        else:
            raise ValueError('Input type is not one of the supported types (int, float, decimal.Decimal, str). '
                             'Received object of type {}'.format(type(value)))
