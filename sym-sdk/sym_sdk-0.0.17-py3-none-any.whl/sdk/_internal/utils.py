from functools import wraps


def wrap_with_error(error_class):
    def wrapper(fn):
        @wraps(fn)
        def wrapped(*args, **kwargs):
            try:
                return fn(*args, **kwargs)
            except Exception:
                raise error_class()

        return wrapped

    return wrapper


def wrap_with_typed_error(error_class, error_enumeration):
    def wrapper(fn):
        @wraps(fn)
        def wrapped(*args, **kwargs):
            try:
                return fn(*args, **kwargs)
            except error_class:
                raise
            except Exception as exc:
                try:
                    lookup = getattr(error_enumeration, "UNKNOWN_ERROR")
                except:
                    raise RuntimeError("Internal Error: could not look up error codes") from exc

                raise error_class(lookup) from exc

        return wrapped

    return wrapper
