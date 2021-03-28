import time
import random
import base64
import os

class Generator:
    _ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyz"
    _COUNTER = 0

    def _to_base36(self, number):  # type: (int) -> str
        if number < 0:
            raise ValueError("Cannot encode negative numbers")

        chars = ""
        while number != 0:
            number, i = divmod(number, 36)  # 36-character alphabet
            chars = self._ALPHABET[i] + chars

        return chars or "0"

    def _pad(self, number):
        padding = "0000"
        num_len = len(str(number))
        padding_len = len(padding) - num_len

        if padding_len >= 0:
            padding = padding[:padding_len] + str(number)

        return padding

    def _b36_time(self):
        return self._to_base36(time.time_ns())

    def _counter(self):
        self._COUNTER += 1

        if self._COUNTER == 9999:
            self._COUNTER = 0

        padded = self._pad(self._COUNTER).encode()
        
        return base64.b64encode(padded).decode()[:-2]

    def _random(self):
        return base64.b64encode(os.urandom(6)).decode()[:6].replace('/', 'n').replace('+', 'y')

    def fuid(self):
        return "%s%s%s" % (self._b36_time(), self._counter(), self._random())

if __name__ == "__main__":
    import timeit

    times = 9999
    
    #fuid
    time_to_run = timeit.timeit("gen = fuid.Generator();gen.fuid()", setup="import fuid", number=times)
    time_each = time_to_run / times

    fuid = Generator()

    print("{:.6f}ms / fuid ({})".format(time_each * 1000, fuid.fuid()))
    
