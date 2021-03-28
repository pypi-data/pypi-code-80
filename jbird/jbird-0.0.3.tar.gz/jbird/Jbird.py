from .Binary import Binary
from .Text import Text


class Jbird():

    bin_file = 'keys.bin'
    txt_file = 'values.txt'

    def __init__(self, path):
        self.path = path
        self.key = Binary(self.path, self.bin_file)
        self.value = Text(self.path, self.txt_file)

    # save the data
    def set(self, key, value):
        self.value.write(self.value.length, value)
        self.key.insert(key, self.value.length, len(value))

    # load the data
    def get(self, key):
        value_pos, value_length = self.key.select(key)
        if value_pos != None and value_length != None:
            return self.value.read(value_pos, value_length)
