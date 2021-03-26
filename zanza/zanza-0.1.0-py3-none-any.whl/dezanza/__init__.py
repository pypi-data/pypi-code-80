"""
This script deobfuscates the input sequence that was
obfuscated by `zanza`.

The input needs to be a JSON-encoded list passed as a
string. To not to confuse the shell with special
characters like [ and ], the input has to be wrapped
in double quotes.
"""

def _reduce(fn, iterable, initializer):
    """Helper method to reduce the input list
    to a single value.

    Args:
        fn: Callback function
        iterable: Input list
        initializer: Initial value
    """

    it = enumerate(iterable)
    value = initializer
    for idx, element in it:
        value = fn(value, element, idx)
    return value


def dezanza(source):
    """Deobfuscate the input sequence.

    Args:
        source (list): JSON-encoded list
    """

    if len(source) == 0:
        raise ValueError("Invalid input: zero length sequence")

    first = source[0]

    if type(first) is not list:
        raise ValueError("Invalid input: first element needs to be a list")

    ret = ""
    first.reverse()
    prev = _reduce(lambda acc, val, idx: acc + val * 10 ** idx, first, 0)
    ret += chr(prev)

    for item in source[1:]:
        curr = prev + item
        ret += chr(curr)
        prev = curr

    return ret
