import os


class File:
    """
    Class for working with the file.
    """

    def __init__(self, path, file, is_bin):
        self.path = path
        self.file = file
        self.is_bin = is_bin
        self.length = self.len()
        self.touch()

    # create if not exists file and dir
    def touch(self):

        # create dir if not exists
        if not os.path.exists(self.path):
            os.mkdir(self.path)

        # create file if not exists
        if not os.path.isfile(os.path.join(self.path, self.file)):
            open(os.path.join(self.path, self.file), 'w').close()

    # get length of the file (0 if not exists)
    def len(self):
        if os.path.isfile(os.path.join(self.path, self.file)):
            mode = 'rb' if self.is_bin else 'r'
            with open(os.path.join(self.path, self.file), mode) as f:
                f.seek(0, 2)
                return f.tell()
        return 0

    # write data to the custom position
    def write(self, pos, data):
        mode = 'r+b' if self.is_bin else 'r+'
        with open(os.path.join(self.path, self.file), mode) as f:
            f.seek(pos)
            f.write(data)

    # read data from the custom position
    def read(self, pos, length):
        mode = 'rb' if self.is_bin else 'r'
        with open(os.path.join(self.path, self.file), mode) as f:
            f.seek(pos)
            return f.read(length)

    # shift data from custom position toward the end
    def push(self, pos, length):
        mode = 'r+b' if self.is_bin else 'r+'
        with open(os.path.join(self.path, self.file), mode) as f:
            for i in reversed(range(pos, self.length + length, length)):
                f.seek(i)
                data = f.read(length)
                f.seek(i + length)
                f.write(data)
