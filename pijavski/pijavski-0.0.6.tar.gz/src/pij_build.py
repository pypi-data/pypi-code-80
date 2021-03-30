
import cffi
import os

ffibuilder = cffi.FFI()

PATH = os.path.dirname(__file__)

def readfile(fil):
    with open(fil, 'r') as f:
        content = f.read()
    return content

ffibuilder.cdef(readfile(os.path.join(PATH, "cdefs.h")), override=True)

ffibuilder.set_source("_pijavski", r"""
    #include "heap.h"
    #include "pijavski.h"
""",
    sources=[os.path.join(PATH, "pijavski.cpp")],
    include_dirs=[PATH]
    )


if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
