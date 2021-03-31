class CircularReference(Exception):
    """Name of cell used in formula"""


class InvalidType(ValueError):
    """Not valid value due its type"""


class MissingParameter(ValueError):
    """Not valid value due its type"""


class DangerousFormula(Exception):
    """Formula has elements wich not are math expressions"""


class InvalidName(ValueError):
    """Not valid name given"""


class FailedCalculation(Exception):
    """Could not achieve calculation"""
