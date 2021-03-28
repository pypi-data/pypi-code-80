import hashlib
from .File import File


class Binary(File):
    """
    Class for working with the keys file.
    """

    # parameters of data chunks
    hash_len, pos_len, length_len = 40, 5, 5
    chunk_len = hash_len + pos_len + length_len

    def __init__(self, path, file):
        super(Binary, self).__init__(path, file, True)

    # get sha1 of the string
    def hash(self, txt: str) -> bytes:
        txt_bytes = str.encode(txt)
        hash_obj = hashlib.sha1(txt_bytes)
        hash_str = hash_obj.hexdigest()
        hash_bytes = str.encode(hash_str)
        return hash_bytes

    # get position of the middle chunk between start_pos and end_pos
    def get_middle(self, start_pos, end_pos):
        return int(((end_pos + start_pos) // self.chunk_len) / 2) * self.chunk_len

    # insert data into custom position (also push apart the other data)
    def insert(self, key, pos, length):

        key_hash = self.hash(key)
        value_pos = pos.to_bytes(self.pos_len, 'big')
        value_len = length.to_bytes(self.length_len, 'big')
        data = b''.join([key_hash, value_pos, value_len])

        start_pos = 0
        start_hash = self.read(0, self.hash_len)

        end_pos = self.length - self.chunk_len if self.length > 0 else 0
        end_hash = self.read(end_pos, self.hash_len)

        if end_hash and key_hash > end_hash:
            key_pos = end_pos + self.chunk_len

        elif not start_hash or key_hash < start_hash:
            key_pos = 0

        else:
            middle_pos = self.get_middle(start_pos, end_pos)
            middle_hash = self.read(middle_pos, self.hash_len)

            while middle_pos != start_pos and middle_pos != end_pos:

                if key_hash > middle_hash:
                    start_pos = middle_pos
                else:
                    end_pos = middle_pos

                middle_pos = self.get_middle(start_pos, end_pos)
                middle_hash = self.read(middle_pos, self.hash_len)

            key_pos = middle_pos + self.chunk_len

        self.length = self.length + self.chunk_len
        self.push(key_pos, self.chunk_len)
        self.write(key_pos, data)

    # binary search of the hash
    def select(self, key):

        key_hash = self.hash(key)
        key_pos = None

        start_pos = 0
        start_hash = self.read(0, self.hash_len)

        end_pos = self.length - self.chunk_len if self.length > 0 else 0
        end_hash = self.read(end_pos, self.hash_len)

        if end_hash and key_hash == end_hash:
            key_pos = end_pos

        elif start_hash and key_hash == start_hash:
            key_pos = 0

        else:
            middle_pos = self.get_middle(start_pos, end_pos)
            middle_hash = self.read(middle_pos, self.hash_len)

            while middle_pos != start_pos and middle_pos != end_pos:

                if middle_hash == key_hash:
                    key_pos = middle_pos
                    break

                if key_hash > middle_hash:
                    start_pos = middle_pos
                else:
                    end_pos = middle_pos

                middle_pos = self.get_middle(start_pos, end_pos)
                middle_hash = self.read(middle_pos, self.hash_len)

        if key_pos:
            chunk = self.read(key_pos, self.chunk_len)
            value_pos_bytes = chunk[self.hash_len:self.hash_len + self.pos_len]
            value_length_bytes = chunk[self.hash_len + self.pos_len:self.chunk_len]

            value_pos = int.from_bytes(value_pos_bytes, 'big')
            value_length = int.from_bytes(value_length_bytes, 'big')

            return value_pos, value_length

        return None, None
