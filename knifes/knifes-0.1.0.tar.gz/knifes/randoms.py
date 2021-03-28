import random
import string
import threading
import time
from .digests import md5


def random_str(length=4):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


def make_unique_str():
    return md5(str(threading.current_thread().ident) + str(time.time()))
