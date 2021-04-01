class LoopStateError(Exception):
    pass
    
class DBError(Exception):
    pass


class MethodError(Exception):
    pass

class LongpollError(MethodError):
    pass


class LibraryError(Exception):
    pass

class LibraryException(LibraryError):
    pass

class LibraryRewriteError(LibraryError):
    pass

class LibraryReload(LibraryException):
    pass

class CallVoid(LibraryException):
    pass

class Quit(LibraryException):
    pass
