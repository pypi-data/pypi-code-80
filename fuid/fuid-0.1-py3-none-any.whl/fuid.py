import time
import random
import base64
import os

_ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyz"
_COUNTER = 0

def _to_base36(number):  # type: (int) -> str
    if number < 0:
        raise ValueError("Cannot encode negative numbers")

    chars = ""
    while number != 0:
        number, i = divmod(number, 36)  # 36-character alphabet
        chars = _ALPHABET[i] + chars

    return chars or "0"

def _pad(number):
    padding = "0000"
    num_len = len(str(number))
    padding_len = len(padding) - num_len

    if padding_len >= 0:
        padding = padding[:padding_len] + str(number)

    return padding

def _b36_time():
    return _to_base36(int(time.time()*1000.0))

def _counter():
    global _COUNTER
    
    _COUNTER += 1

    if _COUNTER == 9999:
        _COUNTER = 0

    padded = _pad(_COUNTER).encode()
    
    return base64.b64encode(padded).decode()[:-2]

def _random():
    return _to_base36(random.getrandbits(32))[:6]

def fuid():
    return "%s%s%s" % (_b36_time(), _counter(), _random())

if __name__ == "__main__":
    import timeit

    times = 9999
    
    #fuid
    time_to_run = timeit.timeit("fuid.fuid()", setup="import fuid", number=times)
    time_each = time_to_run / times

    print("{:.6f}ms / fuid ({})".format(time_each * 1000, fuid()))
    
