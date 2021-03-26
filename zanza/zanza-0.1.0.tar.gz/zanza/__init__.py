"""
This script obfuscates the input string by the following algorithm:

- Takes the first character of the input string, and gets its Unicode
  code point (character code)
- Sets this char code as a reference value
- Initializes a *list* in which stores the digits of the previous
  value as a *list*
- Continues to the next character by calculating its code point and
  the delta to the previous character's code point.
- Sets the current code point as the next reference value
- Adds this delta value to the return list and repeats the steps
  above to the input strings length.
"""

def zanza(source):
    """Obfuscate the input string.

    Args:
        source (str): Input string
    """

    if len(source) == 0:
        raise ValueError("Invalid input: zero-length string")

    ret = []
    prev = ord(source[0])
    first = map(int, str(prev))
    ret.append(list(first))

    for s in source[1:]:
        curr = ord(s)
        ret.append(curr - prev)
        prev = curr

    return ret
