from .File import File


class Value(File):
    """
    Class for working with the values file.
    """

    def __init__(self, path, file):
        super(Value, self).__init__(path, file, False)
