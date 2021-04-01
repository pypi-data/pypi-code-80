#!/usr/bin/env python3
from math import log, floor, ceil


def E_fwd(series: int, idx: int, legacy: bool = True) -> float:
    """ Returns the value for a given E-series at the given index

    Args:
        series (int): The E series to target
        idx (int): The index of the series to get the value of [0 to series-1]
        legacy (bool): If it should return the legacy values for the lower E-series

    Returns:
        float: E-series base value
    """

    E24_overrides = ((10, 11, 12, 13, 14, 15, 16, 22), (2.7, 3.0, 3.3, 3.6, 3.9, 4.3, 4.7, 8.2))

    calculated_base = (10**idx)**(1 / series)  # The (range)th-root of 10^idx

    if series in [3, 6, 12, 24]:
        e24_idx = idx * (24 / series)
        if e24_idx in E24_overrides[0] and legacy:
            base = E24_overrides[1][E24_overrides[0].index(e24_idx)]
            return base

        calculated_base = round(calculated_base, 1)
    else:
        calculated_base = round(calculated_base, 2)

    return calculated_base


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

    Si_prefixes = ('y', 'z', 'a', 'f', 'p', 'n', 'µ', 'm', '', 'k', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')

    def __new__(cls, value, precision=2):
        cls.precision = precision
        cls.base, cls.exponent = get_base(float(value))
        return super(EEValue, EEValue).__new__(cls, value)

    def E(cls, series: int = 96, mode: str = 'round', legacy: bool = True) -> float:
        exponent = max(-8, min(cls.exponent, 8))

        idx = E_inv(series, cls.base)

        if mode == "round":
            idx = round(idx)
            if series in [3, 6, 12, 24]:
                vals = (abs(cls.base - E_fwd(series, idx - 1, legacy)), abs(cls.base - E_fwd(series, idx, legacy)),
                        abs(cls.base - E_fwd(series, idx + 1, legacy)))
                idx += vals.index(min(vals)) - 1

        elif mode == "ceil":
            idx = ceil(idx)
        elif mode == "floor":
            idx = floor(idx)
        else:
            raise ValueError('Mode has to be either "round", "ceil" or "floor". {} is not a valid mode'.format(mode))

        return EEValue(E_fwd(series, idx, legacy) * 10**exponent)

    def __str__(cls):
        exponent = max(-24, min(cls.exponent, 24))
        idx = exponent // 3 + 8
        prefix = cls.Si_prefixes[idx]
        val = float(cls) / 10**((idx - 8) * 3)  # We do this to keep to 3 orders of magnitude
        return "{:.{}f} {}".format(val, cls.precision, prefix)

    def __repr__(cls):
        return "EEValue({})".format(float(cls))

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
