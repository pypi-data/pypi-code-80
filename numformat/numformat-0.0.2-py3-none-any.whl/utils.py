from decimal import Decimal, InvalidOperation
from math import floor, log10


def convert_to_numeric(value):
    if isinstance(value, int):
        return value
    elif isinstance(value, float):
        return to_decimal(repr(value))
    elif isinstance(value, str):
        if '.' not in value:
            return to_int(value)
        return to_decimal(value)
    else:
        raise ValueError('Input was not in any of the supported formats '
                         'int, float, decimal.Decimal. Received object of type {}'.format(type(value)))


def get_order(value):
    if isinstance(value, Decimal) and value.is_zero():
        return 0
    elif isinstance(value, int) and value == 0:
        return 0
    order = floor(log10(abs(value))) + 1
    return order


def is_zero(value):
    if isinstance(value, int):
        return value == 0
    elif isinstance(value, Decimal):
        return value.is_zero()
    else:
        return False


def to_decimal(value):
    try:
        value = Decimal(value)
    except InvalidOperation:
        raise ValueError('Input is not a valid number - {}'.format(value))
    return value


def to_int(value):
    try:
        value = int(value)
    except ValueError:
        raise ValueError('Input is not a valid number - {}'.format(value))
    return value
