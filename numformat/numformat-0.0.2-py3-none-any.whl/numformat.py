from numformat.formatter import Formatter
from numformat.operators.operator_factory import OperatorFactory
from numformat.utils import convert_to_numeric


def autoformat(value,
               max_sig_figs: int = None,
               max_length: int = None,
               allow_scientific_notation: bool = True,
               allow_engineering_notation: bool = True,
               preserve_sig_figs: bool = False,
               strict: bool = False):
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


def sciformat(value):
    value = convert_to_numeric(value)
    operator = OperatorFactory.get_operator(value)
    return operator.to_scientific_notation()


def enggformat(value):
    value = convert_to_numeric(value)
    operator = OperatorFactory.get_operator(value)
    return operator.to_engineering_notation()


def get_sigfigs(value):
    value = convert_to_numeric(value)
    operator = OperatorFactory.get_operator(value)
    return operator.get_sigfigs()


def set_sigfigs(value, sigfigs):
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
