import itertools
from copy import deepcopy

import six

from snoop.utils import with_needed_parentheses, my_cheap_repr, ensure_tuple

if six.PY2:
    from collections import Mapping, Sequence
else:
    from collections.abc import Mapping, Sequence


class BaseVariable(object):
    def __init__(self, source, exclude=()):
        self.source = source
        self.exclude = ensure_tuple(exclude)
        self.code = compile(source, '<variable>', 'eval')
        self.unambiguous_source = with_needed_parentheses(source)

    def items(self, frame):
        try:
            main_value = eval(self.code, frame.f_globals or {}, frame.f_locals)
        except Exception:
            return ()
        return self._items(main_value)

    def _items(self, key):
        raise NotImplementedError


class CommonVariable(BaseVariable):
    def _items(self, main_value):
        result = [(self.source, main_value)]
        for key in self._safe_keys(main_value):
            try:
                if key in self.exclude:
                    continue
                value = self._get_value(main_value, key)
            except Exception:
                continue
            result.append((
                '{}{}'.format(self.unambiguous_source, self._format_key(key)),
                value,
            ))
        return result

    def _safe_keys(self, main_value):
        try:
            for key in self._keys(main_value):
                yield key
        except Exception:
            pass

    def _keys(self, main_value):
        return ()

    def _format_key(self, key):
        raise NotImplementedError

    def _get_value(self, main_value, key):
        raise NotImplementedError


class Attrs(CommonVariable):
    def _keys(self, main_value):
        return itertools.chain(
            getattr(main_value, '__dict__', ()),
            getattr(main_value, '__slots__', ())
        )

    def _format_key(self, key):
        return '.' + key

    def _get_value(self, main_value, key):
        return getattr(main_value, key)


class Keys(CommonVariable):
    def _keys(self, main_value):
        return main_value.keys()

    def _format_key(self, key):
        return '[{}]'.format(my_cheap_repr(key).replace('\n', ' ').replace('\r', ' '))

    def _get_value(self, main_value, key):
        return main_value[key]


class Indices(Keys):
    _slice = slice(None)

    def _keys(self, main_value):
        return range(len(main_value))[self._slice]

    def __getitem__(self, item):
        assert isinstance(item, slice)
        result = deepcopy(self)
        result._slice = item
        return result


class Exploding(BaseVariable):
    def _items(self, main_value):
        if isinstance(main_value, Mapping):
            cls = Keys
        elif isinstance(main_value, Sequence):
            cls = Indices
        else:
            cls = Attrs

        return cls(self.source, self.exclude)._items(main_value)
