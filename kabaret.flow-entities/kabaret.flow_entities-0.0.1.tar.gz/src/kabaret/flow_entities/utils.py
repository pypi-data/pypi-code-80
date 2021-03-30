import keyword
import string


def isidentifier(ident):
    """
    PY2+PY3 valid Python identifier check.
    (inspired by
    https://stackoverflow.com/questions/12700893/
    how-to-check-if-a-string-is-a-valid-python-identifier-including-keyword-check
    )
    """

    if not isinstance(ident, str):
        return False

    if not ident:
        return False

    if keyword.iskeyword(ident):
        return False

    first = "_" + string.ascii_lowercase + string.ascii_uppercase
    if ident[0] not in first:
        return False

    other = first + string.digits
    for ch in ident[1:]:
        if ch not in other:
            return False

    return True


def identifier_param_split(param_value):
    """
    Returns a list of valide identifiers and
    a list of invalid identifiers from the
    given string.

    The string must contain a space separated
    list of names.
    """
    names = [n.strip() for n in param_value.split() if n.strip()]
    valid_names = [n for n in names if isidentifier(n)]
    invalid_names = [n for n in names if n not in valid_names]
    return valid_names, invalid_names
