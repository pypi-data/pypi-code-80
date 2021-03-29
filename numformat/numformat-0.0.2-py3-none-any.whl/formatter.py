from typing import Iterable

from numformat.operators.operator import Operator


class Formatter:

    def __init__(self, operator, max_length,
                 allow_scientific_notation=True,
                 allow_engineering_notation=True,
                 preserve_sig_figs=False,
                 strict=False):
        self.operator: Operator = operator
        self.max_length = max_length
        self.allow_scientific_notation = allow_scientific_notation
        self.allow_engineering_notation = allow_engineering_notation
        self.preserve_sig_figs = preserve_sig_figs
        self.strict = strict

    def to_max_length(self):

        s = self.operator.to_standard_notation()
        sci = None
        e = None

        if self.max_length is None:
            return s
        else:
            if len(s) <= self.max_length:
                return s
            if self.allow_scientific_notation:
                sci = self.operator.to_scientific_notation()
                if len(sci) <= self.max_length:
                    return sci
                if not self.preserve_sig_figs:
                    sci = self._coerce_scientific_length(sci)
                    if len(sci) <= self.max_length:
                        return sci
            if self.allow_engineering_notation:
                e = self.operator.to_engineering_notation()
                if len(e) <= self.max_length:
                    return e
                if not self.preserve_sig_figs:
                    e = self._coerce_engineering_length(e)
                    if len(e) <= self.max_length:
                        return e
            if self.strict:
                raise ValueError('Could not represent the input within {} characters.'.format(self.max_length))
            else:
                return self._get_shortest_string([s, sci, e])

    def to_shortest(self):
        s = self.operator.to_standard_notation()
        sci = self.operator.to_scientific_notation()
        e = self.operator.to_engineering_notation()
        return self._get_shortest_string([s, sci, e])

    # Private methods

    def _coerce_scientific_length(self, current_string):
        digit_difference = len(current_string) - self.max_length
        sig_figs = self.operator.get_sigfigs()
        if digit_difference < sig_figs:
            desired_sig_figs = sig_figs - digit_difference
            self.operator.set_sigfigs(desired_sig_figs)
            return self.operator.to_scientific_notation()
        return current_string

    def _coerce_engineering_length(self, current_string):
        digit_difference = len(current_string) - self.max_length
        sig_figs = self.operator.get_sigfigs()
        if digit_difference < sig_figs:
            desired_sig_figs = sig_figs - digit_difference
            self.operator.set_sigfigs(desired_sig_figs)
            return self.operator.to_engineering_notation()
        return current_string

    @staticmethod
    def _get_shortest_string(strings: Iterable[str]):
        strings = [x for x in strings if x is not None]
        return min(strings, key=len)
