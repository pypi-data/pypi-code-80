from numformat.formatter import Formatter
from numformat.operators.operator_factory import OperatorFactory
from numformat.utils import convert_to_numeric
from typing import Union
from decimal import Decimal


def autoformat(value: Union[int, float, Decimal, str],
               max_sig_figs: int = None,
               max_length: int = 10,
               allow_scientific_notation: bool = True,
               allow_engineering_notation: bool = True,
               preserve_sig_figs: bool = False,
               strict: bool = False) -> str:
    """
    Format a number-like object to a string with smart default options.

    Parameters
    ----------
    value : int, float, decimal.Decimal, or str.
        The number-like object to be formatted.
    max_sig_figs : int, default None
        The maximum number of significant figures to keep in the formatted number if possible. If None, no action
        is taken on reducing the number of significant figures in the formatted number.
    max_length : int, default 10
        The maximum number of characters allowed in the resultant formatted string.
    allow_scientific_notation : bool, default True
        If True, allow scientific notation as an option for the formatted string.
    allow_engineering_notation : bool, default True
        If True, allow engineering notation as an option for the formatted string.
    preserve_sig_figs : bool, default False
        If True, preserve all significant figures that were part of the original input 'value'.
    strict : bool, default False
        If True, raise a ValueError if a given input cannot be formatted within the 'max_length' specified.
    """
    __check_autoformat_args(max_sig_figs=max_sig_figs,
                            max_length=max_length,
                            allow_scientific_notation=allow_scientific_notation,
                            allow_engineering_notation=allow_engineering_notation)

    value = convert_to_numeric(value)
    operator = OperatorFactory.get_operator(value)
    operator.set_sigfigs(desired_sig_figs=max_sig_figs)
    if operator.is_zero():
        return operator.to_standard_notation()

    nf = Formatter(operator=operator, max_length=max_length,
                   allow_scientific_notation=allow_scientific_notation,
                   allow_engineering_notation=allow_engineering_notation,
                   preserve_sig_figs=preserve_sig_figs,
                   strict=strict)
    return nf.to_max_length()


def sciformat(value: Union[int, float, Decimal, str]) -> str:
    """
    Format a number-like object to a string representation in scientific notation.

    Parameters
    ----------
    value : int, float, decimal.Decimal, or str.
        The number-like object to be formatted.
    """
    value = convert_to_numeric(value)
    operator = OperatorFactory.get_operator(value)
    return operator.to_scientific_notation()


def enggformat(value: Union[int, float, Decimal, str]) -> str:
    """
    Format a number-like object to a string representation in engineering notation.

    Parameters
    ----------
    value : int, float, decimal.Decimal, or str.
        The number-like object to be formatted.
    """
    value = convert_to_numeric(value)
    operator = OperatorFactory.get_operator(value)
    return operator.to_engineering_notation()


def get_sigfigs(value: Union[int, float, Decimal, str]) -> int:
    """
    Get the number of significant figures of a number-like object.

    Parameters
    ----------
    value : int, float, decimal.Decimal, or str.
        The number-like object whose significant figures are calculated and returned.
    """
    value = convert_to_numeric(value)
    operator = OperatorFactory.get_operator(value)
    return operator.get_sigfigs()


def set_sigfigs(value: Union[int, float, Decimal, str], sigfigs: int) -> Union[int, float, Decimal, str]:
    """
    Set the number of significant figures of a number-like object. Note that you cannot increase the number of
    significant figures, you can only reduce it.

    Parameters
    ----------
    value : int, float, decimal.Decimal, or str.
        The number-like object whose significant figures are to be set.
    sigfigs: int
        The number of significant figures to be set on the input 'value'.
    """
    value = convert_to_numeric(value)
    operator = OperatorFactory.get_operator(value)
    operator.set_sigfigs(sigfigs)
    return operator.value


# Private Methods


def __check_autoformat_args(max_sig_figs: int,
                            max_length: int,
                            allow_scientific_notation: bool,
                            allow_engineering_notation: bool):
    if max_sig_figs is not None and max_sig_figs < 1:
        raise ValueError('\'max_sig_figs\' must be >= 1. Received {}'.format(max_sig_figs))
    if max_length is not None and max_length < 3:
        raise ValueError('\'max_str_length\' must be >= 3. Received {}'.format(max_sig_figs))
    if not isinstance(allow_scientific_notation, bool):
        raise ValueError(
            '\'allow_scientific_notation\' must be a boolean. Received {}'.format(allow_scientific_notation))
    if not isinstance(allow_engineering_notation, bool):
        raise ValueError(
            '\'allow_engineering_notation\' must be a boolean. Received {}'.format(allow_engineering_notation))
