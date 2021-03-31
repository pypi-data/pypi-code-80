"""
Functions for reading the Hyper-V KV files present on a Linux guest.
"""

from collections import OrderedDict


def read_kv(fileobj, encoding="utf-8"):
    """
    Read a Hyper-V KV file and return a dictionary with all of the file's key/value pairs decoded from their
    byte arrays to unicode strings.

    :param fileobj: a file-like object containing the Hyper-V KV data
    :param encoding: the encoding we assume is in the KV data. This for decoding into unicode.
    :return: an OrderedDict of key/value pairs that reflect what was read from the Hyper-V file given
    """
    kv = OrderedDict()
    while True:
        key = fileobj.read(512)
        val = fileobj.read(2048)
        if not key:
            break
        key = key[:key.find(b'\x00')]
        val = val[:val.find(b'\x00')]
        keystr = key.decode(encoding)
        valstr = val.decode(encoding)
        kv[keystr] = valstr
    return kv


def read_kv_from_file(filepath, encoding="utf-8"):
    """
    Open the given file path for reading bytes and pass to the read_kv function defined above.

    :param filepath: a path to a .kvp_pool_* file
    :param encoding: the encoding to use when converting this file's bytes into unicode
    :return: an OrderedDict of key/value pairs that reflect what was read from the Hyper-V file given
    """
    with open(filepath, 'rb') as infile:
        return read_kv(infile, encoding)
