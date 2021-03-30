#coding: utf-8
import string

def run(str):
    _en = _dg = _sp = _zh = _pu = 0
    for s in str:
        if s in string.ascii_letters:
            _en += 1
        elif s.isdigit():
            _dg += 1
        elif s.isspace():
            _sp += 1
        elif s.isalpha():
            _zh += 1
        else:
            _pu += 1
    return _en, _dg, _sp, _zh, _pu
