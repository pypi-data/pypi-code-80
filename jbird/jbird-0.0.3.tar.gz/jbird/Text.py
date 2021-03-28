from .File import File


class Text(File):
    """
    Class for working with the values file.
    """

    def __init__(self, path, file):
        super(Text, self).__init__(path, file, False)
