#!/usr/bin/env python3
from math import log, floor, ceil


def E_fwd(series: int, idx: int) -> float:
    """ Returns the value for a given E-series at the given index

    Args:
        series (int): The E series to target
        idx (int): The index of the series to get the value of [0 to series-1]

    Returns:
        float: E-series base value
    """
    if series in [3, 6, 12, 24]:
        p = 1
    else:
        p = 2
    return round((10**idx)**(1 / series), p)  # Return the (range)-root of 10^idx


def E_inv(series: int, val: float) -> float:
    """Returns the exact (continous) index for a given value on a given series.

    Args:
        series (int): The E series to target
        val (float): The value to find a base for

    Returns:
        float: The floating idx the value corrosponds to.
    """

    return log(val**series) / log(10)


def get_base(val: float) -> (float, float):
    """Get the base of a float [0-10[ float

    Args:
        val (float): The float to reduce to a single digit value

    Returns:
        float: The single digit representation of the float
        float: The exponent the value was reduced by. Negative for <0 values
    """

    exponent = 0
    while val >= 10:
        exponent += 1
        val /= 10

    while val < 1:
        exponent -= 1
        val *= 10
    return val, exponent


class EEValue(float):
    """ Class that provides EE friendly numbers
    Provides with automatic prefixing and standard value fitting
    """

    E24_series_overrides = ((10, 11, 12, 13, 14, 15, 16, 22), (2.7, 3.0, 3.3, 3.6, 3.9, 4.3, 4.7, 8.2))
    Si_prefixes = ('y', 'z', 'a', 'f', 'p', 'n', 'µ', 'm', '', 'k', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')

    def __new__(cls, value):
        cls.base, cls.exponent = get_base(float(value))
        return super(EEValue, EEValue).__new__(cls, value)

    def E(cls, series: int = 96, mode: str = 'round', legacy: bool = True) -> float:

        idx = E_inv(series, cls.base)

        if mode == "round":
            idx = round(idx)
        elif mode == "ceil":
            idx = ceil(idx)
        elif mode == "floor":
            idx = floor(idx)
        else:
            raise ValueError('Mode has to be either "round", "ceil" or "floor". {} is not a valid mode'.format(mode))

        if series in [3, 6, 12, 24]:
            if idx in cls.E24_series_overrides[0]:
                return EEValue(cls.E24_series_overrides[1][cls.E24_series_overrides[0].index(idx)] * 10**cls.exponent)

        return EEValue(E_fwd(series, idx) * 10**cls.exponent)

    def __str__(cls):
        idx = cls.exponent // 3 + 8
        prefix = cls.Si_prefixes[idx]
        val = float(cls) / 10**((idx - 8) * 3)  # We do this to keep to 3 orders of magnitude
        return "%.2f %s" % (val, prefix)

    def __repr__(cls):
        return "EEValue(%f)" % int(cls)

    # Arithmetic overloads
    def __add__(cls, other):
        res = super(EEValue, cls).__add__(other)
        return cls.__class__(res)

    def __sub__(cls, other):
        res = super(EEValue, cls).__sub__(other)
        return cls.__class__(res)

    def __mul__(cls, other):
        res = super(EEValue, cls).__mul__(other)
        return cls.__class__(res)

    def __div__(cls, other):
        res = super(EEValue, cls).__div__(other)
        return cls.__class__(res)

    def __floordiv__(cls, other):
        res = super(EEValue, cls).__floordiv__(other)
        return cls.__class__(res)

    def __truediv__(cls, other):
        res = super(EEValue, cls).__truediv__(other)
        return cls.__class__(res)

    def __mod__(cls, other):
        res = super(EEValue, cls).__mod__(other)
        return cls.__class__(res)

    def __divmod__(cls, other):
        res = super(EEValue, cls).__divmod__(other)
        return cls.__class__(res)

    def __pow__(cls, other):
        res = super(EEValue, cls).__pow__(other)
        return cls.__class__(res)

    def __radd__(cls, other):
        res = super(EEValue, cls).__radd__(other)
        return cls.__class__(res)

    def __rsub__(cls, other):
        res = super(EEValue, cls).__rsub__(other)
        return cls.__class__(res)

    def __rmul__(cls, other):
        res = super(EEValue, cls).__rmul__(other)
        return cls.__class__(res)

    def __rfloordiv__(cls, other):
        res = super(EEValue, cls).__rfloordiv__(other)
        return cls.__class__(res)

    def __rtruediv__(cls, other):
        res = super(EEValue, cls).__rtruediv__(other)
        return cls.__class__(res)

    def __rmod__(cls, other):
        res = super(EEValue, cls).__rmod__(other)
        return cls.__class__(res)

    def __rdivmod__(cls, other):
        res = super(EEValue, cls).__rdivmod__(other)
        return cls.__class__(res)

    def __rpow__(cls, other):
        res = super(EEValue, cls).__rpow__(other)
        return cls.__class__(res)
